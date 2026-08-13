"""
src/app/main.py

Application factory. `create_app()` builds and returns a fully configured
FastAPI instance. Nothing at module level talks to a database, reads a
file, or does I/O — that all happens inside functions, called on purpose,
at a time we control (app startup, or a test fixture).
"""
from fastapi import FastAPI

from app.api import auth_routes, executions, workflows


def create_app() -> FastAPI:
    app = FastAPI(
        title="Autoinsta",
        description="Instagram workflow automation backend",
        version="0.1.0",
    )

    app.include_router(auth_routes.router, prefix="/api/auth", tags=["auth"])
    app.include_router(workflows.router, prefix="/api/workflows", tags=["workflows"])
    app.include_router(executions.router, prefix="/api/executions", tags=["executions"])

    @app.get("/health", tags=["health"])
    async def health() -> dict:
        return {"status": "ok"}

    return app


# The ASGI server (uvicorn) needs a module-level object to point at.
# This is the ONE place a factory result gets called eagerly — and it's
# fine here, because this module's only job is "be the thing uvicorn imports."
app = create_app()