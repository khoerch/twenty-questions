from fastapi import APIRouter
from app.api.routes import health, questions, solutions, admin

router = APIRouter()
router.include_router(health.router)
router.include_router(questions.router) 
router.include_router(solutions.router)
router.include_router(admin.router)