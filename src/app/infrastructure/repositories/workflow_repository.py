"""
src/app/infrastructure/repositories/workflow_repository.py

Concrete SQLAlchemy implementation of the WorkflowRepository port.
Translates between ORM rows (app.infrastructure.db.models.Workflow)
and whatever the domain layer works with. For now, since the real
domain Workflow dataclass doesn't exist until Checkpoint 4.1, this
repository works directly with the ORM model - that will change
once the domain object exists and a mapper sits between them.
"""
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.workflow.repository import WorkflowRepository
from app.infrastructure.db.models import Workflow


class SqlAlchemyWorkflowRepository(WorkflowRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, workflow_id: UUID) -> Workflow | None:
        result = await self._session.execute(
            select(Workflow).where(Workflow.id == workflow_id)
        )
        return result.scalar_one_or_none()

    async def list_for_owner(self, owner_id: UUID) -> list[Workflow]:
        result = await self._session.execute(
            select(Workflow).where(Workflow.owner_id == owner_id)
        )
        return list(result.scalars().all())

    async def add(self, workflow: Workflow) -> None:
        self._session.add(workflow)