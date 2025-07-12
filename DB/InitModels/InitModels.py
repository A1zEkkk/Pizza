import asyncio

from sqlalchemy import URL

from DB.Models.cfg.settings import Settings

from DB.Models import Base
from DB.engine import ORMDatabase

from DB.Models.DB_Models.auth_models import Users, RefreshToken, AccessToken


url = URL.create(
        drivername="postgresql+asyncpg",
        username="postgres",
        password="postgres",
        host="localhost",
        port=5432,
        database="Pizza",
    )

#Создание таблиц через драйвер engine
async def init_models():
    url_db = url

    engine = ORMDatabase(url_db)
    async with engine.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print(url_db)
