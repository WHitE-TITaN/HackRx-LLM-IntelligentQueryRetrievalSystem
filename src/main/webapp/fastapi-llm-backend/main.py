from fastapi import FastAPI, Request, Header, HTTPException 
from pydantic import BaseModel
from typing import List, Dict
from module import docHandle
from module import vectorDbHandle
from module import authentication
import uvicorn

from typing import Optional

#gemini for response generation
from google.generativeai import GenerativeModel, configure
import os

app = FastAPI()
 
class Payload(BaseModel):
    documents: str        
    questions: list[str] 

@app.post("/hackrx/run")
async def process_data(request: Payload,
    authorization: Optional[str] = Header(None)):


    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.split(" ")[1]
    securityCheck = authentication.authenticate()
    if not securityCheck.varify_api_key(token):
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

    link = request.documents
    question = request.questions
    
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
    return {
            "answers": answerByLLM
            }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)