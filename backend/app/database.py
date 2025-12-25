# Conexión DB

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./tasktrack.db"

# motor de base de datos
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# sesión asincrónica
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# base declarativa
Base = declarative_base()
