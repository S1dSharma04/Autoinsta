"""
src/app/domain/credential/repository.py

Port for credential persistence. Pure Python, no infrastructure
knowledge - same pattern as WorkflowRepository from Checkpoint 2.4.
"""
from abc import ABC, abstractmethod
from uuid import UUID


class CredentialRepository(ABC):
    @abstractmethod
    async def get_by_id(self, credential_id: UUID) -> "Credential | None":
        ...

    @abstractmethod
    async def list_for_owner(self, owner_id: UUID) -> list["Credential"]:
        ...

    @abstractmethod
    async def add(self, credential: "Credential") -> None:
        ...