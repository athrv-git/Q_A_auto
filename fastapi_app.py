# fastapi_app.py

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/generate")
async def generate_answer(request: QuestionRequest):
    # You can replace this logic with a real model like OpenAI, Gemini, etc.
    question = request.question
    return {"answer": f"This is an auto-generated answer for: {question[:30]}..."}
