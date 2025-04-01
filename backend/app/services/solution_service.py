from datetime import datetime, timedelta, timezone
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import Solution
from app.services.llm_service import LLMService
from app.core.cache import ttl_cache
logger = logging.getLogger(__name__)

class SolutionService:
    def __init__(self, db: Session, llm_service: LLMService):
        self.db = db
        self.llm_service = llm_service

    def get_solution_for_date(self, date: datetime.date):
        """Get the solution for a specific date."""
        solution = self.db.query(Solution).filter(Solution.date == date).first()
        return solution

    @ttl_cache(namespace="solution_hints", maxsize=1, ttl_seconds=86400)  # Cache for 24 hours
    async def get_current_solution(self):
        """Get the solution for today."""
        today = datetime.now(timezone.utc).date()
        return self.get_solution_for_date(today)

    def create_solution(self, date: datetime.date, solution: str, hint: str, difficulty: int):
        """Create a solution for a specific date."""
        db_solution = Solution(
            date=date,
            solution=solution,
            hint=hint,
            difficulty=difficulty
        )
        self.db.add(db_solution)
        try:
            self.db.commit()
            self.db.refresh(db_solution)
            return db_solution
        except IntegrityError:
            self.db.rollback()
            logger.warning(f"Solution for date {date} already exists")
            return None

    async def generate_solution_for_date(self, date: datetime.date):
        """Generate a solution for a specific date if one doesn't exist."""
        existing_solution = self.get_solution_for_date(date)
        if existing_solution:
            logger.info(f"Solution for {date} already exists")
            return existing_solution

        day_of_week = date.weekday()
        difficulty = day_of_week + 1  # 1-7 scale
        solution_data = await self.llm_service.generate_solution(difficulty)
        
        return self.create_solution(
            date=date,
            solution=solution_data["solution"],
            hint=solution_data["hint"],
            difficulty=difficulty
        )
