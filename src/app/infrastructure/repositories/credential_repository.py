"""
src/app/infrastructure/repositories/credential_repository.py

Concrete SQLAlchemy implementation of CredentialRepository.
"""
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.credential.repository import CredentialRepository
from app.infrastructure.db.models import Credential


class SqlAlchemyCredentialRepository(CredentialRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, credential_id: UUID) -> Credential | None:
        result = await self._session.execute(
            select(Credential).where(Credential.id == credential_id)
        )
        return result.scalar_one_or_none()

    async def list_for_owner(self, owner_id: UUID) -> list[Credential]:
        result = await self._session.execute(
            select(Credential).where(Credential.owner_id == owner_id)
        )
        return list(result.scalars().all())

    async def add(self, credential: Credential) -> None:
        self._session.add(credential)