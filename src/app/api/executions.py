"""
src/app/api/executions.py

Stub execution routes. Real logic arrives in Checkpoint 4/5.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_executions() -> dict:
    return {"executions": []}