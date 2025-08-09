from DB.Models.cfg.settings import Settings
from datetime import datetime, timezone, timedelta
import jwt
from jwt import ExpiredSignatureError, PyJWTError

from typing import Dict, Any


class TokenManager:
    def __init__(self, settings: Settings):

        self.settings = settings
        self.SECRET_KEY = settings.SECRET_KEY
        self.ALGORITHM = settings.ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES


    def create_access_token(self, user_id: int, role: str) -> str:
        issued_at = datetime.now(timezone.utc)
        exp = issued_at + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self._create_token(user_id, token_type="access", issued_at=issued_at, exp=exp, role=role)
        return access_token


    def create_refresh_token(self, user_id: int, role: str) -> str:
        issued_at = datetime.now(timezone.utc)
        exp = issued_at + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token = self._create_token(user_id, token_type="refresh", issued_at=issued_at, exp=exp, role=role)
        return refresh_token


    def verify_and_decode_token(self, token: str)-> Dict[str, Any]:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Срок действия токена истек.")
        except PyJWTError:
            raise ValueError("Невалидный токен.")


    def get_sub_from_token(self, token: str):
        payload = self.verify_and_decode_token(token)
        return payload.get("sub")

    def _create_token(self, user_id: int, token_type: str, issued_at: datetime, exp: datetime, role: str) -> str:
        payload = {
            "sub": str(user_id),
            "iat": int(issued_at.timestamp()),
            "exp": int(exp.timestamp()),
            "type": token_type,
            "role": role,
        }
        token =  jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token