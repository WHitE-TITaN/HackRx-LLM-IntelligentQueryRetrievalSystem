from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict
from module import docHandle
from module import vectorDbHandle

#gemini for response generation
from google.generativeai import GenerativeModel, configure
import os

app = FastAPI()
 
class Payload(BaseModel):
    documents: str  
    key: str         
    question: list[str] 

@app.post("/process")
async def process_data(payload: Payload):
    link = payload.documents
    key = payload.key
    question = payload.question
    
    #getting key from Enviroment Variables
    KEY_GEMINI = os.getenv("API_KEY_GeminiAi")
    if not KEY_GEMINI:
        return {"message": "❌ API Key for Gemini AI not found in environment variables"}
    configure(api_key = KEY_GEMINI)
    model = GenerativeModel("gemini-1.5-flash")


    #document handling and chunking
    file = docHandle.TextPullOut()
    file_id = os.path.splitext(os.path.basename(link))[0] 
    chunked_text = file.chunkedText(link)


    #create embedding and upload to vector db
    vector_db = vectorDbHandle.VectorDbHandle()
    await vector_db.createEmbedding(chunked_text, file_id)
    

    #chunk retreval and answer generation
    answerByLLM = []
    for i in range(0, len(question)):
        matched_chunks = vector_db.retreaveData(question[i])

        prompt = f"Answer the question based on the context provided.\n\nContext:\n"
        for chunk in matched_chunks:
            prompt += f"{chunk}\n\n"

        prompt += f"Question: {question[i]}"

        try:
            response = model.generate_content(prompt)
            answerByLLM.append(response.text)
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return {"message": "Error generating response", "error": str(e)}

    

    #to do the delete so every file data after all question request is processed.
    return {"message": "✅Data processed successfully", 
            "file_id": file_id,
            "chunks_uploaded": len(chunked_text),
            "ans": answerByLLM}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)