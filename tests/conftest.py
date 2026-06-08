"""Конфигурация pytest."""

import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import asyncio
import pytest

# pytest-asyncio конфигурация
pytest_plugins = ('pytest_asyncio',)


@pytest.fixture(scope="session")
def event_loop():
    """Создаём event loop для async тестов."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def mock_env():
    """Мокаем переменные окружения для тестов."""
    import os
    original = os.environ.copy()

    # Устанавливаем тестовые значения
    os.environ.setdefault("MISTRAL", "test-mistral-key")
    os.environ.setdefault("HH_LOGIN", "")
    os.environ.setdefault("HH_PASSWORD", "")

    yield

    # Восстанавливаем оригинальные значения
    os.environ.clear()
    os.environ.update(original)
