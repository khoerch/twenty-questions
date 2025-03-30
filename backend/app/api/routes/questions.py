from fastapi import APIRouter, HTTPException
from app.api.models.question import Question, QuestionEvaluation
from app.services.llm_service import evaluate_question_with_llm
from app.config import DAILY_SOLUTION

router = APIRouter(prefix="/questions", tags=["questions"])

@router.post("/evaluate", response_model=QuestionEvaluation)
async def evaluate_question(question: Question):
    # Call LLM service to evaluate the question
    evaluation = await evaluate_question_with_llm(question.text, DAILY_SOLUTION)
    
    return QuestionEvaluation(
        is_yes_no=evaluation.get("is_yes_no", False),
        answer=evaluation.get("answer") if evaluation.get("is_yes_no") else None,
        relevance=evaluation.get("relevance") if evaluation.get("is_yes_no") else None,
        is_correct=evaluation.get("is_correct") if evaluation.get("is_yes_no") else None
    ) 