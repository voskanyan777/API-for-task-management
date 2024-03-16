from sqlalchemy import select
from database import session_factory, sync_engine
from ..models.models import Task, Base


class SyncOrm():

    @staticmethod
    def drop_tables() -> None:
        Base.metadata.drop_all(sync_engine)

    @staticmethod
    def create_tables() -> None:
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def select_tasks() -> tuple: