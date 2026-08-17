"""
src/app/infrastructure/db/models.py

SQLAlchemy 2.x ORM models. Mirrors the schema built in Checkpoint 2.1
exactly. These are infrastructure-layer classes — NOT the same as the
pure domain dataclasses that come later (Checkpoint 4). This distinction
is deliberate: the domain layer must never import SQLAlchemy.
"""
import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, LargeBinary
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.infrastructure.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())


class WorkflowVersion(Base):
    __tablename__ = "workflow_versions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workflows.id", ondelete="CASCADE"))
    version: Mapped[int]
    graph: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Credential(Base):
    __tablename__ = "credentials"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str]
    provider: Mapped[str]
    encrypted_secret: Mapped[bytes] = mapped_column(LargeBinary)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Execution(Base):
    __tablename__ = "executions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workflows.id", ondelete="CASCADE"))
    workflow_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workflow_versions.id"))
    status: Mapped[str]
    triggered_by: Mapped[str]
    started_at: Mapped[datetime | None]
    finished_at: Mapped[datetime | None]
    error: Mapped[str | None]


class NodeExecution(Base):
    __tablename__ = "node_executions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    execution_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("executions.id", ondelete="CASCADE"))
    node_id: Mapped[str]
    status: Mapped[str]
    input: Mapped[dict | None] = mapped_column(JSONB)
    output: Mapped[dict | None] = mapped_column(JSONB)
    error: Mapped[str | None]
    started_at: Mapped[datetime | None]
    finished_at: Mapped[datetime | None]


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    event_id: Mapped[str] = mapped_column(unique=True)
    raw_payload: Mapped[dict] = mapped_column(JSONB)
    received_at: Mapped[datetime] = mapped_column(server_default=func.now())
    processed_at: Mapped[datetime | None]


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    action: Mapped[str]
    target_id: Mapped[uuid.UUID | None]
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())