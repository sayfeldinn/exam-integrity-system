from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralised application settings loaded from infra/.env (M0-15).

    Required fields (no default) cause a ValidationError at startup
    if the variable is absent from the environment — fail fast per M0:132.
    """

    # --- Identity ---
    PROJECT_NAME: str = "Exam Integrity System API"

    # --- Postgres -------------------------------------------------------
    # Individual vars (used by docker-compose / Alembic in M0-18).
    POSTGRES_USER: str = "exam_user"
    POSTGRES_PASSWORD: str = "change-me-local-only"
    POSTGRES_DB: str = "exam_integrity"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432

    # Unified asyncpg URL — REQUIRED, no default → fail fast if missing.
    DATABASE_URL: str

    # --- API ------------------------------------------------------------
    API_PORT: int = 8000

    # JWT signing secret — REQUIRED, no default → fail fast if missing.
    # Generate a safe value with: openssl rand -hex 32
    JWT_SECRET: str

    # --- CORS -----------------------------------------------------------
    # Comma-separated origins, e.g. "http://localhost:3000,https://staging.example.com"
    # Use cors_origins_list property for CORSMiddleware (M0-16).
    CORS_ORIGINS: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS_ORIGINS string into a list for FastAPI CORSMiddleware."""
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    # --- pydantic-settings config ---------------------------------------
    model_config = SettingsConfigDict(
        # Try multiple relative paths so the import works whether you run
        # from services/api/ or from the repo root (e.g. in CI / Docker).
        env_file=("../infra/.env", "../../infra/.env", "infra/.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",  # silently ignore unrelated vars in .env (e.g. WEB_PORT)
    )


# Singleton — import this anywhere: `from core.config import settings`
settings = Settings()
