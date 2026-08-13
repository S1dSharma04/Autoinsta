"""
src/app/error_handlers.py

One place that decides what an error looks like to the client, for
every unhandled exception anywhere in the app. Two goals:
  1. Never leak a Python stack trace to the client (security).
  2. Every error response has the same JSON shape, so the frontend
     (and you, debugging) can rely on it.
"""
import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = structlog.get_logger(__name__)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(
            "unhandled_exception",
            path=request.url.path,
            method=request.method,
            exc_info=exc,
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_server_error",
                "message": "Something went wrong. This has been logged.",
            },
        )