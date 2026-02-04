"""
config.py - Centralized configuration using Pydantic Settings

Loads all settings from environment variables with defaults.
"""

from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    
    # ============================================================
    # APP SETTINGS
    # ============================================================
    APP_NAME: str = "ScamShield API"
    APP_VERSION: str = "4.0.0"
    DEBUG: bool = False
    FRONTEND_URL: str = "https://scam-shield-1yzg-42nohqy3p-morbius-projects-43b3a6c9.vercel.app"  # For OAuth redirects
    
    # API Authentication
    API_SECRET_KEY: str = "smsfg54sf8g4s85g4wr6smsf8g4s85g4wr6sms"
    
    # ============================================================
    # DATABASE (MongoDB)
    # ============================================================
    MONGODB_URL: str = "mongodb+srv://morbius:m0rbius@cluster0.rsl5ak3.mongodb.net/scamshield"
    MONGODB_DB_NAME: str = "scamshield"
    
    # ============================================================
    # JWT AUTHENTICATION
    # ============================================================
    JWT_SECRET_KEY: str = "e5d8c2b7a9f3e6d1c4b8a2f5e9d3c7b1a6f0e4d8c2b6a0f4e8d2c6b0a4f8e2d6"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # ============================================================
    # GOOGLE OAUTH 2.0
    # Get credentials at: https://console.cloud.google.com/apis/credentials
    # ============================================================
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: str = "https://scamshield-api-hocl.onrender.com/api/v1/auth/google/callback"
    
    # ============================================================
    # GITHUB OAUTH (optional)
    # Get credentials at: https://github.com/settings/developers
    # ============================================================
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    GITHUB_REDIRECT_URI: str = "https://scamshield-api-hocl.onrender.com/api/v1/auth/github/callback"
    
    # ============================================================
    # AI PROVIDERS
    # ============================================================
    # Groq - FREE, fast
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    
    # Google Gemini - FREE tier
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"
    
    # DeepSeek - affordable
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_MODEL: str = "deepseek-chat"
    
    # Ollama - FREE, local
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    
    # Which provider to use
    AI_PROVIDER: str = "auto"  # auto, groq, gemini, deepseek, ollama
    
    # ============================================================
    # CALLBACK SETTINGS (GUVI Hackathon)
    # ============================================================
    GUVI_CALLBACK_URL: str = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
    MIN_MESSAGES_BEFORE_REPORT: int = 6
    AUTO_CALLBACK: bool = True
    
    # ============================================================
    # EMAIL SETTINGS (for password reset, verification)
    # ============================================================
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: str = "noreply@scamshield.com"
    EMAILS_FROM_NAME: str = "ScamShield"
    
    # ============================================================
    # CORS SETTINGS
    # ============================================================
    CORS_ORIGINS: str = "https://scam-shield-1yzg-42nohqy3p-morbius-projects-43b3a6c9.vercel.app"  # Comma-separated origins or "*" for all
    
    # ============================================================
    # RATE LIMITING
    # ============================================================
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # ============================================================
    # SUPPORTED LANGUAGES
    # ============================================================
    SUPPORTED_LANGUAGES: str = "en,hi,ta,te,kn,ml,bn,mr,gu,pa"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Use this instead of creating new Settings() each time.
    """
    return Settings()


# Global settings instance
settings = get_settings()
