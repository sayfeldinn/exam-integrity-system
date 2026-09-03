from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Exam Integrity System API"

    # M0-14: minimal scaffold. M0-15 will add DATABASE_URL, JWT_SECRET, CORS_ORIGINS, API_PORT with env validation.
    model_config = SettingsConfigDict(
        env_file=("../infra/.env", "../../infra/.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
