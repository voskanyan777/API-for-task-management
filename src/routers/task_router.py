from fastapi import APIRouter, HTTPException, status, Depends
from src.db.orm import SyncOrm
from src.models.task_model import TaskModel
from sqlalchemy.exc import IntegrityError
from src.auth.schemas import UserSchema
from src.auth.auth_jwt import get_current_active_auth_user

task_router = APIRouter(
    prefix='/task',
    tags=['task']
)

syncOrm = SyncOrm()


@task_router.get('/get_user_tasks/')
async def get_tasks(
        user: UserSchema = Depends(get_current_active_auth_user)) -> dict:
    result = syncOrm.select_tasks(user.user_login)
    return {
        'data': result,
        'status': 'ok'
    }


@task_router.post('/add_task')
async def add_user_task(task: TaskModel, user: UserSchema = Depends(
    get_current_active_auth_user)) -> dict:
    task = task.dict()
    task['user_login'] = user.user_login
    try:
        syncOrm.insert_tasks(**task)
    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Задача с таким task_id уже существует'
        )

    return {
        'data': None,
        'status': 'ok'
    }


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
