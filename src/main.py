import asyncio
import uvicorn
from fastapi import FastAPI
from src.db.async_orm import AsyncOrm
from routers.task_router import task_router

app = FastAPI()
app.include_router(task_router)

asyncOrm = AsyncOrm()


async def main() -> None:
    await asyncOrm.drop_tables()
    await asyncOrm.create_tables()


# @app.on_event('startup')
# async def start_server():
#     await asyncOrm.drop_tables()
#     await asyncOrm.create_tables()
#

if __name__ == '__main__':
    asyncio.run(main())
