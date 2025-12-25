# Multi-Agent Customer Support System

Automated customer support using n8n, Ollama, MCP, and Vector Memory.

## Overview

Multi-agent AI system for e-commerce customer support handling:
- Order tracking
- Refund requests  
- Product issues
- General FAQ
- Escalations

## Architecture

```
Streamlit GUI → n8n Workflow → Ollama LLM
                            → MCP Tools (port 3333)
                            → Memory API (port 3334)
```

## Installation

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:1b

# 2. Install n8n
npm install -g n8n

# 3. Python environment
python -m venv venv
source venv/bin/activate
pip install streamlit chromadb fastapi uvicorn requests pydantic
```

## Usage

Start 4 terminals:

```bash
# Terminal 1: MCP Server
uvicorn server:app --port 3333 --reload

# Terminal 2: Memory API
uvicorn memory_api:app --port 3334 --reload

# Terminal 3: n8n
n8n start

# Terminal 4: Streamlit
streamlit run app.py
```

Access: http://localhost:8501

## Assignments

### Assignment 1: Sentiment Analysis

**Test via GUI**: Ask negative questions in Streamlit
```
"This product is terrible and I'm very angry!"
"I'm extremely disappointed with your service!"
```
Result: Automatic escalation due to negative sentiment detection

**Test via API**:
```bash
curl -X POST http://localhost:3333/tools/analyze_sentiment \
  -H "Content-Type: application/json" \
  -d '{"message": "This is terrible!"}'
```

### Assignment 2: Support Ticket

**Test via GUI**: Ask for escalation
```
"I need to speak with a manager immediately!"
"This is unacceptable, escalate this now!"
```
Result: Ticket created with ID (TCK-XXX)

**Test via API**:
```bash
curl -X POST http://localhost:3333/tools/create_support_ticket \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user1", "issue": "Problem", "priority": "high"}'
```

### Assignment 3: Memory Optimization

**Test via GUI**: Send 3+ messages in conversation
```
Message 1: "Where is my order ORD-123?"
Message 2: "I also need a refund"
Message 3: "What is your return policy?"
```
Result: Conversations automatically compressed into optimized memory

**Test via API**:
```bash
# Check stats
curl http://localhost:3334/memory/stats

# Add 3 conversations to trigger optimization
curl -X POST http://localhost:3334/memory/add \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": "conv1", "user_id": "user1", "summary": "Test"}'
```

## Project Structure

```
├── app.py                # Streamlit GUI
├── server.py            # MCP Tools
├── memory_api.py        # Memory API
├── My workflow 2.json   # n8n workflow
└── README.md
```



## Agents

- Intent Classifier: Detects user intent
- Order Agent: Handles order status
- Refund Agent: Processes refunds
- FAQ Agent: Answers policies
- Escalation Agent: Creates tickets
- Memory Agent: Stores conversations

## License

MIT
