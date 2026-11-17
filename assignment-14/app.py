# ============================================
# RAG Chatbot for Walmart Retail Support
# ============================================

import os
from typing import TypedDict, Optional, List
from langchain_openai import AzureOpenAIEmbeddings, ChatOpenAI, OpenAIEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph

# ============================================
# Step 0: Environment Setup (Set your keys)
# ============================================
# -----------------------------
# CONFIG
# -----------------------------
from dotenv import load_dotenv
load_dotenv()

# ============================================
# Step 1: Walmart Documents (15 entries)
# ============================================

docs = [
    Document(page_content="Walmart customers may return electronics within 30 days with a receipt and original packaging."),
    Document(page_content="Grocery items at Walmart can be returned within 90 days with proof of purchase, except perishable products."),
    Document(page_content="OWalmart offers a 1-year warranty on most electronics and appliances. See product details for exceptions."),
    Document(page_content="Walmart Plus members get free shipping with no minimum order amount."),
    Document(page_content="Prescription medications purchased at Walmart are not eligible for return or exchange."),
    Document(page_content="Open-box items are eligible for return at Walmart within the standard return period, but must include all original accessories"),
    Document(page_content="If a Walmart customer does not have a receipt, most returns are eligible for store credit with valid photo identification."),
    Document(page_content="Walmart allows price matching for identical items found on Walmart.com and local competitor ads."),
    Document(page_content="Walmart Vision Center purchases may be returned or exchanged within 60 days with a receipt."),
    Document(page_content="Returns on cell phones at Walmart require the device to be unlocked and all personal data erased."),
    Document(page_content="Receipts are required for cash refunds; otherwise store credit is issued."),
    Document(page_content="Walmart gift cards cannot be redeemed for cash except where required by law."),
    Document(page_content="Seasonal merchandise at Walmart (e.g., holiday decorations) may have modified return windows, see in-store signage"),
    Document(page_content="Bicycles purchased at Walmart can be returned within 90 days if not used outdoors and with all accessories present."),
    Document(page_content="For online Walmart orders, customers can return items in store or by mail using the prepaid label."),
    Document(page_content="Walmart reserves the right to deny returns suspected of fraud or abuse.")
]

# ============================================
# Step 2: State Definition
# ============================================

class RAGState(TypedDict):
    question: str
    context: Optional[str]
    answer: Optional[str]

# ============================================
# Step 3: Embeddings & Vector Store
# ============================================

embeddings = OpenAIEmbeddings(
    base_url=os.getenv("OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
    # api_version="2024-07-01-preview"
)

vectorstore = FAISS.from_documents(
    docs,
    embeddings,
    docstore=InMemoryDocstore({str(i): doc for i, doc in enumerate(docs)})
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# ============================================
# Step 4: LLM Setup
# ============================================

llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_ENDPOINT"),
    api_key=os.getenv("OPENAI_GPT_4O_API_KEY"),
    model=os.getenv("OPENAI_MODEL_GPT_4O"),
    # api_version="2024-07-01-preview",
    temperature=0
    )

# ============================================
# Step 5: Prompt Template
# ============================================

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a Walmart support assistant. Use ONLY the provided context. "
     "Give clear and helpful answers. Cite relevant policy briefly."),
    ("human", "Context:\n{context}\n\nQuestion: {question}")
])

# ============================================
# Step 6: Nodes
# ============================================

def retrieve_node(state: RAGState) -> RAGState:
    retrieved_docs = retriever.invoke(state["question"])
    context = "\n".join(doc.page_content for doc in retrieved_docs)
    return {**state, "context": context}

def generate_node(state: RAGState) -> RAGState:
    formatted = prompt.format(
        context=state["context"],
        question=state["question"]
    )
    response = llm.invoke(formatted)
    return {**state, "answer": response.content}

# ============================================
# Step 7: Graph
# ============================================

builder = StateGraph(RAGState)
builder.add_node("retrieve", retrieve_node)
builder.add_node("generate", generate_node)

builder.set_entry_point("retrieve")
builder.add_edge("retrieve", "generate")
builder.set_finish_point("generate")

rag_graph = builder.compile()

# ============================================
# Step 8: Dummy Inputs (Auto-run)
# ============================================

questions = [
    "Can I return a Walmart bicycle if I've ridden it?",
    "What is the return period for electronics like laptops?",
    "Can I return clothes after trying them on?"
]

# ============================================
# Step 9: Run Demo
# ============================================

if __name__ == "__main__":
    for q in questions:
        print("=" * 60)
        print("QUESTION:", q)

        result = rag_graph.invoke({"question": q})

        print("\nRetrieved Context:\n", result["context"])
        print("\nGenerated Answer:\n", result["answer"])