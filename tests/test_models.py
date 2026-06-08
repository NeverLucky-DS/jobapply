"""Тесты моделей и БД."""

import pytest
from datetime import datetime
from models import Vacancy, Application


class TestVacancyModel:
    """Тесты модели Vacancy."""

    def test_vacancy_creation(self):
        """Создание вакансии с валидными данными."""
        vacancy = Vacancy(
            source="hh.ru",
            source_id="12345",
            title="Python Developer",
            company="Test Company",
            location="Москва",
            salary="100-150k RUB",
            level="intern",
            url="https://hh.ru/vacancy/12345",
        )

        assert vacancy.source == "hh.ru"
        assert vacancy.source_id == "12345"
        assert vacancy.title == "Python Developer"
        assert vacancy.level == "intern"

    def test_vacancy_defaults(self):
        """Поля vacancy имеют корректные defaults."""
        vacancy = Vacancy(
            source="habr",
            source_id="42",
            title="Test",
            url="https://career.habr.com/vacancies/42",
        )

        assert vacancy.id is None  # Не сохранён в БД
        assert vacancy.level is None
        assert vacancy.fetched_at is not None


class TestApplicationModel:
    """Тесты модели Application."""

    def test_application_creation(self):
        """Создание отклика."""
        app = Application(
            vacancy_url="https://hh.ru/vacancy/123",
            vacancy_title="ML Intern",
            company="Сбер",
            source="hh",
            cover_letter="Тестовое письмо",
        )

        assert app.status == "sent"
        assert app.applied_at is not None
        assert app.updated_at is not None

    def test_application_status_values(self):
        """Допустимые значения статуса."""
        valid_statuses = ["sent", "seen", "rejected", "interview"]

        for status in valid_statuses:
            app = Application(
                vacancy_url="https://test.com",
                vacancy_title="Test",
                source="test",
                status=status,
            )
            assert app.status == status


class TestDatabase:
    """Интеграционные тесты БД."""

    @pytest.mark.asyncio
    async def test_init_db_creates_tables(self):
        """init_db создаёт таблицы в БД."""
        from sqlalchemy import text
        from db import init_db, engine
        
        await init_db()
        
        async with engine.begin() as conn:
            # Проверяем что таблицы созданы
            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result]
            
        assert "vacancy" in tables
        assert "application" in tables
