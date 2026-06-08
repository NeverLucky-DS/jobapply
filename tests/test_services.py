"""Тесты сервисов — core бизнес-логика (без внешних зависимостей)."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx


class TestHHService:
    """Тесты hh.ru клиента."""

    @pytest.mark.asyncio
    async def test_search_hh_returns_empty_on_error(self):
        """При HTTP ошибке — возвращает пустой список, не падает."""
        from services.hh import search_hh
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                side_effect=httpx.HTTPError("timeout")
            )
            mock_client.return_value.__aenter__.return_value.__aexit__ = AsyncMock()
            
            result = await search_hh("Python")
            assert result == []

    def test_simplify_handles_missing_fields(self):
        """_simplify не падает на неполных данных."""
        from services.hh import _simplify
        
        vacancy = {"id": "42"}
        result = _simplify(vacancy)
        assert result["id"] == "42"
        assert result["employer"] == "—"
        assert result["salary"] == ""

    def test_fmt_salary_variants(self):
        """Форматирование зарплаты разные варианты."""
        from services.hh import _fmt_salary
        
        assert _fmt_salary({"from": 100, "to": 200, "currency": "USD"}) == "100–200 USD"
        assert _fmt_salary({"from": 100, "currency": "EUR"}) == "от 100 EUR"
        assert _fmt_salary({"to": 200, "currency": "RUB"}) == "до 200 RUB"
        assert _fmt_salary({}) == ""
        assert _fmt_salary(None) == ""


class TestHabrService:
    """Тесты Habr Career клиента."""

    @pytest.mark.asyncio
    async def test_search_habr_returns_empty_on_error(self):
        """При ошибке — пустой список."""
        from services.habr import search_habr
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                side_effect=httpx.HTTPError("fail")
            )
            mock_client.return_value.__aenter__.return_value.__aexit__ = AsyncMock()
            
            result = await search_habr("Python")
            assert result == []


class TestSberParser:
    """Тесты парсера Сбера."""

    def test_detect_level_regex_patterns(self):
        """Регулярки корректно детектят уровень."""
        from services.sber import detect_level, INTERN_RE, JUNIOR_RE, SENIOR_RE

        # Intern patterns
        assert INTERN_RE.search("Стажёр-разработчик")
        assert INTERN_RE.search("Intern position")
        assert INTERN_RE.search("Без опыта работы")

        # Junior patterns
        assert JUNIOR_RE.search("Junior Developer")
        assert JUNIOR_RE.search("Младший инженер")

        # Senior patterns
        assert SENIOR_RE.search("Senior Engineer")
        assert SENIOR_RE.search("Ведущий разработчик")
        assert SENIOR_RE.search("Tech Lead")

    def test_detect_level_filters_correctly(self):
        """detect_level возвращает корректный уровень."""
        from services.sber import detect_level
        
        assert detect_level("Senior Python Developer") is None
        assert detect_level("Tech Lead") is None
        assert detect_level("Python Intern") == "intern"
        assert detect_level("Junior ML Engineer") == "junior"
        assert detect_level("Стажёр-разработчик") == "intern"
