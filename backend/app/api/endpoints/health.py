from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("/")
def health_check():
    """
    Check whether the API is running.
    """
    return {
        "status": "healthy",
        "application": "Enterprise AI Knowledge Assistant",
        "version": "1.0.0",
        "timestamp": datetime.now()
    }