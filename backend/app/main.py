from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.api.routes import questions, solutions, health
from app.database import init_db
from app.services.scheduler_service import SchedulerService
from app.services.llm_service import LLMService
from app.database import get_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="20 Questions API")

# Enable CORS
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

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    # Initialize the database
    init_db()
    logger.info("Database initialized")
    
    # Start the scheduler
    scheduler_service.start()
    
    # Schedule the daily solution generation job
    llm_service = LLMService()
    scheduler_service.schedule_daily_solution_generation(get_db, llm_service)
    logger.info("Daily solution generation scheduled")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    # Shutdown the scheduler if it's running
    if scheduler_service.scheduler.running:
        scheduler_service.scheduler.shutdown()
        logger.info("Scheduler shut down")

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 