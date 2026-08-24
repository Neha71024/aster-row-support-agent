import os
import json
import numpy as np
from google import genai
from dotenv import load_dotenv
from src.ingest import ingest_knowledge_base

# Load environment variables (reads .env file)
load_dotenv()

# Initialize the Gemini API client
# It automatically picks up the GEMINI_API_KEY from environment variables
client = genai.Client()

def get_or_generate_embeddings(kb_dir: str, cache_path: str) -> list:
    """
    Checks if a cache of chunk embeddings exists. If yes, loads it.
    If not, reads files from the knowledge base, calls Gemini to get embeddings,
    and saves them to the cache path.
    """
    if os.path.exists(cache_path):
        print(f"[RAG] Loading embeddings from cache: {cache_path}")
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[RAG] Failed to load cache: {e}. Regenerating...")

    print("[RAG] Cache not found. Generating embeddings for the knowledge base...")
    raw_chunks = ingest_knowledge_base(kb_dir)
    embedded_chunks = []

    for i, chunk in enumerate(raw_chunks):
        print(f"[RAG] Embedding chunk {i+1}/{len(raw_chunks)}: {chunk.file_name} > {chunk.heading}")
        
        # We construct a rich text string combining title, heading, and body content for the embedding
        text_to_embed = f"Title: {chunk.title}\nSection: {chunk.heading}\n\n{chunk.content}"

        try:
            response = client.models.embed_content(
                model="gemini-embedding-2",
                contents=text_to_embed
            )
            
            # Extract the vector array of floats
            vector = response.embeddings[0].values
            
            chunk_dict = chunk.to_dict()
            chunk_dict["embedding"] = vector
            embedded_chunks.append(chunk_dict)

        except Exception as e:
            print(f"[RAG] Error embedding chunk {chunk.file_name} > {chunk.heading}: {e}")
            raise e

    # Save to json file
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(embedded_chunks, f, indent=2)
    print(f"[RAG] Cached {len(embedded_chunks)} embeddings successfully!")

    return embedded_chunks

def retrieve_relevant_chunks(query: str, embedded_chunks: list, limit: int = 5) -> list:
    """
    Converts the query into an embedding, computes cosine similarities,
    applies metadata score boosting, and returns the top matching chunks.
    """
    # 1. Embed the search query
    try:
        response = client.models.embed_content(
            model="gemini-embedding-2",
            contents=query
        )
        query_vector = np.array(response.embeddings[0].values)
    except Exception as e:
        print(f"[RAG] Error embedding search query: {e}")
        return []

    scored_chunks = []

    # 2. Compute similarity for each chunk
    for chunk in embedded_chunks:
        chunk_vector = np.array(chunk["embedding"])
        
        # Since vectors are unit normalized, dot product is identical to cosine similarity
        raw_score = float(np.dot(query_vector, chunk_vector))

        # 3. Apply Metadata Boosting
        status = chunk.get("status")
        authority = chunk.get("policy_authority")
        audience = chunk.get("audience")
        file_name = chunk.get("file_name")

        boost_factor = 1.0
        if status == "active" and authority == "official":
            boost_factor = 1.0  # Base rank for active and official policies
        elif status == "superseded":
            boost_factor = 0.85  # Mildly penalize outdated version
        elif authority == "none" or audience == "internal":
            boost_factor = 0.80  # Mildly penalize internal drafts and scratchpads



        final_score = raw_score * boost_factor

        scored_chunks.append({
            "chunk": chunk,
            "score": final_score,
            "raw_score": raw_score
        })

    # 4. Sort and return top chunks
    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    return scored_chunks[:limit]
