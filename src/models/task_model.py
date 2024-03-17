from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field


class TaskModel(BaseModel):
    user_id: Annotated[int, Field(ge=1)]
    task_id: str
    short_name: str
    description: str
    started_in: datetime
    completed_in: datetime
    deadline: datetime

