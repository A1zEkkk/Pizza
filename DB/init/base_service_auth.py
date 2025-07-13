from DB.Models.cfg.settings import Settings
from DB.engine import ORMDatabase

from DB.Models.services.token_manager import TokenManager
from DB.Models.services.password_hasher import PasswordService


class BaseServiceAuthDB:
    def __init__(self):
        self.settings = Settings()
        self.db = ORMDatabase(self.settings.DATABASE_URL)
        self.session_maker = self.db.get_session

        self.password_service = PasswordService()
        self.hash_password = self.password_service.hash_password
        self.verify_password = self.password_service.verify_password

        self.token_manager = TokenManager(self.settings)


        self.ACCESS_TOKEN_EXPIRE_MINUTES = self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.REFRESH_TOKEN_EXPIRE_MINUTES = self.settings.REFRESH_TOKEN_EXPIRE_MINUTES
        self.ALGORITHM = self.settings.ALGORITHM
        self.SECRET_KEY = self.settings.SECRET_KEY

        print("AuthDBService инициализирован")