from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict
from module import docHandle

app = FastAPI()

class Payload(BaseModel):
    name: str
    age: int

@app.post("/process")
async def process_data(payload: Payload):
    link = "{payload.documents}"
    key = "{payload.key}"
    question = "{payload.question}"

    file = docHandle.TextPullOut()
    text = file.extractText(link)

    greeting = f"Hello {payload.name}, you are {payload.age} years old!"
    is_adult = payload.age >= 18

    return {
        "message": greeting,
        "adult": is_adult,
        "length_of_name": len(payload.name)
    }


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)