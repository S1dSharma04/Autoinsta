"""
src/app/api/auth_routes.py

Stub auth routes. Real OAuth2/JWT logic arrives in Checkpoint 2.2.
"""
from fastapi import APIRouter, Depends
import structlog

from app.config import Settings, get_settings

router = APIRouter()
logger = structlog.get_logger(__name__)


@router.get("/ping")
async def ping() -> dict:
    logger.info("auth_ping_called")
    return {"auth": "ok"}


@router.get("/config-check")
async def config_check(settings: Settings = Depends(get_settings)) -> dict:
    return {
        "environment": settings.environment,
        "jwt_algorithm": settings.jwt_algorithm,
    }