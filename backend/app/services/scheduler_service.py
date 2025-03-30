from datetime import datetime, timedelta, timezone
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from app.services.solution_service import SolutionService
from app.database import get_db
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        
    def start(self):
        """Start the scheduler."""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduler started")
            
    def schedule_daily_solution_generation(self, db_session_factory, llm_service: LLMService):
        """Schedule the daily solution generation job."""
        # Run at midnight UTC every day
        self.scheduler.add_job(
            self._generate_daily_solution,
            CronTrigger(hour=0, minute=0),
            id="daily_solution_generation",
            replace_existing=True,
            args=[db_session_factory, llm_service]
        )
        logger.info("Daily solution generation job scheduled")
        
        # Also generate a solution for today if it doesn't exist yet
        self.scheduler.add_job(
            self._generate_daily_solution,
            id="initial_solution_generation",
            args=[db_session_factory, llm_service]
        )
        
    async def _generate_daily_solution(self, db_session_factory, llm_service: LLMService):
        """Generate a solution for today."""
        try:
            db = next(db_session_factory())
            solution_service = SolutionService(db, llm_service)
            today = datetime.now(timezone.utc).date()
            
            solution = await solution_service.generate_solution_for_date(today)
            if solution:
                logger.info(f"Generated solution for {today}: {solution.solution}")
            else:
                logger.warning(f"Failed to generate solution for {today}")
        except Exception as e:
            logger.error(f"Error generating daily solution: {e}") 