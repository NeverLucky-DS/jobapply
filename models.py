"""Таблицы БД. Profile хранится в profile.json (проще + не нужна миграция)."""

from datetime import datetime
from sqlmodel import SQLModel, Field, UniqueConstraint


class Vacancy(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("source", "source_id", name="uq_source"),)

    id: int | None = Field(default=None, primary_key=True)
    source: str = Field(index=True)
    source_id: str = Field(index=True)
    title: str
    company: str | None = None
    location: str | None = None
    salary: str | None = None
    level: str | None = Field(default=None, index=True)
    url: str
    published_at: str | None = None
    fetched_at: datetime = Field(default_factory=datetime.utcnow)


class Application(SQLModel, table=True):
    """Трекинг откликов."""
    id: int | None = Field(default=None, primary_key=True)
    vacancy_url: str = Field(index=True, unique=True)
    vacancy_title: str
    company: str | None = None
    source: str  # 'hh' | 'habr' | 'sber' ...
    cover_letter: str | None = None
    status: str = Field(default="sent")  # sent | seen | rejected | interview
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
