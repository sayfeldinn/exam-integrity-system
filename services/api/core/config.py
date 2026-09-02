from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Exam Integrity System API"

    class Config:
        env_file = ".env"


settings = Settings()
