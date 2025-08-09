from DB.Models.services import TokenManager, PasswordService
from DB.engine import ORMDatabase
from DB.Models.services.repository import BaseRepository
from DB.Models.cfg.settings import Settings
from DB.Models.DB_models.auth import User
from DB.Models.schemas.auth import UserData

from asyncio import run

async def main():
    settings = Settings()
    url = settings.DATABASE_URL
    orm = ORMDatabase(url)

    base_repo = BaseRepository(model=User, orm_database=orm)
    user_data = UserData(login="gmosm3131cn2131efosml", password="gmosmlssrf", role="admin")


    a = await base_repo.create(user_data)
    print(a)

run(main())
