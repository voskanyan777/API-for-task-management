from sqlalchemy import select
from .database import session_factory, sync_engine
from src.db.models import Task, Base, User, CompletedTask


class SyncOrm():

    @staticmethod
    def drop_tables() -> None:
        Base.metadata.drop_all(sync_engine)

    @staticmethod
    def create_tables() -> None:
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def select_tasks(user_name: str) -> list:
        with session_factory() as session:
            query = select(User.user_name, Task.short_name, Task.description,
                           Task.deadline).join(User,
                                               User.id == Task.user_id).where(
                Task.user_name == user_name)
            result = session.execute(query).all()
            print(type(result))
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
    def insert_tasks(user_login,task_id, short_name, description=None,
                     started_in=None, completed_in=None, deadline=None,
                     nested_tasks=None):
        task = Task(
            user_login=user_login,
            task_id=task_id,
            short_name=short_name,
            description=description,
            started_in=started_in,
            completed_in=completed_in,
            deadline=deadline,
            nested_tasks=nested_tasks
        )

        with session_factory() as session:
            session.add_all([task])
            session.commit()

    @staticmethod
    def update_task(user_id, task_id, short_name, description, started_in,
                    completed_in, deadline):
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
    def delete_task(user_id, task_id):
        with session_factory() as session:
            session.query(Task).filter_by(task_id=task_id,
                                          user_id=user_id).delete()
            session.commit()

    @staticmethod
    def completing_tasks(user_id, task_id):
        with session_factory() as session:
            query = select(Task).where(Task.task_id == task_id)
            result = session.execute(query).scalars().all()[0]
            session.query(Task).filter_by(task_id=task_id,
                                          user_id=user_id).delete()
            session.commit()

            task = CompletedTask(
                user_id=result.user_id,
                task_id=result.task_id,
                short_name=result.short_name,
                description=result.description,
                started_in=result.started_in,
                completed_in=result.completed_in,
                deadline=result.deadline
            )
            session.add_all([task])
            session.commit()

    @staticmethod
    def add_user(user_name: str, user_email: str, hashed_password: str,
                 user_login: str) -> None:
        user = User(
            user_login=user_login,
            user_name=user_name,
            user_email=user_email,
            hashed_password=hashed_password
        )
        with session_factory() as session:
            session.add_all([user])
            session.commit()

    @staticmethod
    def get_user(email: str) -> list:
        with session_factory() as session:
            query = select(User.user_login, User.user_name,
                           User.user_email).where(User.user_email == email)
            result = session.execute(query).first()
            return result

    @staticmethod
    def get_user_auth(email: str) -> list:
        with session_factory() as session:
            query = select(User.user_name,
                           User.hashed_password,
                           User.user_email,
                           ).where(User.user_email == email)
            result = session.execute(query).first()
            return result