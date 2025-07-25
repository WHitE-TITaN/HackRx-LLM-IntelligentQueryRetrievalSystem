from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    documents: List[str]  # base64 or plain text if already parsed

@app.post("/hackrx/run")
async def run_model(request: QueryRequest):
    # ✨ Do query parsing, semantic search, and decision making
    return {
        "success": True,
        "decision": "approved",
        "amount": "₹40,000",
        "justification": "Clause 3.2 states that knee surgeries are covered for policies > 2 months."
    }
