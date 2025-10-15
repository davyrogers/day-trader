from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model_20b: str = "gpt-oss:20b"
    ollama_model_deepseek: str = "deepseek-r1:8b"
    
    # Discord Configuration
    discord_webhook_url: Optional[str] = None
    
    # Workflow Configuration
    run_once: bool = True
    schedule_interval_hours: int = 1
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
