"""Автоотклик: preview cover letter + запуск Playwright-апплая."""

import json
from pathlib import Path

from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from services.mistral import generate_cover_letter
from services.applier import apply_hh

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")
PROFILE_PATH = Path(__file__).parent.parent / "profile.json"


def load_profile() -> dict:
    if PROFILE_PATH.exists():
        return json.loads(PROFILE_PATH.read_text())
    return {}


@router.get("/apply", response_class=HTMLResponse)
async def apply_preview(request: Request, url: str, title: str = "", company: str = ""):
    """Страница предпросмотра: генерирует cover letter и предлагает подтвердить."""
    profile = load_profile()
    if not profile.get("name"):
        return HTMLResponse('<meta http-equiv="refresh" content="0;url=/profile">', status_code=302)

    vacancy = {"title": title, "company": company, "url": url}
    try:
        letter = await generate_cover_letter(vacancy, profile)
    except Exception as e:
        letter = f"[Ошибка генерации: {e}]"

    return templates.TemplateResponse(request, "apply_preview.html", {
        "vacancy": vacancy,
        "letter": letter,
        "profile": profile,
    })


@router.post("/apply")
async def do_apply(request: Request, background_tasks: BackgroundTasks):
    """Запускает Playwright-отклик в фоне."""
    data = await request.json()
    url = data.get("url", "")
    letter = data.get("letter", "")
    title = data.get("title", "")
    company = data.get("company", "")

    if not url:
        return JSONResponse({"ok": False, "error": "url required"}, status_code=400)

    background_tasks.add_task(apply_hh, url=url, cover_letter=letter,
                              title=title, company=company)
    return JSONResponse({"ok": True, "message": "Отклик запущен в фоне"})
