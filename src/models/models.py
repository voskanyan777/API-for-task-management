from datetime import datetime
from typing import Annotated
from sqlalchemy import String, text, JSON, UniqueConstraint, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]
task_short_name = Annotated[str, mapped_column(String(90), nullable=False)]


# Базовый класс
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        (UniqueConstraint('user_email'),)
    )
    id: Mapped[intpk]
    user_name: Mapped[str] = mapped_column(String(40), nullable=False)
    user_email: Mapped[str] = mapped_column(String(90), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    registered_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = (
        UniqueConstraint('user_id', 'task_id', name='unique_user_task_id'),
    )
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    task_id: Mapped[str] = mapped_column(nullable=False)
    short_name: Mapped[task_short_name]
    description: Mapped[str] = mapped_column(nullable=True)
    started_in: Mapped[datetime] = mapped_column(nullable=True)
    completed_in: Mapped[datetime] = mapped_column(nullable=True)
    deadline: Mapped[datetime] = mapped_column(nullable=True)
    nested_tasks = mapped_column(JSON)


class CompletedTask(Base):
    __tablename__ = 'completed_tasks'
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    task_id: Mapped[str] = mapped_column(nullable=False)
    short_name: Mapped[task_short_name]
    description: Mapped[str] = mapped_column(nullable=True)
    started_in: Mapped[datetime] = mapped_column(nullable=True)
    completed_in: Mapped[datetime] = mapped_column(nullable=True)
    deadline: Mapped[datetime] = mapped_column(nullable=True)
    nested_tasks = mapped_column(JSON)
