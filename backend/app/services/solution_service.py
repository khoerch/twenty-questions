from datetime import datetime, timezone
import logging
from typing import Optional
from firebase_admin import firestore
from firebase_admin.firestore import Client
from app.database import Solution
from app.services.llm_service import LLMService
from app.core.cache import ttl_cache


logger = logging.getLogger(__name__)

class SolutionService:
    def __init__(self, db: Client, llm_service: LLMService):
        self.db = db
        self.llm_service = llm_service
        self.solution_collection = "solutions"

    def get_solution_for_date(self, date: datetime.date) -> Optional[Solution]:
        """Get the solution for a specific date."""
        date_string = date.isoformat()
        solution_ref = self.db.collection(self.solution_collection).document(date_string).get()
        
        if solution_ref.exists:
            solution_data = solution_ref.to_dict()
            return Solution(**solution_data)
        return None

    @ttl_cache(namespace="solution_hints", maxsize=1, ttl_seconds=86400)  # Cache for 24 hours
    async def get_current_solution(self):
        """Get the solution for today."""
        today = datetime.now(timezone.utc).date()
        return self.get_solution_for_date(today)

    def create_solution(self, date: datetime.date, solution: str, hint: str, difficulty: int) -> Optional[Solution]:
        """Create a solution for a specific date."""
        if self.get_solution_for_date(date) is not None:
            logger.warning(f"Solution for date {date} already exists")
            return None
        
        date_string = date.isoformat()
        solution_obj = Solution(
            date=date_string,
            solution=solution,
            hint=hint,
            difficulty=difficulty
        )
        solution_data = solution_obj.model_dump()
        solution_data['created_at'] = firestore.SERVER_TIMESTAMP
        
        try:
            self.db.collection(self.solution_collection).document(date_string).set(solution_data)
            updated_solution_ref = self.db.collection(self.solution_collection).document(date_string).get()
            return Solution(**updated_solution_ref.to_dict())
        except Exception as e:
            logger.error(f"Error creating solution for date {date}: {e}")
            return None

    async def generate_solution_for_date(self, date: datetime.date) -> Optional[Solution]:
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
