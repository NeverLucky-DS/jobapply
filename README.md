# jobapply — автоотклики на ML-вакансии

Автоматизация поиска и откликов на вакансии для ML-стажёров и Junior Data Scientists.

## Возможности

- **Поиск вакансий** — Habr Career, hh.ru, Сбербанк (Playwright-парсер)
- **Фильтр по уровню** — только стажёрские и Junior позиции
- **Генерация cover letter** — через Mistral AI под конкретную вакансию
- **Профиль кандидата** — хранение резюме, стека, опыта
- **Автоотклик** — Playwright-автоматизация подачи заявок на hh.ru
- **Telegram-уведомления** — о новых вакансиях по расписанию

## Стек

- **Backend**: FastAPI + SQLModel + SQLite
- **Frontend**: Jinja2 + HTMX + Tailwind CSS (CDN)
- **AI**: Mistral API (cover letter generation)
- **Browser automation**: Playwright (Sber parser, hh.ru auto-apply)
- **Scheduling**: Zo Automations

## Структура проекта

```
jobapply/
├── app.py              # FastAPI entrypoint
├── settings.py         # Конфигурация
├── models.py           # SQLModel-модели
├── db.py               # Async SQLite engine
├── routes/
│   ├── home.py         # Лендинг
│   ├── vacancies.py    # Поиск вакансий
│   ├── profile.py      # Профиль кандидата
│   └── apply.py        # Автоотклик
├── services/
│   ├── hh.py           # hh.ru API client
│   ├── habr.py         # Habr Career API client
│   ├── sber.py         # Sber Playwright parser
│   ├── cache.py        # SQLite cache layer
│   ├── mistral.py      # Cover letter generation
│   └── applier.py      # Playwright auto-apply
├── scripts/
│   ├── fetch_all.py    # Парсинг всех источников
│   └── fetch_sber.py   # Парсинг Сбера
├── web/
│   ├── templates/      # Jinja2-шаблоны
│   └── static/         # CSS, JS
├── profile.json        # Профиль кандидата
└── pyproject.toml      # Зависимости
```

## Установка

```bash
# Клонировать репозиторий
git clone https://github.com/YOUR_USERNAME/jobapply.git
cd jobapply

# Создать виртуальное окружение
uv venv .venv
source .venv/bin/activate

# Установить зависимости
uv pip install -e .

# Установить Playwright и браузер
playwright install chromium
playwright install-deps chromium

# Создать .env файл
cat > .env << ENVEOF
MISTRAL=your_mistral_api_key
HH_LOGIN=your_hh_login        # опционально, для автоотклика
HH_PASSWORD=your_hh_password  # опционально, для автоотклика
ENVEOF

# Запустить
uvicorn app:app --reload
```

## Использование

### 1. Заполнить профиль

Откройте `/profile` и заполните:
- Контактные данные
- Целевую позицию
- Стек технологий
- Опыт работы
- Образование

### 2. Искать вакансии

На странице `/vacancies`:
- Введите ключевые слова (Python, ML, Data Scientist)
- Выберите уровень (Стажёр, Junior, или оба)
- Вакансии подтягиваются из Habr Career + hh.ru + Sber

### 3. Откликаться

На каждой вакансии — кнопка **«✦ Откликнуться»**:
1. Генерируется персонализированное cover letter через Mistral
2. Можно отредактировать или перегенерировать
3. **Автоотклик** — если настроены `HH_LOGIN` + `HH_PASSWORD`
4. **Вручную** — письмо копируется в буфер, открывается страница вакансии

### 4. Автоматический парсинг

Настроен scheduler (каждые 2 часа):
- Парсит новые вакансии с всех источников
- Фильтрует по уровню
- Сохраняет в SQLite
- Шлёт summary в Telegram

## API источники

| Источник | Метод | Ограничения |
|----------|-------|-------------|
| Habr Career | REST API | Без ограничений |
| hh.ru | REST API | Нужен OAuth (заявка #22500 pending) |
| Сбербанк | Playwright | SPA, рендерится браузером |

## HH.ru OAuth

Заявка на приложение отправлена (#22500). После одобрения:
- `HH_CLIENT_ID` и `HH_CLIENT_SECRET` будут в Settings → Advanced
- OAuth-токен сохранится в `hh_token.json`
- Отклики через API `/negotiations` без Playwright

## Конфигурация

Все секреты — в `.env` или [Zo → Settings → Advanced](/?t=settings&s=advanced):

| Переменная | Описание |
|------------|----------|
| `MISTRAL` | API-ключ Mistral AI |
| `HH_LOGIN` | Логин hh.ru (для Playwright auto-apply) |
| `HH_PASSWORD` | Пароль hh.ru |
| `HH_CLIENT_ID` | OAuth client ID (после одобрения заявки) |
| `HH_CLIENT_SECRET` | OAuth client secret |

## Лицензия

MIT

---

Built with ❤️ on [Zo Computer](https://zo.computer)
