
# README

## Overview

This project implements a **log classification pipeline** that automatically assigns a root cause category to unstructured logistics delivery and maintenance logs.

The system combines:

* A **rule-based keyword classifier** (fast, low-cost)
* An **LLM-based refinement layer (OpenAI)** for improved accuracy

---

## Objective

* Analyze free-text incident logs
* Classify them into predefined delay categories
* Reduce manual analysis effort
* Improve operational visibility

---

## Categories

```
[
 "Traffic",
 "Customer Issue",
 "Vehicle Issue",
 "Weather",
 "Sorting/Labeling Error",
 "Human Error",
 "Technical System Failure",
 "Other"
]
```

---

## Input Format

CSV file: `dataset.csv`

```
log_id,log_entry
1,Driver reported heavy traffic on highway
2,Customer not available at delivery address
...
```

---

## Output Format

CSV file: `classified_logs.csv`

```
log_id,log_entry,predicted_category
1,Driver reported heavy traffic on highway,Traffic
2,Customer not available at delivery address,Customer Issue
```

---

## How to Run

### 1. Install dependencies

```
pip install pandas openai python-dotenv
```

### 2. Set environment variables

Create `.env` file:

```
OPENAI_API_KEY=your_api_key
OPENAI_ENDPOINT=https://api.openai.com/v1
```

### 3. Run script

```
python app.py
```

---

## Pipeline Design

### Step 1: Preprocessing

* Lowercase text
* Remove whitespace

### Step 2: Keyword Classification

* Fast rule-based mapping
* Covers common patterns

### Step 3: LLM Refinement

* Applied only when keyword classifier returns `Other`
* Uses `gpt-4o-mini`
* Deterministic (`temperature=0`)

### Step 4: Output Generation

* Adds `predicted_category` column
* Saves results to CSV

---

## Key Design Choices

* Hybrid approach balances **speed + accuracy**
* Keyword layer reduces API cost
* LLM handles ambiguity and variations
* Deterministic outputs for consistency

---

## Difference from Retrieval-Based Pipelines

### This Approach (Classification Pipeline)

* Directly maps input text → predefined category
* No external knowledge base required
* Works purely on:
  * Rules (keywords)
  * Language model reasoning
* Best for:
  * Fixed label classification
  * Structured outputs
  * Operational automation (e.g., dashboards, reporting)

---

### Retrieval-Based Pipelines (RAG)

* First retrieves relevant documents (vector DB / search)
* Then uses LLM to generate answer based on retrieved context
* Characteristics:
  * Requires embeddings + storage
  * Depends on external knowledge sources
  * More complex architecture
* Best for:
  * Question answering
  * Knowledge-intensive tasks
  * Dynamic information lookup

---

### Key Difference

| Aspect      | Classification Pipeline | Retrieval Pipeline      |
| ----------- | ----------------------- | ----------------------- |
| Goal        | Assign category         | Generate answer         |
| Data Source | Input text only         | External knowledge base |
| Complexity  | Low                     | High                    |
| Latency     | Fast                    | Slower                  |
| Use Case    | Automated labeling      | Q&A, search             |

---

## When to Use This Approach

Use this pipeline when:

* You have **fixed categories**
* You need **structured outputs**
* You process **high-volume logs**
* You want **low latency and cost**

---

## Limitations

* Keyword rules may miss edge cases
* LLM adds cost if overused
* No contextual memory across logs

---

## Possible Improvements

* Add embedding-based similarity (no keywords)
* Batch LLM calls for performance
* Add evaluation metrics (accuracy, F1)
* Build API (FastAPI) or UI (Streamlit)

---

## Summary

This solution provides a **simple, scalable, and production-ready pipeline** for classifying logistics logs using a hybrid NLP + LLM approach, optimized for real-world operational use.
