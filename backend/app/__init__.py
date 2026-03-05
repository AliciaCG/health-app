"""
Application factory.
Creates and configures the FastAPI app instance.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import init_db
from app.routers import records_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── Middleware ─────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Startup ────────────────────────────────────────────────────────────────
    @app.on_event("startup")
    def on_startup():
        init_db()

    # ── Health check ───────────────────────────────────────────────────────────
    @app.get("/health", tags=["meta"], summary="API health check")
    def health_check():
        return {"status": "ok", "version": settings.APP_VERSION}

    # ── Routers ────────────────────────────────────────────────────────────────
    app.include_router(records_router)

    return app
