# SOJI_AI_Project

SOJI_AI_Project is a structured pipeline that processes PDF documents, extracts structured information, generates JSON output, converts the extracted data into vector embeddings, and performs retrieval or question-answering tasks using a test application.  
This project is built using **RAG (Retrieval-Augmented Generation)**, **LangGraph**, and **Chroma** vector store.

---

## Features

- 📄 **PDF Document Ingestion** — Upload or provide PDF documents which the system loads and parses into machine-readable text.  
- ✂️ **Text Splitting & Chunking** — Split large documents into manageable chunks suitable for embedding.  
- 🔗 **Vector Embedding Generation** — Convert text chunks into vector embeddings for semantic representation.  
- 🗄️ **Vector Store** — Store embeddings in a vector database (Chroma) for efficient semantic retrieval. :contentReference[oaicite:0]{index=0}  
- 🔍 **Semantic Search & Retrieval** — Given a query or question, retrieve the most relevant chunks based on embedding similarity.  
- 💬 **Question-Answering / Retrieval-Augmented Generation** — Use retrieved context to generate answers to user queries (via LLM + prompt templating), enabling a PDF-driven QA/chat interface.  
- 🧪 **Test Application** — Example or minimal app to demonstrate ingest → vectorize → query → answer pipeline (e.g. `app_test.py` in repo).

---

## Project Structure

```
SOJI_AI_Project/
├── EASA_AD_2025-0254_1.pdf
├── EASA_AD_US-2025-23-53_1.pdf
├── Genererate_json.py
├── generate_vectore.py
├── app_test.py
├── ad_results.json
├── requirements.txt
└── README.md
```


