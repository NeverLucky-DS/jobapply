"""Профиль кандидата: просмотр и редактирование через форму."""

import json
from pathlib import Path

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")
PROFILE_PATH = Path(__file__).parent.parent / "profile.json"


def load_profile() -> dict:
    if PROFILE_PATH.exists():
        return json.loads(PROFILE_PATH.read_text())
    return {}


def save_profile(data: dict):
    PROFILE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2))


@router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    return templates.TemplateResponse(request, "profile.html", {"profile": load_profile()})


@router.post("/profile")
async def save_profile_route(
    request: Request,
    name: str = Form(""),
    email: str = Form(""),
    phone: str = Form(""),
    telegram: str = Form(""),
    city: str = Form(""),
    target_position: str = Form(""),
    stack: str = Form(""),        # через запятую
    about: str = Form(""),
    experience: str = Form(""),
    education: str = Form(""),
):
    profile = load_profile()
    profile.update({
        "name": name, "email": email, "phone": phone,
        "telegram": telegram, "city": city,
        "target_position": target_position,
        "stack": [s.strip() for s in stack.split(",") if s.strip()],
        "about": about, "experience": experience, "education": education,
    })
    save_profile(profile)
    return RedirectResponse("/profile?saved=1", status_code=303)
