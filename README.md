# 🚀 Retrieval-Augmented Generation (RAG) for Document Querying  

This repository contains a **Retrieval-Augmented Generation (RAG) system** that allows you to query documents and retrieve accurate, context-aware responses. The RAG model is seamlessly integrated into **OpenWebUI**, making it easy to interact with using a chat-based interface.  

## ✨ Features  

- **Document Processing** 📄: Reads and processes documents efficiently.  
- **Vector Database Integration** 🔍: Stores document embeddings for fast and accurate retrieval.  
- **Chunking & Indexing** 🏷️: Optimized for handling large documents with configurable chunk sizes.  
- **DeepSeek-R1:14B Model** 🤖: Utilizes a powerful **LLM** for generating high-quality responses.  
- **OpenWebUI Support** 🖥️: The RAG model functions as a backend for OpenWebUI, allowing users to query documents interactively.  

## ⚙️ Setup & Installation  

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/robaita/rag_with_openwebui.git
   cd rag_with_openwebui

2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt

3. **Create Vector Embeddings**  
   ```bash
   python database_operations.py

4. **Run the RAG System**  
   ```bash
   python main.py 'put your query here'

5. **Expose RAG as a REST API**  
   ```bash
   python app.py

6. **Test API**  
   ```bash
   python client.py

7. **Integrate with OpenWebUI**
    - Configure OpenWebUI to use this RAG model as a backend.
    - Start querying your documents with natural language!

## 🎯 Settings & Configuration 
- You can use different embeddings to benchmark the results and choose the one that suits yiur dataset.
- Tweak the chunk_size and chunk_overlap for better results
- Use the LLM model that is giving better performance

## 📌 Use Case
- **This RAG system is ideal for:**
- ✔ Resume screening and querying large collections of resumes 📑
- ✔ Research paper analysis 📚
- ✔ Legal document retrieval ⚖
- ✔ Technical documentation assistance 💡

## **🛠 Future Enhancements**
- Support for multi-modal data (PDFs, images, and tables).
- Fine-tuning the model for domain-specific applications.
- UI enhancements for better user experience.

## 🌟 Contribute & Support
Feel free to fork, open issues, or contribute to the project! 🚀


   