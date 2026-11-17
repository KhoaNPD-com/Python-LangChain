# README

## 1. Project Overview

This project implements an AI assistant using:

* OpenAI GPT-4o-mini (LLM)
* LangGraph (modern agent framework)
* LangChain tools integration

The assistant can:

* Answer general questions
* Fetch real-time weather information
* Retrieve latest web search results

---

## 2. Architecture

The system follows a tool-augmented agent design using LangGraph.

Components:

1. LLM (ChatOpenAI)
   * Responsible for reasoning and response generation
   * Supports tool calling via function binding
2. Tools
   * Weather tool using OpenWeatherMap API
   * Tavily search tool for web queries
3. LangGraph Workflow
   * StateGraph manages message flow
   * ToolNode executes tools
   * Routing function decides next step

---

## 3. Approach

Step 1: Setup API Access

API keys are provided directly in LLM initialization and environment variables.

Step 2: Define Tools

Two tools are implemented:

* get_weather(city)
  * Calls OpenWeatherMap API
  * Returns weather description
* TavilySearch
  * Performs web search
  * Returns concise results

Step 3: Bind Tools to LLM

The LLM is connected with tools using:

llm_with_tools = llm.bind_tools(tools)

This allows the model to decide when to call tools.

Step 4: Build LangGraph Agent

The agent is built using:

* chatbot node → calls LLM
* tool node → executes tools
* routing logic:
  * If tool call exists → go to tools
  * Otherwise → end

Step 5: Automated Conversation

A predefined list of user queries is used instead of input():

* Weather query
* News query
* General knowledge query
* Exit command

---

## 4. Execution Flow

1. User message is added to state
2. LLM generates response
3. If tool is required:
   * ToolNode executes tool
   * Result is returned to LLM
4. Final response is printed

---

## 5. Example Queries

What's the weather in Hanoi?

Tell me the latest news in AI

Who won the last World Cup

---

## 6. Challenges Faced

1. Deprecated API Usage

   Problem:
   create_react_agent is deprecated

Solution:
Replaced with:

* StateGraph
* ToolNode
* Custom routing logic

---

1. Tool Calling Not Triggered

   Problem:
   Model sometimes does not call tools

Solution:

* Improved tool descriptions
* Used bind_tools()

---

1. API Configuration Issues

   Problem:
   Errors due to missing API keys

Solution:

* Added explicit API key parameters
* Used consistent configuration

---

1. Dependency Issues

   Problem:
   Missing libraries

Solution:
pip install langchain-openai langchain-community langchain-tavily langgraph pyowm

---

## 7. Limitations

* Depends on external APIs
* Tool selection may not always be optimal (small model)
* Requires internet connection

---

## 8. Future Improvements

* Add memory persistence
* Add retry and logging system
* Improve prompt engineering
* Deploy as API (FastAPI)
* Add user interface (web app)

---

## 9. Requirements

Python 3.9+

Install dependencies:

pip install langchain-openai langchain-community langchain-tavily langgraph pyowm

---

## 10. Summary

This project demonstrates:

* Tool-based AI agent design
* LangGraph workflow orchestration
* Integration of external APIs with LLMs

The system is modular, extensible, and aligned with modern LangChain practices.
