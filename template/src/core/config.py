from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Image Matching Service"
    API_V1_STR: str = "/api/v1"

    # Model Configuration
    MODEL_NAME: str = "ViT-B-32"
    DATASET_NAME: str = "laion2b_s34b_b79k"
    MODEL_CACHE_DIR: str = "./models_cache"

    # Database Configuration (Placeholder)
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    class Config:
        env_file = ".env"

settings = Settings()
