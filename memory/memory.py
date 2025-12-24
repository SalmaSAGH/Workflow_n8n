# memory.py
import os
import chromadb
from chromadb.config import Settings
from datetime import datetime

PERSIST_DIR = os.environ.get("CHROMA_DIR", "./chroma_data")

client = chromadb.Client(Settings(persist_directory=PERSIST_DIR))
collection = client.get_or_create_collection(name="customer_memory")

def add_memory(conversation_id: str, user_id: str, summary: str, embedding: list = None):
    collection.add(
        ids=[conversation_id],
        documents=[summary],
        metadatas=[{"user_id": user_id, "timestamp": datetime.utcnow().isoformat()}],
        embeddings=[embedding] if embedding else None
    )

def query_memory(query_text: str, n_results: int = 3):
    return collection.query(query_texts=[query_text], n_results=n_results)

if __name__ == "__main__":
    print("Collections:", client.list_collections())
