import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader  # Updated import
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_ollama import OllamaEmbeddings  # Updated import
from langchain_chroma import Chroma  # Updated import

# from langchain.embeddings import OpenAIEmbeddings # openai embedding
# openai_api_key = os.getenv("OPENAI_API_KEY")

CHROMA_PATH = "chroma"
DATA_PATH = "dataset"

def get_embedding():
    return OllamaEmbeddings(model="nomic-embed-text")
    # return OpenAIEmbeddings(openai_api_key=openai_api_key)
    


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Load and process documents
    documents = load_documents()
    if not documents:
        print("⚠️ No documents loaded. Please check the dataset folder.")
        return
    
    chunks = split_documents(documents)
    add_to_chroma(chunks)

def load_documents():
    """Loads PDFs from the dataset directory, handling errors gracefully."""
    try:
        document_loader = PyPDFDirectoryLoader(DATA_PATH)
        documents = document_loader.load()
        return documents
    except Exception as e:
        print(f"❌ Error loading PDFs: {e}")
        return []

def split_documents(documents: list[Document]):
    """Splits documents into smaller chunks for better retrieval."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks: list[Document]):
    """Adds processed chunks to the Chroma vector database."""
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding()
    )

    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"📄 Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]

    if new_chunks:
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add")

def calculate_chunk_ids(chunks):
    """Assigns unique IDs to document chunks for efficient retrieval."""
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source", "unknown")
        page = chunk.metadata.get("page", "unknown")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk.metadata["id"] = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

    return chunks

def clear_database():
    """Deletes the existing Chroma database."""
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

if __name__ == "__main__":
    main()
