import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    gemini_api_key: str = ""
    backend_api_key: str = "aura_secret_key_123" # Default for demo, should be in .env
    allowed_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    database_url: str = "sqlite:///./sales_assistant.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
