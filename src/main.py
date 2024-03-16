import uvicorn
from fastapi import FastAPI
from models.models import Base
from db.database import sync_engine

app = FastAPI()


@app.on_event('startup')
async def start_server():
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)


if __name__ == '__main__':
    uvicorn.run(app)
