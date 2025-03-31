from fastapi import APIRouter, Depends, Request
from app.core.limiter import limiter
from app.api.models.question import Question, QuestionEvaluation
from app.core.config import DAILY_SOLUTION
from app.services.llm_service import LLMService
from app.core.cache import ttl_cache

router = APIRouter(prefix="/api/questions", tags=["questions"])

@router.post("/evaluate", response_model=QuestionEvaluation)
@limiter.limit("20/minute")
@limiter.limit("100/day")
@ttl_cache(namespace="question_evaluations", maxsize=100, ttl_seconds=86400)
async def evaluate_question(
    request: Request,
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