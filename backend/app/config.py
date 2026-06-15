import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/flowdesk"
    
    # API
    API_KEY: str = "secret-api-key-change-in-production"
    API_TITLE: str = "Flowdesk - Shipment Management API"
    API_VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
