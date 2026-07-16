import chromadb
from embedding import generate_embedding

client = chromadb.Client()
collection = client.get_or_create_collection(name="java_code")

def add_chunk(id, code, file):
    embedding = generate_embedding(code)
    collection.add(
        ids=[id],
        embeddings=[embedding.tolist()],
        documents=[code],
        metadatas=[{"file": file}]
    )
    print(f"Stored chunk: {id} | Vector Dimension: {len(embedding)}")

def retrieve(code, exclude_file=None):
    embedding = generate_embedding(code)
    
    # Configure metadata filters to block self-matching
    where_clause = {"file": {"$ne": exclude_file}} if exclude_file else None

    result = collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=3,
        where=where_clause
    )
    
    # Safety checkout in case database yields no entries
    if not result or not result.get("documents"):
        return []
        
    return result["documents"][0]
