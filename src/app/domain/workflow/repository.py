"""
src/app/domain/workflow/repository.py

The port (interface) for workflow persistence. Pure Python - no
SQLAlchemy, no infrastructure knowledge. application code depends on
THIS, never on the concrete implementation in infrastructure.
"""
from abc import ABC, abstractmethod
from uuid import UUID


class WorkflowRepository(ABC):
    @abstractmethod
    async def get_by_id(self, workflow_id: UUID) -> "Workflow | None":
        ...

    @abstractmethod
    async def list_for_owner(self, owner_id: UUID) -> list["Workflow"]:
        ...

    @abstractmethod
    async def add(self, workflow: "Workflow") -> None:
        ...