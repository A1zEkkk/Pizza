from DB.engine import ORMDatabase
from DB.Models.cfg.settings import Settings


class BaseServiceToken:

    def __init__(self, settings: Settings):

        self.settings = settings
        self.db = ORMDatabase(settings.DATABASE_URL)
        self.session_maker = self.db.get_session

        self.SECRET_KEY = settings.SECRET_KEY
        self.ALGORITHM = settings.ALGORITHM

        print("TokenManager инициализирован")