# Pydantic schemas

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True
