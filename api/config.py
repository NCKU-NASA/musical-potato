from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

    """Application configuration"""
    APP_TITLE: str = "RAID 3 Storage System"
    APP_DESCRIPTION: str = (
        "Implement a simple web interface for the RAID 3 storage system."
    )
    APP_VERSION: str = "0.1.0"
    APP_OPENAPI_URL: str = "/openapi.json"
    APP_PREFIX: str = "/api"

    """File storage configuration"""
    UPLOAD_PATH: str = "/tmp"
    FOLDER_PREFIX: str = "block"
    NUM_DISKS: int = 5
    MAX_SIZE: int = 1024 * 1024 * 100  # 100MB


settings = Settings()
