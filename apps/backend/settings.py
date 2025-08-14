from pathlib import Path
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # v2-style config (NO class Config)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",        # ignore unknown vars in .env
    )

    # Core
    CORS_ORIGINS: List[str] = ["http://localhost:3001"]          # e.g. '["http://localhost:3001"]' in .env
    UPLOAD_DIR: str = str(Path(__file__).resolve().parent / "uploads")
    DB_URL: str = "sqlite:///./gallery.db"

    # Optional extras (only if you want to keep these keys in .env)
    PUBLIC_BASE_URL: Optional[str] = None
    FRONTEND_ORIGIN: Optional[str] = None
    BACKEND_ORIGIN: Optional[str] = None
    NEXT_PUBLIC_API_BASE_URL: Optional[str] = None


settings = Settings()

# Ensure upload dir exists
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
