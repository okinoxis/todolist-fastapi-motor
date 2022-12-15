from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str
    BACKEND_CORS_ORIGINS: str 
    PROJECT_NAME: str 
    MONGO_SERVER: str 

    class Config:
        env_file = './.env'

settings = Settings()# pyright: ignore