"""FastAPI точка входа."""
from dotenv import load_dotenv
load_dotenv(override=True)

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from db import init_db
from routes import home, vacancies, profile, apply as apply_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="jobapply", docs_url="/api/docs", redoc_url=None, lifespan=lifespan)
app.mount("/static", StaticFiles(directory="web/static"), name="static")

app.include_router(home.router)
app.include_router(vacancies.router)
app.include_router(profile.router)
app.include_router(apply_route.router)


@app.get("/healthz")
async def healthz():
    return {"ok": True}
