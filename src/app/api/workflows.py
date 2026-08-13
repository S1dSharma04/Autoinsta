"""
src/app/api/workflows.py

Stub workflow routes. Real CRUD arrives in Checkpoint 4.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_workflows() -> dict:
    return {"workflows": []}