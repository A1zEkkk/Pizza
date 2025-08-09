from DB.Models.DB_models import User, RefreshToken
from .base import BaseRepository, InstrumentedAttribute


class UserRepository(BaseRepository[User]):
    def get_pk_column(self) ->InstrumentedAttribute:
        return self.model.id

class RefreshRepository(BaseRepository[RefreshToken]):
    def get_pk_column(self) ->InstrumentedAttribute:
        return self.model.user_id