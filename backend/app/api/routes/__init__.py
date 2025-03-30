from fastapi import APIRouter
from app.api.routes import health, questions

router = APIRouter()
router.include_router(health.router)
router.include_router(questions.router) 