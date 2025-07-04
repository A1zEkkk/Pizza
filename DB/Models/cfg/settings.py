import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

from sqlalchemy import URL

#docker run --name Pizza -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=Pizza -p 5434:5432 -d postgres:15

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            Path(__file__).resolve().parent.parent.parent.parent, ".env"
        )
    )

    def get_db_url(self):
        return str(URL.create(
            drivername="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB
        ))

url = URL.create(
        drivername="postgresql+asyncpg",
        username="postgres",
        password="postgres",
        host="localhost",
        port=5434,
        database="Pizza"
    )