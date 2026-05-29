"""CLI: парсит все источники (Habr, hh, Sber) и сохраняет в SQLite."""

import asyncio
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select
from db import async_session, init_db
from models import Vacancy
from services.hh import search_hh
from services.habr import search_habr
from services.sber import fetch_sber


def map_to_model(v: dict, source: str) -> dict:
    """Мапит поля из ответа сервиса в поля модели Vacancy."""
    # Sber уже имеет правильные имена полей
    if source == "sber":
        return v
    # Маппинг для habr/hh: id -> source_id, name -> title, employer -> company, area -> location
    return {
        "source": source,
        "source_id": str(v.get("id", "")),
        "title": v.get("name", v.get("title", "")),
        "company": v.get("employer", v.get("company")),
        "location": v.get("area", v.get("location")),
        "salary": v.get("salary"),
        "level": v.get("level", "junior"),
        "url": v["url"],
        "published_at": v.get("published_at"),
    }


async def fetch_habr_hh():
    """Парсит Habr и hh API, возвращает список dict."""
    items = []
    try:
        habr = await search_habr(text="", levels=["1", "3"], per_page=100)
        items.extend(habr)
        print(f"  habr: {len(habr)}")
    except Exception as e:
        print(f"  habr error: {e}")

    try:
        hh = await search_hh(text="", area=113, experience=["noExperience", "between1And3"], per_page=100)
        items.extend(hh)
        print(f"  hh: {len(hh)}")
    except Exception as e:
        print(f"  hh error: {e}")

    return items


async def upsert_items(items: list[dict], source: str) -> tuple[int, int]:
    """Сохраняет в SQLite, возвращает (new, updated)."""
    new, updated = 0, 0
    async with async_session() as sess:
        for v in items:
            mapped = map_to_model(v, source)
            result = await sess.execute(select(Vacancy).where(Vacancy.url == mapped["url"]))
            existing = result.scalar_one_or_none()
            if existing:
                existing.title = mapped.get("title", "")
                existing.company = mapped.get("company")
                existing.salary = mapped.get("salary")
                existing.location = mapped.get("location")
                existing.level = mapped.get("level", "junior")
                existing.source = source
                existing.source_id = mapped.get("source_id", "")
                existing.published_at = mapped.get("published_at")
                sess.add(existing)
                updated += 1
            else:
                vac = Vacancy(**mapped)
                sess.add(vac)
                new += 1
        await sess.commit()
    return new, updated


async def main():
    await init_db()

    print("→ fetching habr + hh...")
    habr_hh = await fetch_habr_hh()

    new_total, upd_total = 0, 0
    for src in ["hh.ru", "habr"]:
        items = [v for v in habr_hh if v.get("source") == src]
        if items:
            n, u = await upsert_items(items, src)
            print(f"  {src}: new={n} upd={u}")
            new_total += n
            upd_total += u

    print("→ fetching sber...")
    try:
        sber = await fetch_sber()
        if sber:
            n, u = await upsert_items(sber, "sber")
            print(f"  sber: new={n} upd={u}")
            new_total += n
            upd_total += u
    except Exception as e:
        import traceback
        print(f"  sber error: {e}")
        traceback.print_exc()

    print(f"\nИТОГО: новых {new_total}, обновлено {upd_total}")


if __name__ == "__main__":
    asyncio.run(main())
