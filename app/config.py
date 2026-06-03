from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://revel_user:revel_password@localhost:5432/revel_erp"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
