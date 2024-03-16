import uvicorn
from fastapi import FastAPI
from models.models import Base
from db.database import sync_engine

app = FastAPI()

if __name__ == '__main__':
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
