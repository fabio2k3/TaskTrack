from pydantic import BaseModel, Field
from datetime import date, datetime

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    task_date: date

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    task_date: date | None = None
    completed: bool | None = None

class Task(TaskBase):
    id: int
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2
