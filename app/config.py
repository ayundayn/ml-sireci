from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    debug: bool = True

    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]

    # Paths
    artifacts_dir: str = "./artifacts"
    models_dir: str = "./artifacts/models"
    data_dir: str = "./artifacts/data"

    # Recommendation Settings
    default_top_n: int = 10
    min_rating: float = 3.0
    cf_fallback_threshold: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
