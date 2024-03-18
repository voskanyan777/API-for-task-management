from sqlalchemy import select, insert, update
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
                Task.user_id == user_id)
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

            return formatted_result

    @staticmethod
    def insert_tasks(user_id, task_id, short_name, description, started_in, completed_in, deadline):
        task = Task(
            user_id=user_id,
            task_id=task_id,
            short_name=short_name,
            description=description,
            started_in=started_in,
            completed_in=completed_in,
            deadline=deadline
        )

        with session_factory() as session:
            session.add_all([task])
            session.commit()

    @staticmethod
    def update_task(user_id, task_id, short_name, description, started_in, completed_in, deadline):
        with session_factory() as session:
            session.query(Task).filter_by(task_id=task_id).delete()
            session.commit()

            task = Task(
                user_id=user_id,
                task_id=task_id,
                short_name=short_name,
                description=description,
                started_in=started_in,
                completed_in=completed_in,
                deadline=deadline
            )
            session.add_all([task])
            session.commit()

    @staticmethod
    def delete_task(task_id):
        with session_factory() as session:
            session.query(Task).filter_by(task_id=task_id).delete()
            session.commit()

    @staticmethod
    def completing_tasks(task_id):
        with session_factory() as session:
            query = select(Task).where(Task.task_id == task_id)
            result = session.execute(query).scalars().all()

