import uvicorn
from fastapi import FastAPI
from src.db.models import Base
from src.db.orm import SyncOrm
from db.database import sync_engine
from routers.task_router import task_router
from src.auth.auth_jwt import router as auth_router

app = FastAPI()
app.include_router(task_router)
app.include_router(auth_router)


syncOrm = SyncOrm()


@app.on_event('startup')
async def start_server():
    # Base.metadata.drop_all(sync_engine)
    # Base.metadata.create_all(sync_engine)
    #
    pass

if __name__ == '__main__':
    uvicorn.run(app, port=8000)
