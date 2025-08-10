from abc import ABC, abstractmethod

from pydantic import BaseModel
from typing import Generic, Type, TypeVar

from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy import select, delete, insert, update

from DB.utils.exceptions import DuplicateEntryError
from DB.Models import Base
from ....engine import ORMDatabase

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType], ABC):
    def __init__(self, model: Type[ModelType], orm_database: ORMDatabase):
        self.model = model
        self.orm_database = orm_database

    @abstractmethod
    def get_pk_column(self)->InstrumentedAttribute:
        """Возвращает колонку, которая является РК"""
        pass

    #метод create Должен создаваться в каждом уникальном классе. Тут он нахуй не нужен

    async def get_by_id(self, id_value: int):
        async with self.orm_database.get_session() as session:
            stmt = select(self.model).where(self.get_pk_column() == id_value)
            result = await session.execute(stmt)
            obj = result.scalar_one_or_none()

            if obj is None:
                raise NoResultFound

            return obj

    async def create(self, data: BaseModel):
         data_dict = data.model_dump()
         async with self.orm_database.get_session() as session:
             try:
                 data = self.model(**data_dict)
                 session.add(data)
                 await session.commit()
                 await session.refresh(data)
                 return data

             except IntegrityError as e:
                 await session.rollback()
                 raise DuplicateEntryError(f"Объект с такими уникальными данными уже существует.") from e

    #Дополнить нужно проверку на существование data
    async def update(self, id_value: int, data: BaseModel):
        async with self.orm_database.get_session() as session:
            stmt = update(self.model).where(self.get_pk_column() == id_value).values(**data.model_dump()).returning(self.model)
            result = await session.execute(stmt)

            obj = result.scalar_one_or_none()
            if obj is None:
                raise NoResultFound

            await session.commit()

            return obj

    async def delete(self, id_value: int):
        async with self.orm_database.get_session() as session:
            stmt = select(self.model).where(self.get_pk_column() == id_value)
            result = await session.execute(stmt)
            obj_to_delete = result.scalar_one_or_none()

            if obj_to_delete is None:
                raise NoResultFound


            await session.delete(obj_to_delete)
            await session.commit()

            return obj_to_delete
