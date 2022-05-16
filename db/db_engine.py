import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_session
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class DBEngine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not DBEngine._instance:
            DBEngine._instance = super(DBEngine, cls).__new__(cls, *args, **kwargs)
        return DBEngine._instance

    def __init__(self):
        self.engine = create_async_engine('postgresql+asyncpg://admin:admin@127.0.0.1/uav_simulation', echo=True)

    async def get_session(self):
        async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            return session

    async def init_models(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
