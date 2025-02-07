import argparse
import os
from langchain_chroma import Chroma 
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama  # Ensuring consistency in imports
from langchain_ollama import OllamaEmbeddings 

# from langchain.embeddings import OpenAIEmbeddings # openai embedding
# openai_api_key = os.getenv("OPENAI_API_KEY")

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def get_embedding():
    return OllamaEmbeddings(model="nomic-embed-text")
    # return OpenAIEmbeddings(openai_api_key=openai_api_key)

def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)

def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    # Construct the context text.
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    
    # Format the prompt.
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Invoke the model.
    model = Ollama(model="mistral")
    response_text = model.invoke(prompt)

    # Extract sources.
    sources = [doc.metadata.get("id", "Unknown") for doc, _ in results]
    formatted_response = f"Response: \n\n{response_text}\n\nSources: {sources}"
    
    # print(formatted_response)
    return response_text

if __name__ == "__main__":
    main()
