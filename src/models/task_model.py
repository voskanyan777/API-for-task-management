from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field


class TaskModel(BaseModel):
    user_id: Annotated[int, Field(ge=1)]
    task_id: str
    short_name: str
    description: str | None = None
    started_in: datetime | None = None
    completed_in: datetime | None = None
    deadline: datetime | None = None
    nested_tasks: dict[str, str] | None = None
