from __future__ import annotations

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy import text

from core.config import settings
from core.database import engine

app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_redirect():
    return RedirectResponse(url="/api/v1/health", status_code=307)


@app.get("/api/v1/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint verifying API and Database connectivity."""
    db_status = "healthy"
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:  # noqa: BLE001  <--- ضعه هنا
        db_status = f"unhealthy: {e!s}"  # <--- وهنا

    return {
        "status": "ok" if db_status == "healthy" else "degraded",
        "database": db_status,
    }
