from datetime import datetime
from typing import Annotated
from sqlalchemy import String, text, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]
task_short_name = Annotated[str, mapped_column(String(90), nullable=False)]


# Базовый класс
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        (UniqueConstraint('user_email'), )
    )
    id: Mapped[intpk]
    user_name: Mapped[str] = mapped_column(String(40), nullable=False)
    user_email: Mapped[str] = mapped_column(String(90), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    registered_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[intpk]
    short_name: Mapped[task_short_name]
    description: Mapped[str]
    started_in: Mapped[datetime]
    completed_in: Mapped[datetime]
    deadline: Mapped[datetime]
    nested_tasks = mapped_column(JSON)


class CompletedTask(Base):
    __tablename__ = 'completed_tasks'
    id: Mapped[intpk]
    short_name: Mapped[task_short_name]
    description: Mapped[str]
    started_in: Mapped[datetime]
    completed_in: Mapped[datetime]
    deadline: Mapped[datetime]
    nested_tasks = mapped_column(JSON)
