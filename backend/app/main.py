from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, Field
from datetime import datetime, date

# -------------------------
# DATABASE SETUP
# -------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasktrack.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -------------------------
# DATABASE MODELS
# -------------------------
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    task_date = Column(Date, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# -------------------------
# Pydantic MODELS
# -------------------------
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    task_date: date = Field(..., description="Fecha de la tarea (YYYY-MM-DD)")

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    task_date: date | None = None
    completed: bool | None = None

class TaskResponse(TaskCreate):
    id: int
    completed: bool
    created_at: datetime

    model_config = {"from_attributes": True}

# -------------------------
# DEPENDENCIES
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# APP INSTANCE
# -------------------------
app = FastAPI(title="TaskTrack API", version="1.0")

# -------------------------
# ROUTES
# -------------------------

# CREATE TASK
@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# READ TASKS (filters + sorting)
@app.get("/tasks", response_model=list[TaskResponse])
def read_tasks(
    completed: bool | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    sort_by: str = Query("task_date"),
    db: Session = Depends(get_db)
):
    query = db.query(Task)

    if completed is not None:
        query = query.filter(Task.completed == completed)
    if start_date:
        query = query.filter(Task.task_date >= start_date)
    if end_date:
        query = query.filter(Task.task_date <= end_date)

    if sort_by == "title":
        query = query.order_by(Task.title)
    else:
        query = query.order_by(Task.task_date)

    return query.all()

# READ SINGLE TASK
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# UPDATE TASK
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

# MARK TASK AS COMPLETE
@app.put("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = True
    db.commit()
    db.refresh(task)
    return task

# DELETE TASK
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}
