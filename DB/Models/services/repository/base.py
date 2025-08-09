from abc import ABC, abstractmethod

from pydantic import BaseModel
from typing import Generic, Type, TypeVar

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy import select, delete, insert, update

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
            result = await session.execute(stmt).scalar_one_or_none()

            if result is None:
                raise NoResultFound

            return result

    async def create(self, data: BaseModel):
         data_dict = data.model_dump()
         async with self.orm_database.get_session() as session:
            obj = session.add(self.model(**data_dict))
            await session.commit()
            await session.refresh(obj)
            return obj

    async def update(self, id_value: int, data: BaseModel):
        async with self.orm_database.get_session() as session:
            stmt = update(self.model).where(self.get_pk_column() == id_value).values(**data.model_dump()).returning(self.model)
            result = await session.execute(stmt)
            await session.commit()

            obj = result.scalar_one_or_none()
            if obj is None:
                raise NoResultFound

            return result

    async def delete(self, id_value: int):
        async with self.orm_database.get_session() as session:
            stmt = delete(self.model).where(self.get_pk_column() == id_value).returning(self.model)
            result = await session.execute(stmt)
            await session.commit()

            obj = result.scalar_one_or_none()
            if obj is None:
                raise NoResultFound

            return obj
