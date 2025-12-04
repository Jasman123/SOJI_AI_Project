# SOJI_AI_Project

SOJI_AI_Project is a structured pipeline that processes PDF documents, extracts structured information, generates JSON output, converts the extracted data into vector embeddings, and performs retrieval or question-answering tasks using a test application.  
This project is built using **RAG (Retrieval-Augmented Generation)**, **LangGraph**, and **Chroma Vector Store**.

---

## 📁 Project Structure

SOJI_AI_Project/
├── Genererate_json.py
├── generate_vectore.py
├── app_test.py
├── ad_results.json
├── requirements.txt
└── README.md



---

## 🧠 Overview

The system performs three main actions:

1. **Extract structured data from PDF files → JSON**  
2. **Create vector embeddings from the JSON data and store in ChromaDB**  
3. **Run RAG/LangGraph application to test retrieval and question-answering**

This README explains each script in detail in the correct workflow order.

---

# 1. `Genererate_json.py`

### 🎯 Purpose  
This script loads one or more PDF files and extracts structured content using an LLM.  
It then generates a clean JSON file containing the extracted and normalized information.

### 🧩 What the script does
- Loads PDF documents (e.g., *EASA Airworthiness Directives*).
- Splits pages if needed.
- Uses an LLM to:
  - Extract important fields (ex: AD number, title, affected aircraft, compliance requirements, etc.).
  - Convert messy PDF text into structured JSON.
- Saves the final data into **`ad_results.json`**.

### 🗂 Output Example
You will get a clean JSON such as:

```json
[
  {
    "ad_id": "2025-0254",
    "source_file": "EASA_AD_2025-0254.pdf",
    "summary": "...",
    "affected_models": [...],
    "requirements": "...",
    "references": [...]
  }
]

### ▶️ Run the script

python Genererate_json.py

Important: This script must be run first before generating the vector database.

# 2. generate_vectore.py
### 🎯 Purpose

This script reads the JSON generated earlier and transforms each entry into vector embeddings using an embedding model.

### 🧩 What the script does

Loads ad_results.json

Creates embeddings using GoogleGenerativeAIEmbeddings or other embedding model.

Stores vectors inside a Chroma persistent vector store.

Prepares the database to be queried by the RAG system.

### 🗄 Vector Store

The script initializes Chroma like:

Chroma(
    collection_name="ad_collection",
    embedding_function=GoogleGenerativeAIEmbeddings(...),
    persist_directory="./chroma_db"
)

./chroma_db/

containing all vector embeddings.

### ▶️ Run the script

python generate_vectore.py

Ensure ad_results.json exists before generating vectors.

# 3. app_test.py
### 🎯 Purpose

This is the test application that connects everything:

* Loads the Chroma vector store

* Creates a Retrieval-Augmented Generation workflow using LangGraph

* Accepts user queries

* Retrieves the most relevant AD data

* Passes data into the LLM for final answers

### 🧩 Key Actions Inside the Script

Initialize LangGraph state machine.

Load messages and maintain graph transitions.

Query Chroma via similarity search.

Create structured outputs from LLM using LangGraph’s Pydantic integration.

Produce final answer with citations.

### ▶️ Run the Script

python app_test.py











