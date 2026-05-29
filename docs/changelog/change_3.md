# change_3 — расписание парсинга + SQLite-кэш

**Дата:** 2026-05-29

## Что сделано

### 1. SQLite + SQLModel для кэша вакансий
- Создан `db.py` — async engine + sessionmaker для SQLite (aiosqlite)
- Создан `models.py` — таблица `Vacancy` с полями:
  - `source` (hh.ru / habr / sber)
  - `source_id` — внешний id вакансии
  - `title`, `company`, `location`, `salary`
  - `level` (intern / junior)
  - `url` — уникальный ключ
  - `published_at`, `fetched_at`

### 2. Единый скрипт `scripts/fetch_all.py`
- Параллельно парсит Habr Career (intern + junior, до 100 вакансий)
- Пытается парсить hh.ru API (блокируется 403 из дата-центра — нужен OAuth или прокси)
- Парсит rabota.sber.ru через Playwright (до 2 страниц, ~50 вакансий)
- Делает upsert в SQLite (новые — INSERT, существующие — UPDATE)

### 3. Zo Automation — расписание каждые 2 часа
- Создана автоматизация `FREQ=HOURLY;INTERVAL=2`
- Запускает `.venv/bin/python scripts/fetch_all.py`
- Отправляет отчёт в Telegram только если есть новые вакансии
- Следующий запуск: 2026-05-29 03:44 MSK

### 4. Обновлённые сервисы
- `services/cache.py` — читает из SQLite, возвращает в формате как hh/habr
- `services/sber.py` — Playwright-парсер с пост-фильтрацией уровня по тайтлу
- `routes/vacancies.py` — объединяет hh/habr/sber, сортирует по дате

## Статус источников

| Источник | Метод | Статус |
|----------|-------|--------|
| Habr Career | API (qd[]=1&qid[]=3) | ✅ Работает |
| hh.ru | Публичный API | ❌ 403 (нужен OAuth) |
| Sber | Playwright | ✅ Работает (~2 intern/junior) |
| Ozon | Playwright | ❌ Antibot challenge |
| Alfa | Playwright | ❌ Пустой SSR |
| Telegram | Telethon | ⏳ Нужны credentials |

## Следующие шаги

1. **OAuth для hh.ru** — даст доступ к откликам и полному API
2. **Telegram-парсер** — нужен api_id/api_hash с my.telegram.org/apps
3. **Профиль кандидата** — страница `/profile` для хранения резюме
4. **Генерация cover letter** — интеграция с Mistral через `Skills/resume-tailor`
