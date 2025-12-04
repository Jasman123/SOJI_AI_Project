from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, RemoveMessage
from typing import Literal
from IPython.display import Image, display
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List, Optional
import json

data_test = [
    {"Aircraft Model": "MD-11", "MSN": 48123, "Modifications": "None"},
    {"Aircraft Model": "DC-10-30F", "MSN": 47890, "Modifications": "None"},
    {"Aircraft Model": "Boeing 737-800", "MSN": 30123, "Modifications": "None"},
    {"Aircraft Model": "A320-214", "MSN": 5234, "Modifications": "None"},
    {"Aircraft Model": "A320-232", "MSN": 6789, "Modifications": "mod 24591 (production)"},
    {"Aircraft Model": "A320-214", "MSN": 7456, "Modifications": "SB A320-57-1089 Rev 04"},
    {"Aircraft Model": "A321-111", "MSN": 8123, "Modifications": "None"},
    {"Aircraft Model": "A321-112", "MSN": 364, "Modifications": "mod 24977 (production)"},
    {"Aircraft Model": "A319-100", "MSN": 9234, "Modifications": "None"},
    {"Aircraft Model": "MD-10-10F", "MSN": 46234, "Modifications": "None"}
]

class State(MessagesState):
    documents : list[str]
    json_result: dict | None

class ApplicabilityRules(BaseModel):
    aircraft_models: str
    msn_constraints: str
    modifications: str
    applicable : str


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
chat = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
).with_structured_output(ApplicabilityRules)

embeddings = GoogleGenerativeAIEmbeddings(
    model="text-embedding-004",
    timeout=30,
    max_retries=2,
)


def load_vector_store(embeddings):
    vector_store = Chroma(
        embedding_function=embeddings,
        collection_name="pdf_docs",
        persist_directory="chroma_db"
    )
    return vector_store

def retrieve_documents(state:State) -> State:
    vector_store = load_vector_store(embeddings)
    question = state["messages"][-1].content
    retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k":3, 'lambda_mult': 0.7}
    )
    docs = retriever.invoke(question)
    document_pages = [doc.page_content for doc in docs]
    return {"documents": document_pages}

def extract_json(state: State):
    last_msg = state["messages"][-1]

    if isinstance(last_msg, AIMessage):
        try:
            data = json.loads(last_msg.content)
        except:
            data = {"error": "Failed to parse JSON output"}
    else:
        data = {"error": "Last message is not AIMessage"}

    return {"json_result": data}

def chat_model(state: State) -> State:
    documents = "\n\n".join(state["documents"])
    question = state["messages"][-1].content
    prompt_template = PromptTemplate(
        input_variables=["documents", "question"],
        template="""
        Use the following documents to answer the question.
        
        Documents:
        {documents}
        
        Question:
        {question}
        
        Provide a detailed and accurate answer based on the documents.
        If the answer is not found in the documents, respond with "I don't know."
        """
    )
    prompt = prompt_template.format(documents=documents, question=question)
    state['messages'].append(HumanMessage(content=prompt))
    # print(state['messages'])
    response = chat.invoke(state['messages'])
    response_msg = AIMessage(content=response.model_dump_json())
    return {"messages": state['messages'] + [response_msg]}

builder = StateGraph(State)
builder.add_node("chat_model", chat_model)
builder.add_node("retrieve_documents", retrieve_documents)
builder.add_node("extract_json", extract_json)

builder.add_edge(START, "retrieve_documents")
builder.add_edge("retrieve_documents", "chat_model")
builder.add_edge("chat_model", "extract_json")
builder.add_edge("extract_json", END)

graph = builder.compile()
memory = MemorySaver()
react_graph_memory = builder.compile(checkpointer=memory)


# result = graph.invoke({
#     "messages": [
#         HumanMessage(content="is MD-11 is affected by rule  by FAA AD 2025-23-53 and EASA AD 2025-0254 (yes/no/not applicable)?")
#     ]
# })
# print(result["json_result"])     

final_result =[]

for item in data_test:
    question = f"is {item['Aircraft Model']} with MSN {item['MSN']} and Modifications {item['Modifications']} is affected by rule  by FAA AD 2025-23-53 and EASA AD 2025-0254 (yes/no/not applicable)?"
    result = graph.invoke({
        "messages": [
            HumanMessage(content=question)
        ]
    })
    json_result = result["json_result"]
    final_result.extend({
        "Aircraft Model": item['Aircraft Model'],
        "MSN": item['MSN'],
        "Modifications": item['Modifications'],
        "Applicable": json_result.get("applicable", "error"),
        "Details": json_result
    })
    print(json_result)


