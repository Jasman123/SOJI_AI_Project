from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters.character import CharacterTextSplitter
import json

class ApplicabilityRules(BaseModel):
    aircraft_models: List[str]
    msn_constraints: Optional[str] = None
    excluded_if_modifications: List[str]
    required_modifications: List[str]

class Rules(BaseModel):
    ad_id: str
    applicability_rules: ApplicabilityRules


def load_pdf(file_path: str) -> str:
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    for i in range(len(docs)):
        docs[i].page_content =' '.join(docs[i].page_content.split())

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    pages_splitter = text_splitter.split_documents(docs)
    return pages_splitter

documents = load_pdf("EASA_AD_2025-0254_1.pdf")
print(documents)

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
).with_structured_output(Rules)

results =[]
for i, doc in enumerate(documents):
    print(f"--- PDF Page {i+1} ---")
    print(doc.page_content)
    response = llm.invoke(
        f"""
        Extract the applicability rules from the following Airworthiness Directive (AD) text:

        {doc.page_content}

        Provide the output in the specified structured format.
        """
    )

    results.append(response.model_dump())
print(json.dumps(results, indent=2))