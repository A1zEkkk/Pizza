import jwt
import uuid

from typing import Dict

from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from DB.Models.services_init import BaseServiceToken
from DB.Models.DB_Models.auth_models import Users, AccessToken, RefreshToken


class TokenManager(BaseServiceToken):
    async def create_access_token(self, user: Users) -> Dict[str, str]:
        """"
            ****************************Функция для создания Access_token**************************************
            1) Создаем время протухания токена
            2) Создается JWT токен
            3) Открывается сессия и создается объект для добавление в DB AT
            4) Сохраняем данные в БД
        """
        expire = (datetime.now(timezone.utc) + timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)).replace(
            tzinfo=None)  # Время старта
        issued_at = datetime.now(timezone.utc).replace(tzinfo=None)  # Время протухания

        payload = {
            "sub": str(user.id),
            "exp": expire,
            "iat": issued_at,
            "jti": str(uuid.uuid4())
        }  # Данные для управления сессией

        token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)  # JWT токен

        async with self.session_maker() as session:  # Открытие сессии
            session: AsyncSession

            db_token = AccessToken(
                token=token,
                user_id=user.id,
                expires_at=expire,
                issued_at=issued_at,
                is_revoked=False
            )  # Access токен

            session.add(db_token)  # Добавляем наш токен
            await session.commit()  # Сохраняем изменения
            await session.refresh(db_token)  # Обновляем изменения
            print(f"Access token создан для user_id={user.id}")

            return {
                "token": token,
                "expire": expire
            }


    async def create_refresh_token(self, user: Users) -> Dict[str, str]:
        """
            ****************************Функция для создания Refresh_token**************************************
            1) Создаем время протухания токена
            2) Создается JWT токен
            3) Открывается сессия и создается объект для добавление в DB AT
            4) Сохраняем данные в БД
        """
        expire = (datetime.now(timezone.utc) + timedelta(minutes=self.settings.REFRESH_TOKEN_EXPIRE_MINUTES)).replace(
            tzinfo=None)  # Cтарт
        issued_at = datetime.now(timezone.utc).replace(tzinfo=None)  # Время протухания токена
        # Эта функция из встроенного модуля
        # Python uuid генерирует универсальный уникальный идентификатор (UUID).
        # UUID — это 128-битное число, которое гарантированно является уникальным в пространстве и времени.
        # uuid4() генерирует случайный UUID.
        jti = str(uuid.uuid4())

        payload = {
            "sub": str(user.id),
            "exp": expire,
            "iat": issued_at,
            "jti": jti,
            "type": "refresh"
        }  # Данные для управления сессией

        token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)  # JWT токен

        async with self.session_maker() as session:  # Открытие сессии
            session: AsyncSession

            db_token = RefreshToken(
                token=token,
                user_id=user.id,
                expires_at=expire,
                issued_at=issued_at,
                is_revoked=False,
                jti=jti,
                used=False
            )  # Данные которые добавим в DB

            session.add(db_token)  # Добавили в сессию
            await session.commit()  # Сохранили
            await session.refresh(db_token)  # Обновили

            print(f"Refresh token создан для user_id={user.id}")

            return {
                "token": token,
                "expire": expire
            }