from DB.Models.cfg.settings import Settings
from DB.engine import ORMDatabase

class BaseService:
    def __init__(self):
        self.settings = Settings()
        self.db = ORMDatabase(self.settings.DATABASE_URL)
        self.session_maker = self.db.get_session