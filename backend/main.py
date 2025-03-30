import os
import json
from typing import Optional
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("Warning: OPENAI_API_KEY environment variable not set")

client = openai.OpenAI(api_key=openai_api_key)

# For now, hardcode the daily solution
DAILY_SOLUTION = "Mariah Carey"

class Question(BaseModel):
    text: str

class QuestionEvaluation(BaseModel):
    is_yes_no: bool
    answer: Optional[str] = None
    relevance: Optional[int] = None
    is_correct: Optional[bool] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/questions/evaluate", response_model=QuestionEvaluation)
async def evaluate_question(question: Question):
    if not openai_api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    # Call OpenAI to evaluate the question
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": f"""
                You are an assistant for a 20 Questions style game. The secret answer is: {DAILY_SOLUTION}.
                
                Evaluate if the user's input is a valid yes/no question. If it is, determine:
                1. The correct answer (YES/NO)
                2. How relevant the question is to guessing the secret (0-100)
                3. If the question implies a specific guess, determine if that guess is correct
                
                Examples of relevance scores:
                - "Is it alive?" - 30 (somewhat relevant but very general)
                - "Is it a person?" - 60 (more specific and helpful)
                - "Is it an American president?" - 90 (very specific and directly related)
                
                Return your evaluation in JSON format with these fields:
                - is_yes_no: boolean indicating if input is a valid yes/no question
                - answer: "YES" or "NO" if applicable
                - relevance: integer from 0-100 if applicable
                - is_correct: boolean, true if the question implies the correct answer
                """},
                {"role": "user", "content": question.text}
            ]
        )
        
        # Parse the response
        result = response.choices[0].message.content
        evaluation = json.loads(result)
        
        return QuestionEvaluation(
            is_yes_no=evaluation.get("is_yes_no", False),
            answer=evaluation.get("answer") if evaluation.get("is_yes_no") else None,
            relevance=evaluation.get("relevance") if evaluation.get("is_yes_no") else None,
            is_correct=evaluation.get("is_correct") if evaluation.get("is_yes_no") else None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating question: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 