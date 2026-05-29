"""Поиск вакансий: hh.ru + Habr Career, фильтр по уровню (intern/junior)."""

import asyncio
import re

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services.hh import search_hh
from services.habr import search_habr
from services.cache import search_cached

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")

# Маппинг level -> параметры источников
LEVEL_MAP = {
    "intern":  {"habr": [1],    "hh": ["noExperience"]},
    "junior":  {"habr": [3],    "hh": ["noExperience", "between1And3"]},
    "starter": {"habr": [1, 3], "hh": ["noExperience"]},  # дефолт: стажёр + джун
}

# Стоп-слова: убираем мидлов/сеньоров/лидов даже если просочились
STOP_WORDS = re.compile(
    r"\b(senior|lead|principal|staff|head|chief|director|архитектор|"
    r"руководитель|ведущ|старш|тимлид|team\s*lead)\b",
    re.IGNORECASE,
)


def _drop_senior(items: list[dict]) -> list[dict]:
    return [v for v in items if not STOP_WORDS.search(v.get("title", ""))]


@router.get("/vacancies", response_class=HTMLResponse)
async def vacancies_page(
    request: Request,
    q: str = "ML",
    area: int = 113,
    level: str = "starter",
):
    """Стажёрские/джуновские вакансии из hh.ru + Habr Career."""
    cfg = LEVEL_MAP.get(level, LEVEL_MAP["starter"])
    levels = ["intern", "junior"] if level == "starter" else [level]
    hh_items, habr_items, cached_items = await asyncio.gather(
        search_hh(text=q, area=area, experience=cfg["hh"], per_page=20),
        search_habr(text=q, levels=cfg["habr"], per_page=20),
        search_cached(text=q, levels=levels, limit=30),
    )
    items = _drop_senior(hh_items + habr_items + cached_items)
    items.sort(key=lambda v: v.get("published_at", ""), reverse=True)
    ctx = {
        "items": items,
        "q": q,
        "area": area,
        "level": level,
        "total": len(items),
        "hh_count": len([v for v in items if v.get("source") == "hh.ru"]),
        "habr_count": len([v for v in items if v.get("source") == "habr"]),
        "corp_count": len([v for v in items if v.get("source") in ("sber", "ozon", "alfa")]),
    }
    if request.headers.get("hx-request") == "true":
        return templates.TemplateResponse(request, "_vacancy_list.html", ctx)
    return templates.TemplateResponse(request, "vacancies.html", ctx)
