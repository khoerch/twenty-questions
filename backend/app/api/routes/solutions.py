from datetime import datetime, date, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from firebase_admin.firestore import Client
from app.core.limiter import limiter
from app.database import get_db, Solution
from app.services.solution_service import SolutionService
from app.services.llm_service import LLMService
from app.api.models.solution import SolutionCreateRequest, SolutionFullResponse, SolutionHintResponse

router = APIRouter(prefix="/api/solutions", tags=["solutions"])


@router.get("/current/hint", response_model=SolutionHintResponse)
@limiter.limit("20/minute")
@limiter.limit("100/day")
async def get_current_solution_hint(
    request: Request,
    db: Client = Depends(get_db),
    llm_service: LLMService = Depends()
):
    """Get the current day's solution hint."""
    solution_service = SolutionService(db, llm_service)
    solution = await solution_service.get_current_solution()
    
    if not solution:
        solution = solution_service.generate_solution_for_date(datetime.now(timezone.utc).date())
        
    if not solution:
        raise HTTPException(status_code=404, detail="No solution found for today")
        
    return solution

@router.post("/future", response_model=SolutionFullResponse)
@limiter.limit("10/day")
async def create_future_solution(
    request: Request,
    solution_request: SolutionCreateRequest,
    db: Client = Depends(get_db),
    llm_service: LLMService = Depends()
):
    """Create a solution for a future date."""
    solution_service = SolutionService(db, llm_service)
    
    if solution_request.date <= datetime.now(timezone.utc).date():
        raise HTTPException(status_code=400, detail="Date must be in the future")
    
    existing_solution = solution_service.get_solution_for_date(solution_request.date)
    if existing_solution:
        raise HTTPException(status_code=400, detail=f"Solution already exists for {solution_request.date}")
    
    if solution_request.solution and solution_request.hint:
        day_of_week = solution_request.date.weekday()
        difficulty = day_of_week + 1
        
        solution = solution_service.create_solution(
            date=solution_request.date,
            solution=solution_request.solution,
            hint=solution_request.hint,
            difficulty=difficulty
        )
    else:
        solution = solution_service.generate_solution_for_date(solution_request.date)
    
    if not solution:
        raise HTTPException(status_code=500, detail="Failed to create solution")
        
    return solution