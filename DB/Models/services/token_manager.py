import uuid

from typing import Dict

from datetime import datetime

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from DB.init.base_service_token import BaseServiceToken
from DB.Models.DB_Models.auth_models import Users, AccessToken, RefreshToken

from DB.utils import token_checker, add_row, fetch_time_interval, create_token


class TokenManager(BaseServiceToken):
    async def create_access_token(self, user: Users) -> str:
        """"
            ****************************Функция для создания Access_token**************************************
            1) Создаем время протухания токена
            2) Создается JWT токен
            3) Открывается сессия и создается объект для добавление в DB AT
            4) Сохраняем данные в БД
        """
        minutes = self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
        expire, issued_at = fetch_time_interval(minutes)

        payload = {
            "sub": str(user.id),
            "exp": expire,
            "iat": issued_at,
            "jti": str(uuid.uuid4())
        }

        token =  create_token(payload, self.SECRET_KEY, self.ALGORITHM) # JWT токен

        async with self.session_maker() as session:  # Открытие сессии
            session: AsyncSession

            #Добавление данных в BD
            await add_row(
                session,
                AccessToken,
                token=token,
                user_id=user.id,
                expires_at=expire,
                issued_at=issued_at,
                is_revoked=False
            )
            print(f"Refresh token создан для user_id={user.id}")


            return token


    async def create_refresh_token(self, user: Users) -> str:
        """
            ****************************Функция для создания Refresh_token**************************************
            1) Создаем время протухания токена
            2) Создается JWT токен
            3) Открывается сессия и создается объект для добавление в DB AT
            4) Сохраняем данные в БД
        """
        minutes = self.settings.REFRESH_TOKEN_EXPIRE_MINUTES
        expire, issued_at = fetch_time_interval(minutes)
        jti = str(uuid.uuid4())

        payload = {
            "sub": str(user.id),
            "exp": expire,
            "iat": issued_at,
            "jti": jti,
            "type": "refresh"
        }

        token =  create_token(payload, self.SECRET_KEY, algorithm=self.ALGORITHM) # JWT токен

        async with self.session_maker() as session:  # Открытие сессии
            session: AsyncSession

            await add_row(
                session,
                RefreshToken,
                token=token,
                user_id=user.id,
                expires_at=expire,
                issued_at=issued_at,
                is_revoked=False,
                jti=jti,
                used=False
            )
            print(f"Refresh token создан для user_id={user.id}")

            return token

    async def revoke_tokens(self, type_token: str, token: str) -> bool:
        """Отключает access и все связанные refresh токены пользователя"""
        if type_token == "access":
            model = AccessToken
        else:
            model = RefreshToken

        async with self.session_maker() as session:
            session: AsyncSession

            #Отзываем токен
            stmt_token = (
                update(model)
                .where(model.token == token)
                .values(is_revoked=True)
                .returning(model.user_id)
            )
            await session.execute(stmt_token)
            await session.commit()

            if stmt_token:
                return True
            else:
                return False


    async def access_is_alive(self, token: str) -> bool:
        async with self.session_maker() as session:
            return await token_checker(token, session, AccessToken)

    async def refresh_is_alive(self, token: str) -> bool:
        async with self.session_maker() as session:
            return await token_checker(token, session, RefreshToken)