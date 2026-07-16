import chromadb

from embedding import generate_embedding

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="java_code"
)


def add_chunk(id, code, file):

    embedding = generate_embedding(code)

    collection.add(
        ids=[id],
        embeddings=[embedding.tolist()],
        documents=[code],
        metadatas=[
            {
                "file": file
            }
        ]
    )
    print(f"Stored chunk: {id}")
    print(f"Embedding dimensions: {len(embedding)}")


def retrieve(code):

    embedding = generate_embedding(code)

    result = collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=3
    )
    print("\nRetrieved documents:")

    for doc in result["documents"][0]:
        print("--------------------")
        print(doc[:200])

    return result["documents"][0]