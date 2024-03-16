from fastapi import APIRouter
from src.db.orm import SyncOrm

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
