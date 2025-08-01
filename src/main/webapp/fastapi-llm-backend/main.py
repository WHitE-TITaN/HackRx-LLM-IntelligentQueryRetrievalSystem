from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

class Payload(BaseModel):
    name: str
    age: int

@app.post("/process")
async def process_data(payload: Payload):
    greeting = f"Hello {payload.name}, you are {payload.age} years old!"
    is_adult = payload.age >= 18

    return {
        "message": greeting,
        "adult": is_adult,
        "length_of_name": len(payload.name)
    }


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)