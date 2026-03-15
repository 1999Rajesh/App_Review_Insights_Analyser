from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application configuration"""
    
    # Groq API (Deprecated - kept for backward compatibility)
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    
    # Google Gemini API (Primary LLM)
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"
    
    # SMTP Email
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 465
    SENDER_EMAIL: str
    SENDER_PASSWORD: str
    RECIPIENT_EMAIL: str
    
    # App Settings
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    MAX_THEMES: int = 5
    MAX_WORDS: int = 250
    REVIEW_WEEKS_RANGE: int = 8
    MAX_REVIEWS_TO_FETCH: int = 500
    
    # Quality Filters for Reviews (Phase 1)
    MIN_REVIEW_WORD_COUNT: int = 5
    ALLOW_EMOJIS: bool = False
    REQUIRED_LANGUAGE: str = "en"
    REVIEWS_DATA_DIR: str = "data/reviews"
    
    # Google Play Store Settings
    PLAY_STORE_DEFAULT_APP_ID: str = ""
    PLAY_STORE_COUNTRY: str = "us"
    PLAY_STORE_LANGUAGE: str = "en"
    
    # Scheduler Settings
    SCHEDULER_INTERVAL_MINUTES: int = 5  # Run every 5 minutes for testing
    SCHEDULER_LOG_FILE: str = "logs/scheduler.log"
    
    # Railway Deployment
    PORT: int = 8000
    
    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
