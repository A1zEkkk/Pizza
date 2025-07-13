from sqlalchemy import select

from typing import Dict, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession

from DB.init.base_service_auth import BaseServiceAuthDB
from DB.Models.DB_Models.auth_models import Users, AccessToken, RefreshToken


class AuthDBService(BaseServiceAuthDB):
    async def create_user(self, login: str, password: str, role: str)-> Optional[Dict[str, str]]:
        """"
            *******************Функция создания юзера*************
            1) Хешируем пароль
            2) Открываем сессию
            3) Проверяем пользователя на существование в таблице
            4) Если пользователя нету в БД, то добавляем его
            5) Создаем рефреш и акцесс токен и добавляем в бд
            6) Возвращаем словарь с информацией
        """
        password = self.hash_password(password) # Хеш пароль
        async with self.session_maker() as session: # Открывам сессию
            session: AsyncSession #Анотатор
            stmt = select(Users).where(Users.login == login) # Генерируем sql запрос
            result = await session.execute(stmt) #Вполняем sql запрос
            existing_user = result.scalar_one_or_none() # Извлекаем только одну строку из результата SQL-запроса

            if existing_user: #Проверка на существование юзера
                print(f"Пользователь с логином {login} уже существует.")

                return None

            #Прошли проверку
            new_user = Users(role=role, login=login, password=password) #Генерируем строку (вектор)
            session.add(new_user) #добавили в сессию
            await session.commit() #отправили INSERT в базу
            await session.refresh(new_user) #Обновляем объект в базе данных
            print(f"Пользователь {login} создан в БД с ID: {new_user.id}")
            token = await self.token_manager.create_access_token(new_user) #Создаем акцесс токен
            refresh = await self.token_manager.create_refresh_token(new_user) #Создаем рефреш токен
            return {
                "user_id": new_user.id,
                "access_token": token["token"],
                "access_token_expires": token["expire"],
                "refresh_token": refresh["token"],
                "refresh_token_expires": refresh["expire"]
            }

    async def authenticate_user(self, login: str, password: str) -> Union[Dict[str, str], None, bool]:
        """
            ************Аунтефикация и верификация юзера************
            1) Открываем сессию
            2) Проверяем на существование логина в бд и проверку пароля
            3) Получаем user_id из модели Users, затем отключаем старый акцесс и рефреш токен
            4) Создаем новый токен и делаем его активным
            5) Возвращаем новые данные в виде словаря
        """
        async with self.session_maker() as session: # Открытие сессии
            session: AsyncSession
            user_query = select(Users).filter_by(login=login) # Генерируем sql запрос
            result = await session.execute(user_query) # Выполняем sql запрос
            user = result.scalar_one_or_none() # Получаем результат из бд

            if user is None: # Проверка на существование
                print("Пользователь не найден")

                return None

            if not self.verify_password(password, user.password): # Проверяем хеш пароль
                print("Неверный пароль")

                return False

            print("Успех: пользователь верифицирован")
            user_id = user.id # Получаем id пользователя

            # Запрашиваем все refresh токены пользователя
            refresh_query = select(RefreshToken).where(RefreshToken.user_id == user_id) # Генерируем sql запрос
            result_refresh = await session.execute(refresh_query) # Выполняем sql запрос
            refresh_token_objs = result_refresh.scalars().all() # Получаем все строки с этим user_id

            # Запрашиваем все access токены пользователя
            access_query = select(AccessToken).where(AccessToken.user_id == user_id) # Генерируем sql запрос
            result_access = await session.execute(access_query) # Выполняем sql запрос
            access_token_objs = result_access.scalars().all() # Получаем все строки с этим user_id

            # Обновляем флаги
            for token in refresh_token_objs:
                token.is_revoked = True
                print(f"Refresh-токен с ID {token.id} помечен как использованный.")

            for token in access_token_objs:
                token.is_revoked = True
                print(f"Access-токен с ID {token.id} помечен как использованный.")

            await session.commit()


        # Создаём новые токены (вне сессии, чтобы избежать nested session)
        access = await self.token_manager.create_access_token(user)
        refresh = await self.token_manager.create_refresh_token(user)

        return {
            "user_id": user.id,
            "access_token": access["token"],
            "access_token_expires": access["expire"],
            "refresh_token": refresh["token"],
            "refresh_token_expires": refresh["expire"]
        }
