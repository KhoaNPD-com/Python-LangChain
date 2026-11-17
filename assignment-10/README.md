# Product Similarity Search using Pinecone + Azure OpenAI

## Overview

This script demonstrates semantic similarity search using embeddings.

## Features

- Uses Azure OpenAI embedding model (text-embedding-3-small)
- Stores vectors in Pinecone
- Retrieves top-3 similar products

## Steps

1. Initialize Azure OpenAI and Pinecone clients
2. Create/connect Pinecone index
3. Convert product titles to embeddings
4. Store vectors in Pinecone
5. Convert query to embedding
6. Perform similarity search

## Dataset

Embedded sample product list:

- Red T-Shirt
- Blue Jeans
- Black Leather Jacket
- White Sneakers
- Green Hoodie

## Run

pip install pinecone openai
python product_similarity.py

## Output

Displays top-3 similar products with similarity score

## Notes

- No manual input() is used (dummy query included)
- Logs can be saved via output redirection

## Output demonstration

[INFO] Uploaded product embeddings to Pinecone.

============================================
Query: clothing item suitable for summer
Top 3 similar products:

- Green Hoodie (score: 0.3169)
- Red T-Shirt (score: 0.3054)
- White Sneakers (score: 0.2843)

============================================
