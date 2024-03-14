from datetime import datetime
from typing import Annotated
from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]


# Базовый класс
class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'Users'
    id: Mapped[intpk]
    user_name: Mapped[str] = mapped_column(String(40), nullable=False)
    user_email: Mapped[str] = mapped_column(String(90), nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    registered_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class Notes(Base):
    __tablename__ = 'Notes'
    id: Mapped[intpk]
    short_name: Mapped[str] = mapped_column(String(90), nullable=False)
    description: Mapped[str]
    deadline: Mapped[datetime]