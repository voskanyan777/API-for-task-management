from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,  # Логирование
)

async_enige = create_async_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True
)

session_factory = sessionmaker(sync_engine)
