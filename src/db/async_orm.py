from .database import async_factory, async_engine
from src.models.models import Base


class AsyncOrm():

    @staticmethod
    async def drop_tables() -> None:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @staticmethod
    async def create_tables() -> None:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
