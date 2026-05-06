from pydantic_settings import BaseSettings
from typing import List, Optional
import json


class Settings(BaseSettings):
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8001
    api_reload: bool = True
    debug: bool = True

    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8001",
        "http://127.0.0.1:3000",
    ]

    # Database Configuration
    db_type: str = "sqlite"  # sqlite or mysql
    sqlite_path: str = "./artifacts/ml_service.db"

    # MySQL Configuration
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = "root"
    mysql_database: str = "banyu_guide_db"

    # Paths
    artifacts_dir: str = "./artifacts"
    models_dir: str = "./artifacts/models"
    data_dir: str = "./artifacts/data"

    # Recommendation Settings
    default_top_n: int = 10
    min_rating: float = 3.0
    cf_fallback_threshold: int = 5

    @property
    def mysql_url(self) -> str:
        return f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
