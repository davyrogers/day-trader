from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434"
    
    # AI Models Configuration (comma-separated list)
    ai_models: str = "deepseek-r1:8b,gpt-oss:20b,gpt-oss:20b,gpt-oss:20b,llama3:70b,mistral:latest"
    ai_temperatures: str = "0.7,0.8,0.9,1.0,0.85,0.75"
    
    # Synthesis Model
    synthesis_model: str = "gpt-oss:20b"
    synthesis_temperature: float = 0.7
    
    # Concurrent Execution (false if Ollama can't handle parallel requests)
    run_concurrent: bool = False
    
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
        extra = "ignore"  # Ignore extra fields for backward compatibility
    
    def get_ai_models(self) -> List[tuple[str, float]]:
        """Parse AI models and temperatures into list of tuples."""
        models = [m.strip() for m in self.ai_models.split(",")]
        temps = [float(t.strip()) for t in self.ai_temperatures.split(",")]
        
        # Ensure we have temperatures for all models
        while len(temps) < len(models):
            temps.append(0.8)  # Default temperature
        
        return list(zip(models, temps[:len(models)]))


settings = Settings()
