from fastapi import FastAPI
from pydantic import BaseModel
from .config import app
from .routes_links import APIs
from pepper.AI.engine import Engine  # your existing class


engine = Engine()

class ChatRequest(BaseModel):
    message: str

@app.post(APIs.CHAT)
def chat(req: ChatRequest):

    response = engine._generate(
        _identity="You are Pepper, a helpful school assistant.",
        prompt=req.message
    )

    return {
        "response": response
    }