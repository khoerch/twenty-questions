import logging
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.limiter import limiter
from app.api.models.question import Question, QuestionEvaluation
from app.services.llm_service import LLMService
from app.database import get_db
from app.services.solution_service import SolutionService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/questions", tags=["questions"])

@router.post("/evaluate", response_model=QuestionEvaluation)
@limiter.limit("20/minute")
@limiter.limit("100/day")
async def evaluate_question(
    request: Request,
    question: Question,
    db: Session = Depends(get_db),
    llm_service: LLMService = Depends()
):
    solution_service = SolutionService(db, llm_service)
    solution_details = await solution_service.get_current_solution()
    logger.info(f"Evaluating question: {question.text} against solution: {solution_details.solution}")
    evaluation = await llm_service.evaluate_question(question.text, solution_details.solution)
    
    return QuestionEvaluation(
        is_yes_no=evaluation.get("is_yes_no", False),
        answer=evaluation.get("answer") if evaluation.get("is_yes_no") else None,
        relevance=evaluation.get("relevance") if evaluation.get("is_yes_no") else None,
        is_correct=evaluation.get("is_correct") if evaluation.get("is_yes_no") else None
    ) 