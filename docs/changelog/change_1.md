# change_1 — стартовый каркас

## Что сделано

- Скелет FastAPI-проекта: `app.py`, `settings.py`, `routes/`, `services/`, `web/`.
- Лендинг (`/`) с hero, метриками источников, объяснением «как работает» и сеткой подключённых источников.
- Страница `/vacancies` — живой поиск по публичному API hh.ru через HTMX, без перезагрузки.
- `services/hh.py` — async-клиент hh.ru (поиск, упрощённое представление вакансии).
- `services/sources.py` — реестр источников для лендинга и будущего воркера.
- `web/templates/base.html` + `main.css` + `three-bg.js` — Three.js облако точек на фоне, premium-типографика, тёмная тема.
- `docs/sources.md` — полная карта источников вакансий ML/DS.
- `pyproject.toml` с минимальным набором: FastAPI, httpx, jinja2, sqlmodel, aiosqlite, mistralai.
- `.env.example` — конфиг с Mistral, hh OAuth, Telethon.

## Почему так

- **FastAPI + Jinja + HTMX, без SPA** — соответствует правилам проекта, быстрый старт, server-rendered.
- **Tailwind через Play CDN** — на старте проще, позже мигрируем на CLI, когда зафиксируем дизайн.
- **Three.js через ESM CDN** — не тянем сборщик, фон lazy, частицы выключаются при `prefers-reduced-motion`.
- **hh.ru без OAuth** — публичного API хватает для поиска; OAuth нужен только для самих откликов, добавлю отдельно.
- **БД не подключена** — пока нет персистентного state, добавлю в `change_2`, когда появится профиль/история откликов.

## Дальше

- `change_2`: SQLite + SQLModel, модели `Profile`, `Vacancy`, `Application`, история поисков.
- `change_3`: hh.ru OAuth, форма профиля, кнопка «откликнуться» с Mistral cover letter.
- `change_4`: фоновый воркер парсинга (mode=process) + Telethon для TG-каналов.
