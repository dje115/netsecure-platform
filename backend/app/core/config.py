"""
Application Configuration
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "Security Assessment Platform"
    API_VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "postgresql://security_admin:changeme@localhost:5432/security_platform"
    
    # Security
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # AI Services
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Scanner Service (WSL2)
    WSL_SCANNER_URL: str = "http://localhost:9000"
    WSL_SCANNER_HOST: str = "localhost"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
