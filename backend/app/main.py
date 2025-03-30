from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import logging
from app.core.limiter import limiter
from app.api.routes import questions, solutions, health
from app.database import init_db
from app.services.scheduler_service import SchedulerService
from app.services.llm_service import LLMService
from app.database import get_db


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="20 Questions API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(questions.router)
app.include_router(solutions.router)
app.include_router(health.router)

# Initialize scheduler
scheduler_service = SchedulerService()

# Initialize rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    init_db()
    logger.info("Database initialized")
    
    scheduler_service.start()
    llm_service = LLMService()
    scheduler_service.schedule_daily_solution_generation(get_db, llm_service)
    logger.info("Daily solution generation scheduled")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    if scheduler_service.scheduler.running:
        scheduler_service.scheduler.shutdown()
        logger.info("Scheduler shut down")

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 