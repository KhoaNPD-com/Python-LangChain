import os
import numpy as np
from scipy.spatial.distance import cosine
import openai
from openai import OpenAI

# -----------------------------
# CONFIG
# -----------------------------
from dotenv import load_dotenv
load_dotenv()

# -----------------------
# Azure OpenAI Setup
# -----------------------
client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT")
)

EMBED_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

# -----------------------
# Sample Dataset
# -----------------------
products = [
    {
        "title": "Classic Blue Jeans",
        "short_description": "Comfortable blue denim jeans with a relaxed fit.",
        "price": 49.99,
        "category": "Jeans"
    },
    {
        "title": "Red Hoodie",
        "short_description": "Cozy red hoodie made from organic cotton.",
        "price": 39.99,
        "category": "Hoodies"
    },
    {
        "title": "Black Leather Jacket",
        "short_description": "Stylish black leather jacket for a modern look.",
        "price": 129.99,
        "category": "Jackets"
    },
    {
        "title": "White T-Shirt",
        "short_description": "Basic white t-shirt made from soft cotton fabric.",
        "price": 19.99,
        "category": "T-Shirts"
    },
    {
        "title": "Running Sneakers",
        "short_description": "Lightweight running shoes designed for comfort and speed.",
        "price": 79.99,
        "category": "Shoes"
    }
]

# -----------------------
# Create Embeddings
# -----------------------
def create_embeddings(texts):
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=texts
    )
    return [item.embedding for item in response.data]

# Add embeddings to products
product_texts = [
    f"{p['title']}. {p['short_description']}" for p in products
]
product_embeddings = create_embeddings(product_texts)

# -----------------------
# Semantic Search
# -----------------------
def semantic_search(query, top_n=3):
    # Embed query
    query_embedding = create_embeddings([query])[0]

    # Compute similarities
    similarities = []
    for idx, prod_emb in enumerate(product_embeddings):
        sim = 1 - cosine(query_embedding, prod_emb)  # cosine similarity
        similarities.append((sim, products[idx]))

    # Sort descending
    similarities.sort(key=lambda x: x[0], reverse=True)

    return similarities[:top_n]

# -----------------------
# Demo (auto input - no input())
# -----------------------
queries = [
    "comfortable denim pants",
    "warm sweatshirt for winter",
    "lightweight shoes for running"
]

for q in queries:
    print(f"\n🔎 Query: {q}")
    results = semantic_search(q, top_n=3)

    for score, product in results:
        print(f"  ✅ {product['title']} (Score: {score:.4f})")