# memory_api.py - Assignment 3: Optimized Memory with Summarization
import os
import chromadb
from chromadb.config import Settings
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

# --- Setup ChromaDB ---
PERSIST_DIR = os.environ.get("CHROMA_DIR", "./chroma_data")
client = chromadb.Client(Settings(persist_directory=PERSIST_DIR))
collection = client.get_or_create_collection(name="customer_memory")

# --- FastAPI app ---
app = FastAPI()

# --- Models ---
class MemoryAddRequest(BaseModel):
    conversation_id: str
    user_id: str
    summary: str

class MemoryQueryRequest(BaseModel):
    query_text: str
    n_results: int = 3

# --- Assignment 3: Conversation Buffer ---
# Stocker temporairement les conversations avant de les résumer
conversation_buffer = {}

def optimize_summary(summaries: list) -> str:
    """
    Optimise plusieurs résumés en un seul résumé condensé.
    Simple concatenation avec limite de taille.
    """
    combined = " | ".join(summaries)
    # Limiter à 500 caractères max
    if len(combined) > 500:
        return combined[:497] + "..."
    return combined

# --- Endpoints ---
@app.post("/memory/add")
def add_memory(req: MemoryAddRequest):
    """Add memory with smart summarization"""
    user_id = req.user_id
    
    # Ajouter au buffer
    if user_id not in conversation_buffer:
        conversation_buffer[user_id] = []
    
    conversation_buffer[user_id].append(req.summary)
    
    # Si buffer > 3 conversations, optimiser
    if len(conversation_buffer[user_id]) >= 3:
        optimized = optimize_summary(conversation_buffer[user_id])
        
        # Stocker le résumé optimisé
        collection.add(
            ids=[f"{user_id}-optimized-{datetime.utcnow().timestamp()}"],
            documents=[optimized],
            metadatas=[{
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat(),
                "type": "optimized",
                "count": len(conversation_buffer[user_id])
            }]
        )
        
        # Vider le buffer
        conversation_buffer[user_id] = []
        
        return {
            "status": "added_optimized",
            "conversation_id": req.conversation_id,
            "optimized": True
        }
    else:
        # Stocker normalement
        collection.add(
            ids=[req.conversation_id],
            documents=[req.summary],
            metadatas=[{
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat(),
                "type": "single"
            }]
        )
        
        return {
            "status": "added",
            "conversation_id": req.conversation_id,
            "optimized": False
        }

@app.post("/memory/query")
def query_memory(req: MemoryQueryRequest):
    """Query with semantic search"""
    results = collection.query(
        query_texts=[req.query_text],
        n_results=req.n_results
    )
    return {
        "results": results,
        "count": len(results.get("ids", [[]])[0])
    }

@app.get("/memory/stats")
def get_stats():
    """Get memory statistics - Assignment 3"""
    return {
        "total_memories": collection.count(),
        "buffer_size": sum(len(v) for v in conversation_buffer.values()),
        "users_in_buffer": len(conversation_buffer)
    }