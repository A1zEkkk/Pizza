from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi.templating import Jinja2Templates
from pathlib import Path


#docker run --name Pizza -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=Pizza -p 5432:5432 -d postgres:15

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    SECRET_KEY: str

    class Config:
        env_file = BASE_DIR / ".env"
