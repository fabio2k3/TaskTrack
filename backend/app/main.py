# FastAPI appfrom fastapi import FastAPI

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from . import models, schemas, crud

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskTrack API")


# Dependency: DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/tasks", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    return crud.create_task(db, task)


@app.get("/tasks", response_model=list[schemas.Task])
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)


@app.put("/tasks/{task_id}", response_model=schemas.Task)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.complete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
