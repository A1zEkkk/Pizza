from DB.Models.services import TokenManager, PasswordService
from DB.engine import ORMDatabase
from DB.Models.services.repository import BaseRepository
from DB.Models.cfg.settings import Settings
from DB.Models.DB_models.auth import User
from DB.Models.schemas.auth import UserData

from DB.Models.services.repository import *

from freezegun import freeze_time


from asyncio import run

async def main():
    settings = Settings()
    url = settings.DATABASE_URL
    orm = ORMDatabase(url)
    token_manager = TokenManager(settings)
    user_repository = UserRepository(User, orm)
    user_data = UserData(login="te311112312312412412313213123122321321412312st1", password="<PASSWORD312>312312512w21312321321", role="admin")
    info = await user_repository.create(user_data)
    access_token = token_manager.create_access_token(10, "admin")
    print(info)
run(main())
