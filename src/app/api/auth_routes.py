"""
src/app/api/auth_routes.py

Real registration and login. Uses the DB session directly for now
(via get_db) rather than a repository - the application/use-case layer
that would normally sit between routes and persistence doesn't exist
yet (that's Phase 4). This is a deliberate, temporary shortcut, not a
final design - noted here so it isn't mistaken for the intended
long-term shape.
"""
import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.config import Settings, get_settings
from app.core.security import create_access_token, hash_password, verify_password
from app.infrastructure.db.base import get_db
from app.infrastructure.db.models import User
from app.api.deps import get_current_user

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


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)) -> User:
    existing = await db.execute(select(User).where(User.email == body.email))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(email=body.email, hashed_password=hash_password(body.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)

    logger.info("user_registered", user_id=str(user.id))
    return user


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if user is None or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token(user.id)
    logger.info("user_logged_in", user_id=str(user.id))
    return TokenResponse(access_token=token)

@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user