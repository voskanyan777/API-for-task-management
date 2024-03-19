from fastapi import APIRouter, HTTPException, status
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
        'data': result,
        'status': 'ok'
    }


@task_router.post('/add_task')
async def add_user_task(task: TaskModel):
    try:
        syncOrm.insert_tasks(**task.dict())
        return {
            'data': None,
            'status': 'ok'
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Задача с таким task_id уже существует'
        )


@task_router.put('/update_task')
async def update_task(task: TaskModel):
    syncOrm.update_task(**task.dict())
    return {
        'data': None,
        'status': 'ok'
    }


@task_router.delete('/delete_task/{user_id}/{task_id}')
async def delete_task(user_id: int, task_id: str):
    syncOrm.delete_task(user_id, task_id)
    return {
        'data': None,
        'status': 'ok'
    }


@task_router.get('/completing_tasks/{user_id}/{task_id}')
async def completing_tasks(user_id: int, task_id: str):
    syncOrm.completing_tasks(user_id, task_id)
    return {
        'data': None,
        'status': 'ok'
    }
