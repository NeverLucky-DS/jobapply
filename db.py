"""SQLite + SQLModel async — единая точка для движка и сессий."""

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./jobapply.db"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Создаёт таблицы, если их ещё нет."""
    import models  # noqa: F401  — регистрируем модели
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
