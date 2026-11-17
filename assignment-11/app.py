# ==============================
# INSTALL
# pip install langchain-openai langchain-community langchain-tavily langgraph pyowm
# ==============================

import os
from typing import Annotated, TypedDict
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_tavily import TavilySearch

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from openai import OpenAI

# -----------------------------
# CONFIG
# -----------------------------
from dotenv import load_dotenv
load_dotenv()

# ==============================
# STEP 1: API KEYS
# ==============================

# os.environ["AZURE_OPENAI_ENDPOINT"] = "YOUR_ENDPOINT"
# os.environ["AZURE_OPENAI_API_KEY"] = "YOUR_API_KEY"
# os.environ["AZURE_DEPLOYMENT_NAME"] = "GPT-4o-mini"

os.environ["OPENWEATHERMAP_API_KEY"] = os.getenv('OPEN_WEATHER_API_KEY')
os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')

# ==============================
# STEP 2: TOOLS
# ==============================

weather = OpenWeatherMapAPIWrapper()

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    print(f"[Tool] Weather for: {city}")
    return weather.run(city)

tavily_tool = TavilySearch(max_results=1)

tools = [get_weather, tavily_tool]

# ==============================
# STEP 3: LLM
# ==============================

llm = ChatOpenAI(
    model=os.getenv('OPENAI_MODEL_GPT_4O'),
    temperature=0,
    api_key=os.getenv('OPENAI_GPT_4O_API_KEY'),
    base_url=os.getenv('OPENAI_ENDPOINT'),
)


llm_with_tools = llm.bind_tools(tools)

# ==============================
# STEP 4: STATE DEFINITION
# ==============================

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# ==============================
# STEP 5: NODES
# ==============================

def chatbot_node(state: AgentState):
    return {
        "messages": [llm_with_tools.invoke(state["messages"])]
    }

tool_node = ToolNode(tools)

# Decide whether to call tool or end
def route(state: AgentState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"
    return END

# ==============================
# STEP 6: GRAPH
# ==============================

graph = StateGraph(AgentState)

graph.add_node("chatbot", chatbot_node)
graph.add_node("tools", tool_node)

graph.set_entry_point("chatbot")

graph.add_conditional_edges(
    "chatbot",
    route,
)

graph.add_edge("tools", "chatbot")

app = graph.compile()

# ==============================
# STEP 7: AUTO INPUT
# ==============================

print("=== AI Assistant (New LangGraph) ===")

messages = []

mock_questions = [
    "What's the weather in Hanoi?",
    "Tell me the latest news in AI",
    "Who won the last World Cup?",
    "exit"
]

for q in mock_questions:
    print("\nUser:", q)

    if q.lower() == "exit":
        print("Assistant: Goodbye!")
        break

    messages.append({"role": "user", "content": q})

    response = app.invoke({"messages": messages})

    ai_msg = response["messages"][-1]
    messages.append(ai_msg)

    print("Assistant:", ai_msg.content)

print("\n=== Done ===")