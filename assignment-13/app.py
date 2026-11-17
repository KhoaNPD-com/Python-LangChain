# pip install langchain langgraph langchain-openai langchain-community pydantic faiss-cpu

import os
from typing import TypedDict, List
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.prebuilt import ToolNode

# -----------------------------
# CONFIG
# -----------------------------
from dotenv import load_dotenv
load_dotenv()

# -------------------------------
# OpenAI Config
# -------------------------------
# os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_GPT_4O_API_KEY')

# -------------------------------
# LLM Setup (OpenAI instead of Azure)
# -------------------------------
llm = ChatOpenAI(
    model=os.getenv('OPENAI_MODEL_GPT_4O'),
    temperature=0,
    base_url=os.getenv('OPENAI_ENDPOINT'),
    api_key=os.getenv('OPENAI_GPT_4O_API_KEY')
)

# -------------------------------
# Mock Medical Knowledge Base
# -------------------------------
mock_chunks = [
    Document(page_content="Sore throat: drink warm fluids, avoid cold drinks."),
    Document(page_content="Mild fever: rest and stay hydrated."),
    Document(page_content="Dizziness: check blood pressure and hydration."),
    Document(page_content="Persistent cough >2 weeks: consult doctor."),
    Document(page_content="Fatigue: may be due to iron deficiency or poor sleep."),
]

# -------------------------------
# Embeddings + FAISS
# -------------------------------
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    base_url=os.getenv('OPENAI_ENDPOINT'),
    api_key=os.getenv('AZURE_OPENAI_API_KEY')
)

db = FAISS.from_documents(mock_chunks, embedding_model)
retriever = db.as_retriever()

# -------------------------------
# TOOL 1: Retrieve Advice
# -------------------------------
@tool
def retrieve_advice(user_input: str) -> str:
    """Get medical advice from internal knowledge base."""
    docs = retriever.invoke(user_input)
    return "\n".join(doc.page_content for doc in docs)

# -------------------------------
# TOOL LIST
# -------------------------------
tools = [retrieve_advice]

# -------------------------------
# Bind tools to LLM
# -------------------------------
llm_with_tools = llm.bind_tools(tools)

# -------------------------------
# State Definition
# -------------------------------
from langchain_core.messages import BaseMessage

class State(TypedDict):
    messages: List[BaseMessage]

# -------------------------------
# Model Node
# -------------------------------
def call_model(state: State):
    messages = state["messages"]

    response = llm_with_tools.invoke(messages)

    # print("[DEBUG] Model Response:", response)

    return {"messages": messages + [response]}

# -------------------------------
# Conditional Routing
# -------------------------------
def should_continue(state: State):
    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return END

# -------------------------------
# Tool Node
# -------------------------------
tool_node = ToolNode(tools)

def call_tools(state: State):
    tool_result = tool_node.invoke(state)

    return {
        "messages": state["messages"] + tool_result["messages"]
    }

# -------------------------------
# Build Graph
# -------------------------------
builder = StateGraph(State)

builder.add_node("model", call_model)
builder.add_node("tools", call_tools)

builder.set_entry_point("model")

builder.add_conditional_edges(
    "model",
    should_continue,
    ["tools", END]
)

builder.add_edge("tools", "model")

graph = builder.compile()

# -------------------------------
# Dummy Inputs (AUTO RUN)
# -------------------------------
test_inputs = [
    "My name is John, I am 30 years old and I have a sore throat and feel tired.",
    "I am Anna, 25, feeling dizzy and weak.",
    "Tom here, 40 years old, persistent cough for 3 weeks."
]

# -------------------------------
# Run Chatbot
# -------------------------------
if __name__ == "__main__":
    for i, user_input in enumerate(test_inputs):
        print("\n==============================")
        print(f"[CASE {i+1}] User Input:")
        print(user_input)

        result = graph.invoke({
    "messages": [
        SystemMessage(
            content=(
                "You are a medical assistant chatbot.\n"
                "Steps:\n"
                "1. Extract patient info (name, age, symptoms).\n"
                "2. Use tools if needed.\n"
                "3. Provide simple preliminary advice.\n"
                "4. Be concise and safe.\n"
                "5. Do NOT give diagnosis."
            )
        ),
        HumanMessage(content=user_input)
    ]
})


        print("\n[FINAL RESPONSE]")
        print(result["messages"][-1].content)