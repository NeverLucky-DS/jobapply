"""Чтение кэшированных вакансий из SQLite в общем формате (как у hh/habr)."""

from sqlmodel import select
from sqlalchemy import func, or_
from db import async_session
from models import Vacancy

_LVL = {"intern": "Стажёр", "junior": "Junior"}


async def search_cached(text: str = "", levels: list[str] | None = None, limit: int = 50) -> list[dict]:
    """Вернёт вакансии из БД в shape, совместимом с hh/habr (поля name/employer/area/...)."""
    levels = levels or ["intern", "junior"]
    async with async_session() as s:
        stmt = select(Vacancy).where(Vacancy.level.in_(levels))
        if text.strip():
            like = f"%{text.strip().lower()}%"
            stmt = stmt.where(or_(
                func.lower(Vacancy.title).like(like),
                func.lower(Vacancy.company).like(like),
            ))
        stmt = stmt.order_by(Vacancy.fetched_at.desc()).limit(limit)
        rows = (await s.execute(stmt)).scalars().all()
    return [{
        "source": v.source,
        "id": f"{v.source}:{v.source_id}",
        "url": v.url,
        "name": v.title,
        "employer": v.company or "—",
        "area": v.location or "—",
        "experience": _LVL.get(v.level or "", "—"),
        "schedule": "—",
        "salary": v.salary or "",
        "snippet": "",
        "published_at": v.published_at or "",
    } for v in rows]
