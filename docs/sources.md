# Источники вакансий ML/DS стажёр

Полный реестр источников с механикой парсинга. Используется как референс для воркера и для лендинга (`services/sources.py`).

## 1. Telegram — агрегаторы

| Канал | Ссылка | Частота | Фильтр |
|---|---|---|---|
| Machine Learning Jobs | https://t.me/machinelearning_jobs | 5–15/день | ML/DS/MLOps |
| AI Jobs | https://t.me/ai_jobs | 2–5/день | AI/LLM |
| Datascience Jobs | https://t.me/datascience_jobs | 2–5/день | DS/Analytics |

@machinelearning_jobs — самый живой, постят работодатели напрямую. **Чтение через Telethon**: `client.iter_messages(channel, offset_date=last_check)`.

## 2. Telegram — студенческие/стажировки

| Канал | Что там |
|---|---|
| Поступашки (вакансии) | стажировки, конкурсы |
| ВРаботе студентам | вакансии для студентов |
| Young Meetup IT | IT-стажировки, мероприятия |
| DataCraft | data-сообщество |

Часто первыми публикуют открытие новых программ (Авито ААА, Яндекс ШАР, Сбер) — раньше официальных сайтов.

## 3. Telegram — официальные HR компаний

| Компания | Канал |
|---|---|
| Яндекс | https://t.me/yandex_jobs |
| Сбер | https://t.me/sber_jobs |
| Авито | https://t.me/avito_jobs |
| Ozon | https://t.me/ozon_jobs |
| МТС | https://t.me/mts_jobs |
| Альфа-Банк | https://t.me/alfabank_jobs |
| T-Bank | https://t.me/tbank_jobs |
| Positive Technologies | https://t.me/positive_technologies |

Эксклюзивные программы, не попадающие на hh.ru.

## 4. Job-борды

### hh.ru — главный

**Поиск (UI):**
```
https://hh.ru/search/vacancy?text=data+scientist&experience=noExperience&area=1
```

**Публичный API (без авторизации):**
```
GET https://api.hh.ru/vacancies
  ?text=data+scientist
  &area=113            # 113=РФ, 1=Москва, 2=СПб
  &experience=noExperience   # | between1And3 | between3And6
  &order_by=publication_time
  &date_from=2026-05-27T00:00:00
  &per_page=50
```

Поля: `published_at`, `apply_alternate_url`, `employer.name`, `area.name`, `experience.name`, `salary`. Реализовано в `services/hh.py`.

### Habr Career
```
https://career.habr.com/vacancies?q=ML+engineer&sort=date
https://career.habr.com/api/frontend/vacancies?q=ML&sort=date&page=1   # неофициальный, работает
```

### SuperJob (нужен API-ключ)
```
https://api.superjob.ru/2.33/vacancies/?keywords=data+scientist
```

### LinkedIn (требует авторизации)
```
https://www.linkedin.com/jobs/search/?keywords=ML+engineer+junior&f_E=1
```

## 5. Прямые сайты компаний

Эксклюзивные программы, **не дублируют hh.ru**:

| Компания | URL |
|---|---|
| Яндекс | https://yandex.ru/jobs/vacancies/ |
| Яндекс стажировки | https://yandex.ru/yaintern/ |
| Сбер Student | https://student.sber.ru/internship |
| СберТех | https://sbertech.ru/vacancy |
| Авито Tech | https://avito.tech/vacancies |
| Авито Академия | https://avito-analytics-academy.ru |
| Ozon Tech | https://ozon.tech/vacancies |
| VK | https://vk.company/career/ |
| T-Bank | https://www.tbank.ru/career/vacancies/ |
| МТС | https://rabota.mts.ru/ |
| Газпромбанк | https://jobs.gpb.ru |
| Альфа-Банк | https://hr.alfabank.ru |
| Касперский | https://careers.kaspersky.ru |
| JetBrains | https://www.jetbrains.com/ru-ru/careers/jobs/ |
| Positive Technologies | https://www.ptsecurity.com/ru-ru/about/careers/ |
| X5 Group | https://job.x5.ru |
| Huawei Russia | https://career.huawei.ru |
| Cloud.ru | https://cloud.ru/ru/careers |
| Selectel | https://careers.selectel.ru |
| 2ГИС | https://2gis.ru/career |
| evrone | https://evrone.ru/careers |

## 6. Студенческие агрегаторы

| Ресурс | URL |
|---|---|
| changellenge.com | https://changellenge.com/internships/ |
| Future Today | https://futuretoday.ru |
| Яндекс.Практикум Jobs | https://practicum.yandex.ru/career/ |
| ODS.ai | https://ods.ai/jobs |
| Kaggle | https://www.kaggle.com/jobs |
| ML Tracker | https://mltracker.ru |
| getmatch.ru | https://getmatch.ru |
| works.do | https://works.do |

## 7. Архитектура опроса

| Источник | Метод | Частота | Авторизация |
|---|---|---|---|
| hh.ru API | REST GET | каждые 2 ч | нет |
| Habr Career API | REST GET | каждые 4 ч | нет |
| TG-каналы | Telethon | realtime / webhook | да (сессия) |
| Сайты компаний | HTML парсинг | раз в день | нет |
| changellenge | HTML парсинг | раз в день | нет |
| LinkedIn | scraping | раз в день | да |

**Приоритет №1 — hh.ru API**: официальный, бесплатный, отдаёт `apply_alternate_url`, `published_at`, всё в одном запросе.
