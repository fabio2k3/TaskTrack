# FastAPI appfrom fastapi import FastAPI

from fastapi import FastAPI
from .database import engine, Base

app = FastAPI(title="TaskTrack API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
def health_check():
    return {"status": "ok"}
