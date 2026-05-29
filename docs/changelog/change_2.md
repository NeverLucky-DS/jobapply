# change_2 — фильтр по уровню + корп-парсер Сбера

## Что сделано

### Фильтр по уровню (intern / junior)
- `services/hh.py`: параметр `experience` стал списком, передаётся несколькими `experience=` в URL — hh API это поддерживает.
- `services/habr.py`: новый параметр `levels` — список qid Habr (1=intern, 3=junior, 5=middle, 6=senior, 7=lead), пробрасывается как `qid[]=...`.
- `routes/vacancies.py`: новый параметр `?level=intern|junior|starter` (дефолт `starter` = intern + junior).
  Маппинг `LEVEL_MAP` → параметры hh/habr.
  Пост-фильтр `_drop_senior` дополнительно режет всё, где в title встречается `senior|lead|principal|head|архитектор|руководитель|ведущий|старший|тимлид` — на случай, если что-то просочится из API.
- UI: селект в форме `/vacancies` теперь выбирает уровень, а не «опыт hh».

Проверка на запросе `Python`: 20 вакансий, 0 senior-like, все intern/junior.

### Корп-парсер Сбера (Phase 1, Browser-based)
- Поставлен `playwright` + Chromium headless (`.venv` проекта, ~250 MB).
- `db.py` — SQLite (`jobapply.db`) + SQLModel async, функция `init_db()`.
- `models.py` — таблица `Vacancy(source, source_id, title, company, location, level, url, ...)` с уникальным индексом по `(source, source_id)`.
- `services/sber.py` — Playwright headless. Открывает `rabota.sber.ru/search/?page=N`, ждёт карточки, через `page.evaluate` вытаскивает `[title, href, location, company]` со всех `[class*="styled__Card"]`.
  - URL-фильтр `?type=internship|junior` у Сбера **не работает** — отдаёт всё подряд.
  - Поэтому уровень определяем регэкспами по заголовку (`detect_level`): сначала отсекаем senior/lead/архитектор/ведущий, потом ищем intern/junior-маркеры.
- `services/cache.py` — `search_cached(text, levels, limit)` — читает из БД в общем формате (shape как у hh/habr), чтобы шаблон `_vacancy_list.html` работал без условий по источнику.
- `routes/vacancies.py` — добавлен 3-й параллельный запрос к `search_cached`, новый счётчик `corp_count`.
- `scripts/fetch_sber.py` — CLI: открывает Сбер, парсит 4 страницы (200 карточек), оставляет только intern/junior, upsert в БД.
- Шаблон `_vacancy_list.html` — бейджи источников по цветам: hh.ru фиолетовый, habr мятный, **sber изумрудный**, ozon голубой, alfa красный.

Запуск парсера: `cd Projects/jobapply && .venv/bin/python scripts/fetch_sber.py`.
По состоянию на сейчас у Сбера 2 intern, 0 junior из 200 просмотренных карточек — реально пусто.

## Что не сделано (Phase 2)
- Ozon (`job.ozon.ru`) — 307 + cookie challenge, нужен Playwright с прохождением challenge.
- Alfa (`job.alfabank.ru`) — 200 OK, `__NEXT_DATA__` пустой, рендерится клиентом → Playwright нужен.
- sbergraduate.ru — отдельный стажёрский портал Сбера, скорее всего гораздо больше intern-вакансий.
- Расписание парсинга (cron / Zo automation) — пока запуск ручной.
- Профиль, резюме, сопроводительные через Mistral, авто-отклик.
