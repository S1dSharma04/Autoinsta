"""
src/app/api/auth_routes.py

Stub auth routes. Real OAuth2/JWT logic arrives in Checkpoint 2.2.
"""
from fastapi import APIRouter, Depends

from app.config import Settings, get_settings

router = APIRouter()


@router.get("/ping")
async def ping() -> dict:
    return {"auth": "ok"}


@router.get("/config-check")
async def config_check(settings: Settings = Depends(get_settings)) -> dict:
    """
    Proves DI actually works: this route never calls get_settings() itself
    at the top of the file. FastAPI sees the Depends(get_settings) default,
    calls get_settings() for us, and hands the result in as `settings`.
    """
    return {
        "environment": settings.environment,
        "jwt_algorithm": settings.jwt_algorithm,
    }