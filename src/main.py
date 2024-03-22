import uvicorn
from fastapi import FastAPI
from models.models import Base
from src.db.orm import SyncOrm
from db.database import sync_engine
from routers.task_router import task_router

app = FastAPI()
app.include_router(task_router)

syncOrm = SyncOrm()


@app.on_event('startup')
async def start_server():
    # Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
