"""
src/app/api/schemas/auth.py

Pydantic request/response shapes for auth routes. These are transport
concerns - deliberately separate from the ORM models in infrastructure
and from any future domain object. What the wire accepts is allowed to
differ from what's stored.
"""
from uuid import UUID

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr