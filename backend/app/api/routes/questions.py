from fastapi import APIRouter, HTTPException, Depends
from app.api.models.question import Question, QuestionEvaluation
from app.config import DAILY_SOLUTION
from app.services.llm_service import LLMService

router = APIRouter(prefix="/api/questions", tags=["questions"])

@router.post("/evaluate", response_model=QuestionEvaluation)
async def evaluate_question(
    question: Question,
    llm_service: LLMService = Depends()
):
    evaluation = await llm_service.evaluate_question(question.text, DAILY_SOLUTION)
    
    return QuestionEvaluation(
        is_yes_no=evaluation.get("is_yes_no", False),
        answer=evaluation.get("answer") if evaluation.get("is_yes_no") else None,
        relevance=evaluation.get("relevance") if evaluation.get("is_yes_no") else None,
        is_correct=evaluation.get("is_correct") if evaluation.get("is_yes_no") else None
    ) 