# SOJI_AI_Project

SOJI_AI_Project is a structured pipeline that processes PDF documents, extracts structured information, generates JSON output, converts the extracted data into vector embeddings, and performs retrieval or question-answering tasks using a test application.  
This project is built using **RAG (Retrieval-Augmented Generation)**, **LangGraph**, and **Chroma** vector store.

---

## Features

- 📄 **PDF Document Ingestion** — Upload or provide PDF documents which the system loads and parses into machine-readable text.  
- ✂️ **Text Splitting & Chunking** — Split large documents into manageable chunks suitable for embedding.  
- 🔗 **Vector Embedding Generation** — Convert text chunks into vector embeddings for semantic representation.  
- 🗄️ **Vector Store** — Store embeddings in a vector database (Chroma) for efficient semantic retrieval. 
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


- `Genererate_json.py` — Script/module responsible for extracting structured data from processed documents, and outputting JSON.  
- `generate_vectore.py` — Module that reads the extracted data (or text chunks), computes embeddings, and stores them into the vector store (Chroma).  
- `app_test.py` — Demonstration/test app showing how to query the vector store and perform retrieval or QA tasks.  
- `ad_results.json` — Example output (structured data) after running the pipeline on sample PDFs.  
- PDF files — Example or sample documents used for ingestion/testing.  
- `requirements.txt` — Dependency list for Python environment.  

---

## How It Works (Pipeline Overview)

1. **Document Loading** — Load one or more PDF documents.  
2. **Text Extraction & Preprocessing** — Extract text from PDF and preprocess (clean up, normalize).  
3. **Text Splitting / Chunking** — Split long text into chunks to suit embedding model / context window constraints.  
4. **Embedding Generation** — For each chunk, generate vector embedding (semantic representation).  
5. **Vector Store Insertion** — Store embeddings (with metadata, e.g. document ID, chunk info) into a vector store (Chroma).  
6. **Question / Query Handling** — When user provides a question or query:  
   - Embed the query into a vector.  
   - Search the vector store for top-k most similar chunks.  
   - Retrieve the corresponding text chunks (context).  
7. **Prompt Construction** — Build a prompt that includes the retrieved context + user question (e.g. “Answer based only on the following context …”).  
8. **LLM Generation** — Use a language model to generate an answer based on the prompt + context (RAG).  
9. **Return Answer (with References / Metadata)** — Return answer along with source metadata (which document/chunk used), enabling transparency.  

This architecture (chunking → embedding → vector store → retrieval → LLM) is broadly similar to other PDF-to-chatbot systems built with frameworks like LangChain + vector stores (e.g. Chroma).

---


<img width="187" height="432" alt="graph_xray" src="https://github.com/user-attachments/assets/153d96ab-88a8-441d-920f-8d496b552f0c" />


