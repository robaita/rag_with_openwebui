from flask import Flask, request, jsonify
import os, re
from langchain_chroma import Chroma 
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama  # Ensuring consistency in imports
from langchain_ollama import OllamaEmbeddings 

# from langchain.embeddings import OpenAIEmbeddings # openai embedding
# openai_api_key = os.getenv("OPENAI_API_KEY")

CHROMA_PATH = "chroma"

context = ''
question = ''

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

app = Flask(__name__)

@app.route('/api/query', methods=['POST'])
def api_query():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400


    answer = query_rag(query)
    print(answer)             
    return jsonify({"answer": answer})

def get_embedding():
    return OllamaEmbeddings(model="nomic-embed-text")
    # return OpenAIEmbeddings(openai_api_key=openai_api_key)


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    # Construct the context text.
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    
    context = ''
    
    for doc, _ in results:
        # print(f"Document: {doc.metadata.get('id', 'Unknown')}, Score: {score}")
        content = doc.page_content
        sources = doc.metadata.get("id", "Unknown")
        # print("Sources:",sources)
        item = sources.replace("dataset", "")
        item = item.replace(".pdf", "")
        item = item.replace("_", " ")
        item = item.replace("resume", "")
        item = item.replace("/", "")
        item = item.replace("\\", "")
        item = re.sub(r'[^A-Za-z\s]', '', item)

        context = context + f'Candidate name: {item} \n {content} \n\n'

    
    # print("Context:\n",context)
    # Format the prompt.
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    # prompt = prompt_template.format(context=context_text, question=query_text)

    prompt = prompt_template.format(context=context, question=query_text)

    # Invoke the model.
    model = Ollama(model="mistral")
    response_text = model.invoke(prompt)

    # Extract sources.
    sources = [doc.metadata.get("id", "Unknown") for doc, _ in results]
    formatted_response = f"Please find the asked information \n{response_text}\n\nSources: {sources}"
    
    # print(formatted_response)
    return formatted_response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Run Flask app
    # app.run(debug=True, port=5000)  # Run Flask app