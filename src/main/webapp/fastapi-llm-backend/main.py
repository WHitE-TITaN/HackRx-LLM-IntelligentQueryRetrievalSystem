import gc
from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from module import docHandle, vectorDbHandle, authentication
from google.generativeai import GenerativeModel, configure
import os, shutil
import psutil

app = FastAPI()

class Payload(BaseModel):
    documents: str        
    questions: list[str] 


#to free log the memory usage
def log_memory_usage(label=""):
    process = psutil.Process(os.getpid())
    mem_mb = process.memory_info().rss / 1024 ** 2  # in MB
    print(f"[MEMORY] {label}: {mem_mb:.2f} MB")
    return mem_mb


@app.post("/hackrx/run")
async def process_data(request: Payload, authorization: Optional[str] = Header(None)):
    mem_before = log_memory_usage("Before processing")
    
    file = None
    chunked_text = None
    vector_db = None
    matched_chunks = None
    prompt = None
    answerByLLM = []
    temp_file_path = None  # If you store downloaded files
    
    try:
        # Auth check
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unauthorized")
        token = authorization.split(" ")[1]
        securityCheck = authentication.Authenticate(os.getenv("API_KEY_MongoDb"))
        if not securityCheck.verify_api_key(token):
            raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

        link = request.documents
        question = request.questions
        
        # Gemini setup
        KEY_GEMINI = os.getenv("API_KEY_GeminiAi")
        if not KEY_GEMINI:
            return {"message": "❌ API Key for Gemini AI not found"}
        configure(api_key=KEY_GEMINI)
        model = GenerativeModel("gemini-1.5-flash")

        # Document handling
        file = docHandle.TextPullOut()
        file_id = os.path.splitext(os.path.basename(link))[0]
        chunked_text = file.chunkedText(link)
        # temp_file_path = file.get_temp_path()  # if applicable

        # Vector DB
        vector_db = vectorDbHandle.VectorDbHandle()
        await vector_db.createEmbedding(chunked_text, file_id)
        
        # Question answering
        for q in question:
            matched_chunks = vector_db.retreaveData(q)
            prompt = "Answer the question based on the context provided.\n\nContext:\n"
            for chunk in matched_chunks:
                prompt += f"{chunk}\n\n"
            prompt += f"Question: {q}"
            try:
                response = model.generate_content(prompt)
                answerByLLM.append(response.text)
            except Exception as e:
                return {"message": "Error generating response", "error": str(e)}

        return {"answers": answerByLLM}

    finally:
        # Close custom objects if they have cleanup methods
        if hasattr(file, "close"): file.close()
        if hasattr(vector_db, "close"): vector_db.close()
        
        # Delete large variables
        del file, chunked_text, vector_db, matched_chunks, prompt, answerByLLM
        
        # Remove temp files if applicable
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path) if os.path.isfile(temp_file_path) else shutil.rmtree(temp_file_path)
            except Exception as e:
                print(f"⚠️ Error deleting temp file: {e}")
        
        # Force GC
        gc.collect()
        mem_after = log_memory_usage("After cleanup")
        print(f"[MEMORY] Freed: {mem_before - mem_after:.2f} MB")





if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))