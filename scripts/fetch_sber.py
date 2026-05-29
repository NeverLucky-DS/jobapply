"""CLI: парсит Сбер и upsert в SQLite. Запускать руками или из расписания."""

import asyncio
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlmodel import select
from db import async_session, init_db
from models import Vacancy
from services.sber import fetch_sber


async def upsert(items: list[dict]) -> tuple[int, int]:
    new, upd = 0, 0
    async with async_session() as s:
        for it in items:
            res = await s.execute(
                select(Vacancy).where(
                    Vacancy.source == it["source"],
                    Vacancy.source_id == it["source_id"],
                )
            )
            existing = res.scalar_one_or_none()
            if existing:
                for k, v in it.items():
                    setattr(existing, k, v)
                upd += 1
            else:
                s.add(Vacancy(**it))
                new += 1
        await s.commit()
    return new, upd


async def main():
    await init_db()
    items = await fetch_sber(max_pages=4)
    by_level = Counter(it["level"] for it in items)
    n, u = await upsert(items)
    print(f"sber: всего {len(items)} (intern={by_level.get('intern',0)} junior={by_level.get('junior',0)})  → new={n} upd={u}")


if __name__ == "__main__":
    asyncio.run(main())
