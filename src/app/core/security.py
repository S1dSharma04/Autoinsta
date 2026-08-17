"""
src/app/core/security.py

Password hashing and JWT encode/decode primitives. Lives in `core`
(framework-agnostic, importable by any layer) per the roadmap's folder
design - not `infrastructure`, because there's no external service
here, just pure cryptographic functions.
"""
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from passlib.context import CryptContext

from app.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: UUID) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> UUID:
    """
    Raises jwt.PyJWTError (or a subclass) if the token is invalid,
    tampered with, or expired. Callers must catch this.
    """
    settings = get_settings()
    payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    return UUID(payload["sub"])




from cryptography.fernet import Fernet, InvalidToken


def get_fernet() -> Fernet:
    settings = get_settings()
    return Fernet(settings.fernet_key.encode())


def encrypt_secret(plaintext: str) -> bytes:
    return get_fernet().encrypt(plaintext.encode())


def decrypt_secret(ciphertext: bytes) -> str:
    """
    Raises cryptography.fernet.InvalidToken if the ciphertext is corrupt,
    tampered with, or was encrypted with a different key. Callers must
    handle this - it means the credential is unreadable, not that it's
    merely wrong.
    """
    return get_fernet().decrypt(ciphertext).decode()