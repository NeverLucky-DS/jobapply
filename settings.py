"""Конфиг: читает env-переменные, отдаёт типизированный объект."""

from dotenv import load_dotenv
load_dotenv()  # подгружает .env если есть

import os
from dataclasses import dataclass

MISTRAL_API_KEY = os.environ.get("MISTRAL") or os.environ.get("MISTRAL_API_KEY", "")
HH_LOGIN = os.environ.get("HH_LOGIN", "")
HH_PASSWORD = os.environ.get("HH_PASSWORD", "")


@dataclass
class Settings:
    mistral_key: str
    hh_access_token: str
    db_path: str
    app_base_url: str


def load() -> Settings:
    return Settings(
        mistral_key=os.getenv("MISTRAL_API_KEY") or os.getenv("MISTRAL") or "",
        hh_access_token=os.getenv("HH_ACCESS_TOKEN", ""),
        db_path=os.getenv("DB_PATH", "./jobapply.db"),
        app_base_url=os.getenv("APP_BASE_URL", ""),
    )


settings = load()
