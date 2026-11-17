# Semantic Search using Azure OpenAI Embeddings

## 1. Embeddings Creation and Usage

In this project, product descriptions were transformed into numerical vectors (embeddings) using Azure OpenAI’s **`text-embedding-3-small`** model.

This endpoint using OpenAI with the same model on AI portal

### Process:

* Each product’s **title and short description** were combined into a single text input.
* The embedding API was called:

  **Python**

  **response = client.embeddings.create(**

  **    model="text-embedding-3-small",**

  **    input=texts**

  **)**

  Show more lines
* The output is a **dense vector representation** (typically 1536 dimensions).
* These embeddings were **stored in memory** for all products.

### Usage:

* When a user query is provided:
  * It is converted into an embedding using the same model.
* The query embedding is then compared with all product embeddings.
* The system returns the most semantically similar products.

---

## 2. Cosine Similarity for Ranking

To rank products, **cosine similarity** was used.

### Formula:

```
cosine_similarity(A, B) = (A · B) / (||A|| * ||B||)
```

### Implementation:

**Python**

**similarity = 1 - cosine(query_embedding, product_embedding)**

**``**

Show more lines

### Explanation:

* Measures the **angle between two vectors** instead of magnitude.
* Value range:
  * `1` → identical meaning
  * `0` → unrelated
  * `-1` → opposite meaning
* Works well for embeddings because:
  * Embeddings encode **semantic meaning**
  * Magnitude is less important than direction

### Ranking:

* Compute similarity for all products
* Sort in descending order
* Return **Top-N most similar items**

---

## 3. Challenges and Limitations

### ⚠️ Challenges

1. **API Configuration**
   * Requires correct setup of:
     * API key
     * Endpoint
     * Deployment name
   * Common errors: authentication issues, wrong deployment names
2. **Latency**
   * Embedding generation requires API calls
   * Can be slow for large datasets if not batched properly
3. **Data Quality**
   * Poor or very short descriptions lead to weak embeddings
   * Quality of results depends heavily on input text

---

### ⚠️ Limitations

1. **Scalability**
   * Current approach compares query with all products → **O(n)**
   * Not efficient for large datasets (10K+ items)
   * Solution: use vector databases (FAISS, Pinecone, Redis)
2. **No Filtering**
   * System only uses semantic similarity
   * Does not consider:
     * price range
     * categories
   * Could lead to irrelevant results in some contexts
3. **Embedding Cost**
   * API usage may incur cost for large-scale systems
4. **Semantic Ambiguity**
   * Model may interpret vague queries differently than expected
