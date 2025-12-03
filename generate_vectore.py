import json
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_text_splitters.character import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
import re


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
chat = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="text-embedding-004",
    timeout=30,
    max_retries=2,
)


def load_json_file(path : str) -> str:
    with open(path, 'r') as f:
        data = json.load(f)

    docs=[]
    for item in data:

        if item['ad_id'] in [None, "", "None"]:
            continue

        text = f"""
    Airworthiness Directive : {item['ad_id']}
    Applicable Aircraft Models: {item['applicability_rules']['aircraft_models']}
    msn Constraints : {item['applicability_rules']['msn_constraints']}
    Excluded Modifications: {item['applicability_rules']['excluded_if_modifications']}
    Required Modification : {item['applicability_rules']['required_modifications']}
    """
        docs.append(
        Document(page_content=text, metadata={"ad_id": item["ad_id"]})
    )

    return docs

def build_vector_store(documents):
    vector_store = Chroma.from_documents(
        documents,
        embedding=embeddings,
        collection_name="pdf_docs",
        persist_directory="chroma_db"
    )
    
    return vector_store

document = load_json_file("ad_results.json")
for i in range(len(document)):
        document[i].page_content =' '.join(document[i].page_content.split())

vector_store = build_vector_store(document)
print("Vector store loaded.")
print("len of collection:", vector_store._collection.count())

# resutl = vector_store.as_retriever(
#     search_type="mmr",
#     search_kwargs={"k":3, 'lambda_mult': 0.7}
# )
# question = 'What is main topic of this document?'
# retrieved_docs = resutl.invoke(question)
# print("Retrieved Documents:")
# for doc in retrieved_docs:
#     print("---- Document ----")
#     print("page number:", doc.metadata.get('page'))
#     print(doc.page_content)







