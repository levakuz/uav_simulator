import datetime
from abc import abstractmethod

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_engine import DBEngine


class BaseModelMinix:
    @abstractmethod
    async def get(self, id):
        model = str(type(self).__name__)
        engine = DBEngine()
        session: AsyncSession = await engine.get_session()
        result = await session.execute(
            select(self.__class__).where(self.__class__.id == id)
        )
        await session.close()
        for row in result:
            return row[model]

    async def create(self, **kwargs):
        engine = DBEngine()
        session: AsyncSession = await engine.get_session()
        for key, value in kwargs.items():
            if hasattr(self, key):
                if key == 'time':
                    value = datetime.datetime.fromisoformat(value)
                setattr(self, key, value)
        session.add(self)
        result = await session.commit()
        await session.close()
        return result

    async def delete(self, id: int):
        engine = DBEngine()
        session: AsyncSession = await engine.get_session()
        result = await session.execute(
            delete(self.__class__).where(self.__class__.id == id)
        )
        await session.commit()
        await session.close()
        return result

    async def update(self, id: int, **kwargs):
        engine = DBEngine()
        session: AsyncSession = await engine.get_session()
        # for key, value in kwargs.items():
        #     if hasattr(self, key):
        #         if key == 'time':
        #             value = datetime.datetime.fromisoformat(value)
        #         setattr(self, key, value)
        for key, value in kwargs.items():
            if key == 'time':
                kwargs[key] = datetime.datetime.fromisoformat(value)
        # session.add(self)
        result = await session.execute(
            update(self.__class__).where(self.__class__.id == id).values(**kwargs)
        )
        await session.commit()
        await session.close()
        return result
