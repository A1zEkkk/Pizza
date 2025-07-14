from DB.init.base_service_auth import BaseServiceAuthDB
from DB.Models.DB_Models.auth_models import Users, AccessToken, RefreshToken


from typing import Optional, Dict, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class AuthDBService(BaseServiceAuthDB):
    async def create_user(self, login: str, password: str, role: str) -> Optional[Dict[str, Union[int, str]]]:
        """
        Создает пользователя, если его ещё нет:
        1) Хеширует пароль
        2) Проверяет наличие пользователя с таким логином
        3) Создаёт нового пользователя
        4) Создаёт access и refresh токены
        5) Возвращает данные пользователя и токены
        """
        hashed_password = self.hash_password(password)

        async with self.session_maker() as session:
            session: AsyncSession
            stmt = select(Users).where(Users.login == login)
            result = await session.execute(stmt)
            existing_user = result.scalar_one_or_none()

            if existing_user:
                print(f"Пользователь с логином '{login}' уже существует.")
                return None

            new_user = Users(role=role, login=login, password=hashed_password)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

            print(f"Пользователь '{login}' создан с ID: {new_user.id}")

            access_token = await self.token_manager.create_access_token(new_user)
            refresh_token = await self.token_manager.create_refresh_token(new_user)

            return {
                "user_id": new_user.id,
                "access_token": access_token["token"],
                "access_token_expires": access_token["expire"],
                "refresh_token": refresh_token["token"],
                "refresh_token_expires": refresh_token["expire"]
            }

    async def authenticate_user(self, login: str, password: str) -> Union[Dict[str, Union[int, str]], None, bool]:
        """
        Аутентифицирует пользователя:
        1) Проверяет наличие пользователя с таким логином
        2) Проверяет пароль
        3) Помечает все токены пользователя как отозванные
        4) Создаёт новые токены и возвращает их
        """
        async with self.session_maker() as session:
            session: AsyncSession

            # Получаем пользователя
            stmt = select(Users).filter_by(login=login)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if not user:
                print("Пользователь не найден")
                return None

            if not self.verify_password(password, user.password):
                print("Неверный пароль")
                return False

            print("Пользователь верифицирован")

            # Отзываем все токены пользователя
            for token_model in [RefreshToken, AccessToken]:
                stmt_tokens = select(token_model).where(token_model.user_id == user.id)
                result_tokens = await session.execute(stmt_tokens)
                tokens = result_tokens.scalars().all()
                for token in tokens:
                    token.is_revoked = True
                    print(f"{token_model.__name__} с ID {token.id} помечен как отозванный.")

            await session.commit()

        # Создаём новые токены вне сессии, чтобы избежать nested session
        access_token = await self.token_manager.create_access_token(user)
        refresh_token = await self.token_manager.create_refresh_token(user)

        return {
            "user_id": user.id,
            "access_token": access_token["token"],
            "access_token_expires": access_token["expire"],
            "refresh_token": refresh_token["token"],
            "refresh_token_expires": refresh_token["expire"]
        }
