"""Клиент Habr Career — неофициальный frontend-API. Работает без авторизации.

Уровни (qid):
  1 — Стажёр (Intern)
  3 — Младший (Junior)
  5 — Средний (Middle)
  6 — Старший (Senior)
  7 — Ведущий (Lead)
"""

import logging

import httpx

HABR_API = "https://career.habr.com/api/frontend/vacancies"
UA = "Mozilla/5.0 (compatible; jobapply/0.1)"

log = logging.getLogger(__name__)


async def search_habr(
    text: str,
    levels: list[int] | None = None,
    per_page: int = 30,
) -> list[dict]:
    """Поиск вакансий на career.habr.com. При ошибке — пустой список."""
    params: list[tuple[str, str | int]] = [
        ("q", text),
        ("sort", "date"),
        ("type", "all"),
        ("page", 1),
    ]
    for q in levels or []:
        params.append(("qid[]", q))
    try:
        async with httpx.AsyncClient(timeout=15, headers={"User-Agent": UA}) as client:
            r = await client.get(HABR_API, params=params)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        log.warning("habr search failed: %s", e)
        return []
    return [_simplify(v) for v in (data.get("list") or [])[:per_page]]


def _simplify(v: dict) -> dict:
    company = v.get("company") or {}
    pub = v.get("publishedDate") or {}
    divisions = v.get("divisions") or []
    skills = v.get("skills") or []
    tags = [d.get("title") for d in divisions if d.get("title")][:1]
    tags += [s.get("title") for s in skills if s.get("title")][:4]
    snippet = " · ".join(tags) if tags else ""
    return {
        "source": "habr",
        "id": str(v.get("id") or ""),
        "name": v.get("title") or "",
        "employer": company.get("title") or "—",
        "area": "Удалённо" if v.get("remoteWork") else "—",
        "experience": "—",
        "schedule": "Удалёнка" if v.get("remoteWork") else "—",
        "salary": _fmt_salary(v),
        "published_at": (pub.get("date") or "")[:10],
        "url": f"https://career.habr.com{v.get('href')}" if v.get("href") else "",
        "apply_url": None,
        "snippet": snippet,
    }


def _fmt_salary(v: dict) -> str:
    s = v.get("salary") or {}
    if s.get("formatted"):
        return s["formatted"]
    p = v.get("predictedSalary") or {}
    if p.get("formatted"):
        return p["formatted"] + " ~"
    return ""
