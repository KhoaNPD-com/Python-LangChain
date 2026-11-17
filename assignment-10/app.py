# ============================================
# Product Similarity Search using Pinecone + Azure OpenAI
# ============================================

# pip install pinecone openai

import os
from pinecone import Pinecone, ServerlessSpec
from openai import AzureOpenAI, OpenAI

# -----------------------------
# CONFIG
# -----------------------------
from dotenv import load_dotenv
load_dotenv()

# ============================================
# Step 0: Set environment variables (FILL YOUR KEYS)
# ============================================
os.environ["AZURE_DEPLOYMENT_NAME"] = "text-embedding-3-small"

os.environ["PINECONE_API_KEY"] = os.getenv('PINECONE_API_KEY')

# ============================================
# Step 1: Initialize clients
# ============================================
client = OpenAI(
 api_key=os.getenv('AZURE_OPENAI_API_KEY'),
 base_url=os.getenv('OPENAI_ENDPOINT'),
)

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# ============================================
# Step 2: Create or connect index
# ============================================
index_name = "product-similarity-index"

existing_indexes = [index["name"] for index in pc.list_indexes()]

if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=1536,  # embedding dimension
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

# ============================================
# Step 3: Sample dataset (embedded)
# ============================================
products = [
 {"id": "prod1", "title": "Red T-Shirt", "description": "Comfortable cotton t-shirt in bright red"},
 {"id": "prod2", "title": "Blue Jeans", "description": "Stylish denim jeans with relaxed fit"},
 {"id": "prod3", "title": "Black Leather Jacket", "description": "Genuine leather jacket with classic style"},
 {"id": "prod4", "title": "White Sneakers", "description": "Comfortable sneakers perfect for daily wear"}, 
 {"id": "prod5", "title": "Green Hoodie", "description": "Warm hoodie made of organic cotton"},
]

# ============================================
# Step 4: Embedding function
# ============================================
def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model=os.getenv("AZURE_DEPLOYMENT_NAME")
    )
    return response.data[0].embedding


# ============================================
# Step 5: Upsert vectors
# ============================================

vectors = []

for product in products:
    emb = get_embedding(product["title"])
    
    vectors.append({
        "id": product["id"],
        "values": emb
    })

index.upsert(vectors=vectors)

print("[INFO] Uploaded product embeddings to Pinecone.")

# ============================================
# Step 6: Dummy query (NO input())
# ============================================
query = "clothing item suitable for summer"
query_embedding = get_embedding(query)

# ============================================
# Step 7: Query Pinecone
# ============================================
top_k = 3

results = index.query(
    vector=query_embedding,
    top_k=top_k,
    include_metadata=False
)

# ============================================
# Step 8: Print results
# ============================================
print("\n============================================")
print(f"Query: {query}")
print(f"Top {top_k} similar products:\n")

for match in results.matches:
    product_id = match.id
    score = match.score

    product = next(p for p in products if p["id"] == product_id)

    print(f"- {product['title']} (score: {score:.4f})")

print("============================================")