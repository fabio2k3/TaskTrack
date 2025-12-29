from pydantic import BaseModel
from datetime import date, datetime

class TaskBase(BaseModel):
    title: str
    description: str | None = None

class TaskCreate(TaskBase):
    pass   # 👈 NO pedimos date

class Task(TaskBase):
    id: int
    date: date
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True
