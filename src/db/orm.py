from sqlalchemy import select
from src.db.database import session_factory, sync_engine
from ..models.models import Task, Base, User


class SyncOrm():

    @staticmethod
    def drop_tables() -> None:
        Base.metadata.drop_all(sync_engine)

    @staticmethod
    def create_tables() -> None:
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def select_tasks(user_id: int) -> list:
        with session_factory() as session:
            query = select(User.user_name, Task.short_name, Task.description, Task.deadline).join(User,
                                                                                                  User.id == Task.user_id).where(
                User.id == user_id)
            result = session.execute(query).all()

            # Создание списка словарей из результатов
            formatted_result = []
            for row in result:
                formatted_result.append({
                    'user_name': row[0],
                    'short_name': row[1],
                    'description': row[2],
                    'deadline': row[3]
                })

            print(formatted_result)
            return formatted_result


