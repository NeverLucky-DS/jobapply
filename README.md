# jobapply — agent pipeline для поиска работы

Автоматизация для ML/DS стажировок: сбор вакансий → фильтр по уровню → cover letter (Mistral) → действие в браузере (Playwright).

---

## Зачем этот проект (агенты / backend)

MVP **агентского pipeline**: perceive → decide → generate → act.

| Навык | Реализация |
|-------|------------|
| Python | FastAPI, services layer |
| FastAPI | REST + Jinja/HTMX UI, `/api/docs` |
| Тесты | pytest (detect_level, health) |
| LLM | Mistral — персонализированные cover letters |
| Async | async FastAPI, async Playwright, aiosqlite |
| Git | структура routes → services |

**Источники:** Habr Career API, hh.ru API, career portal (Playwright SPA).

---

## Стек

- FastAPI + SQLModel + async SQLite
- Mistral API
- Playwright (async)
- Jinja2 + HTMX

---

## Быстрый старт

```bash
uv venv .venv && source .venv/bin/activate
uv pip install -e .
playwright install chromium
cp .env.example .env  # MISTRAL, опционально HH_*
uvicorn app:app --reload
```

---

## Архитектура

```
sources (habr / hh / playwright) → filter (level) → mistral (letter) → applier (browser)
                                              ↓
                                         SQLite log
```

---

## Скриншоты

```markdown
![Вакансии](docs/screenshots/vacancies.png)
```

| Файл | Что снять |
|------|-----------|
| `vacancies.png` | страница поиска вакансий |
| `cover-letter.png` | сгенерированное письмо |
| `apply-flow.png` | preview перед откликом |

Папка `docs/screenshots/`, формат PNG/JPG.
