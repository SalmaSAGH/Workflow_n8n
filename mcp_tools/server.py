# server.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from datetime import datetime

app = FastAPI()

class OrderRequest(BaseModel):
    order_id: str

class TicketRequest(BaseModel):
    user_id: str
    issue: str
    priority: str = "normal"

# Mock data; swap with your DB later.
ORDERS = {
    "ORD-123": {"status": "Shipped", "delivery_eta_days": 2},
    "ORD-456": {"status": "Processing", "delivery_eta_days": 5},
}

@app.post("/tools/get_order_status")
def get_order_status(req: OrderRequest) -> Dict:
    data = ORDERS.get(req.order_id, {"status": "Unknown", "delivery_eta_days": None})
    return {"order_id": req.order_id, **data}

# Assignment 2: Support Ticket Creation Tool
@app.post("/tools/create_support_ticket")
def create_support_ticket(req: TicketRequest) -> Dict:
    # In real life, write to DB or file; here we return a mock ticket id
    return {"ticket_id": "TCK-" + req.user_id[:3] + "-001", "status": "created", "priority": req.priority}


# Assignment 1: Sentiment Analysis Tool
class SentimentRequest(BaseModel):
    message: str

@app.post("/tools/analyze_sentiment")
def analyze_sentiment(req: SentimentRequest) -> Dict:
    # Simple keyword-based sentiment (pas besoin de LLM complexe)
    message_lower = req.message.lower()
    
    negative_words = ["bad", "terrible", "angry", "hate", "worst", "disappointed", "unacceptable"]
    positive_words = ["good", "great", "love", "excellent", "happy", "thank", "perfect"]
    
    neg_count = sum(1 for word in negative_words if word in message_lower)
    pos_count = sum(1 for word in positive_words if word in message_lower)
    
    if neg_count > pos_count:
        sentiment = "negative"
        priority = "high"
    elif pos_count > neg_count:
        sentiment = "positive"
        priority = "normal"
    else:
        sentiment = "neutral"
        priority = "normal"
    
    return {
        "sentiment": sentiment,
        "priority": priority,
        "confidence": max(neg_count, pos_count) / (len(message_lower.split()) + 1)
    }