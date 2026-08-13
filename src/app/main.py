"""
src/app/main.py
"""
from fastapi import FastAPI

from app.api import auth_routes, executions, workflows
from app.error_handlers import register_error_handlers
from app.logging_config import configure_logging


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="Autoinsta",
        description="Instagram workflow automation backend",
        version="0.1.0",
    )

    register_error_handlers(app)

    app.include_router(auth_routes.router, prefix="/api/auth", tags=["auth"])
    app.include_router(workflows.router, prefix="/api/workflows", tags=["workflows"])
    app.include_router(executions.router, prefix="/api/executions", tags=["executions"])

    @app.get("/health", tags=["health"])
    async def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()