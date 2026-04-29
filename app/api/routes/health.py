from fastapi import APIRouter
from typing import Dict

router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/health", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "banyu-guide-ml-service",
        "version": "1.0.0"
    }
