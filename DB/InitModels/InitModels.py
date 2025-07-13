from DB.Models import Base
from DB.engine import ORMDatabase

from DB.Models.cfg.settings import Settings

from DB.Models.DB_Models.auth_models import Users, RefreshToken, AccessToken



#Создание таблиц через драйвер engine
async def init_models():
    url_db = Settings().DATABASE_URL

    engine = ORMDatabase(url_db)
    async with engine.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print(url_db)
