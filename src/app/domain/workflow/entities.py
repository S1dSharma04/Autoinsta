"""
src/app/domain/workflow/entities.py

Pure domain objects for the workflow graph. No SQLAlchemy, no FastAPI -
these mirror the frontend's Node/Edge/Workflow shapes exactly (see the
frontend integration spec), since workflow_versions.graph stores this
structure verbatim as JSONB.
"""
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Position:
    x: float
    y: float


@dataclass(frozen=True)
class Node:
    id: str
    type: str
    position: Position
    data: dict


@dataclass(frozen=True)
class Edge:
    id: str
    source: str
    target: str
    source_handle: str | None = None
    target_handle: str | None = None


@dataclass(frozen=True)
class Graph:
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)


@dataclass
class WorkflowVersion:
    id: UUID
    workflow_id: UUID
    version: int
    graph: Graph
    created_at: datetime


@dataclass
class Workflow:
    id: UUID
    owner_id: UUID
    name: str
    is_active: bool
    current_version: WorkflowVersion | None
    created_at: datetime
    updated_at: datetime