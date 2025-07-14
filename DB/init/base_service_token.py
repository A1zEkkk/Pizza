from DB.engine import ORMDatabase
from DB.Models.cfg.settings import Settings


class BaseServiceToken:
    def __init__(self):
        self.settings = Settings()
        self.db = ORMDatabase(self.settings.DATABASE_URL)
        self.session_maker = self.db.get_session
        self.SECRET_KEY = self.settings.SECRET_KEY
        self.ALGORITHM = self.settings.ALGORITHM
        print("TokenManager инициализирован")