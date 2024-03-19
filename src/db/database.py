from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,  # Логирование
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)

session_factory = sessionmaker(sync_engine)
async_factory = async_sessionmaker(async_engine)
