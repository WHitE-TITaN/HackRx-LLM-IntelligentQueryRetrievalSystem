from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict
from module import docHandle
from module import vectorDbHandle
import os

app = FastAPI()

class Payload(BaseModel):
    documents: str  
    key: str         
    question: str 

@app.post("/process")
async def process_data(payload: Payload):
    link = payload.documents
    key = payload.key
    question = payload.question

    file = docHandle.TextPullOut()
    file_id = os.path.splitext(os.path.basename(link))[0] 
    chunked_text = file.chunkedText(link)

    vector_db = vectorDbHandle.VectorDbHandle()
    vector_db.createEmbedding(chunked_text, file_id)


    #to do the delete so every file data after all question request is processed.
    return {"message": "✅Data processed successfully", 
            "file_id": file_id,
             "chunks_uploaded": len(chunked_text)}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)