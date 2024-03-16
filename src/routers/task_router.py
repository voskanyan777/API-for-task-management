from fastapi import APIRouter
from src.db.orm import SyncOrm
from src.models.task_model import TaskModel

task_router = APIRouter(
    prefix='/task',
    tags=['task']
)

syncOrm = SyncOrm()


@task_router.get('/get_user_tasks/{user_id}')
async def get_tasks(user_id: int) -> dict:
    result = syncOrm.select_tasks(user_id)
    return {
        'data': result
    }


@task_router.post('/add_task')
async def add_user_task(task: TaskModel):
    syncOrm.insert_tasks(**task.dict())
    return {
        'data': None,
        'status': 'ok'
    }

@task_router.put('/update_task')
async def update_task():
    syncOrm.update_task()
    return {
        'data': None,
        'status': 'ok'
    }