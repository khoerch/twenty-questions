from fastapi import APIRouter, Request
from app.core.limiter import limiter
from app.core.cache import reset_cache

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/clear-cache")
@limiter.limit("5/minute")
async def clear_cache_endpoint(request: Request, namespace: str = None):
    result = reset_cache(namespace)
    return {"message": result}