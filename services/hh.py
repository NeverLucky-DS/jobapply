"""Клиент hh.ru — публичный поиск без OAuth.

Внимание: api.hh.ru блокирует дата-центровые IP (403). На проде нужен OAuth-токен
или исходящий прокси. Сейчас при ошибке возвращаем пустой список и не падаем.
"""

import logging

import httpx

HH_API = "https://api.hh.ru/vacancies"
UA = "jobapply/0.1 (yondo565@gmail.com)"

log = logging.getLogger(__name__)


async def search_hh(
    text: str,
    area: int = 113,
    experience: list[str] | None = None,
    per_page: int = 30,
) -> list[dict]:
    """Возвращает вакансии hh.ru в упрощённом формате. При ошибке — []."""
    params: list[tuple[str, str | int]] = [
        ("text", text),
        ("area", area),
        ("order_by", "publication_time"),
        ("per_page", per_page),
    ]
    for e in experience or ["noExperience"]:
        params.append(("experience", e))
    try:
        async with httpx.AsyncClient(timeout=15, headers={"User-Agent": UA}) as client:
            r = await client.get(HH_API, params=params)
            r.raise_for_status()
            raw = r.json().get("items", [])
    except httpx.HTTPError as e:
        log.warning("hh.ru search failed: %s", e)
        return []
    return [_simplify(v) for v in raw]


def _simplify(v: dict) -> dict:
    salary = v.get("salary") or {}
    return {
        "source": "hh.ru",
        "id": v.get("id"),
        "name": v.get("name"),
        "employer": (v.get("employer") or {}).get("name") or "—",
        "area": (v.get("area") or {}).get("name") or "—",
        "experience": (v.get("experience") or {}).get("name") or "—",
        "schedule": (v.get("schedule") or {}).get("name") or "—",
        "salary": _fmt_salary(salary),
        "published_at": (v.get("published_at") or "")[:10],
        "url": v.get("alternate_url"),
        "apply_url": v.get("apply_alternate_url"),
        "snippet": (v.get("snippet") or {}).get("requirement") or "",
    }


def _fmt_salary(s: dict) -> str:
    if not s:
        return ""
    lo, hi, cur = s.get("from"), s.get("to"), s.get("currency") or ""
    if lo and hi:
        return f"{lo:,}–{hi:,} {cur}".replace(",", " ")
    if lo:
        return f"от {lo:,} {cur}".replace(",", " ")
    if hi:
        return f"до {hi:,} {cur}".replace(",", " ")
    return ""
