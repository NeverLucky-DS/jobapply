"""Главная и /about."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services.sources import SOURCES

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    stats = {
        "tg_channels": sum(1 for s in SOURCES if s["kind"] == "tg"),
        "job_boards": sum(1 for s in SOURCES if s["kind"] == "board"),
        "company_sites": sum(1 for s in SOURCES if s["kind"] == "company"),
        "total": len(SOURCES),
    }
    return templates.TemplateResponse(
        request, "home.html", {"stats": stats, "sources": SOURCES[:8]}
    )
