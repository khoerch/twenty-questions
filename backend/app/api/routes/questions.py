from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.limiter import limiter
from app.api.models.question import Question, QuestionEvaluation
from app.services.llm_service import LLMService
from app.core.cache import ttl_cache
from app.database import get_db
from app.services.solution_service import SolutionService


router = APIRouter(prefix="/api/questions", tags=["questions"])

@router.post("/evaluate", response_model=QuestionEvaluation)
@limiter.limit("20/minute")
@limiter.limit("100/day")
@ttl_cache(namespace="question_evaluations", maxsize=100, ttl_seconds=86400)
async def evaluate_question(
    request: Request,
    question: Question,
    db: Session = Depends(get_db),
    llm_service: LLMService = Depends()
):
    solution_service = SolutionService(db, llm_service)
    solution = solution_service.get_current_solution()
    evaluation = await llm_service.evaluate_question(question.text, solution)
    
    return QuestionEvaluation(
        is_yes_no=evaluation.get("is_yes_no", False),
        answer=evaluation.get("answer") if evaluation.get("is_yes_no") else None,
        relevance=evaluation.get("relevance") if evaluation.get("is_yes_no") else None,
        is_correct=evaluation.get("is_correct") if evaluation.get("is_yes_no") else None
    ) 