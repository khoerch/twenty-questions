from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import time

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    relevance: int
    isCorrect: bool

@app.post("/questions/evaluate", response_model=QuestionResponse)
async def evaluate_question(question: Question):
    if not question.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Simulate processing delay
    time.sleep(0.3)
    
    # This is a placeholder response - will be replaced with LLM logic later
    return {
        "answer": "YES" if random.random() > 0.5 else "NO",
        "relevance": random.randint(0, 100),
        "isCorrect": random.random() > 0.95  # 5% chance of being correct
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 