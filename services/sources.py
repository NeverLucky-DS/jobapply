"""Реестр источников вакансий. Используется на лендинге и воркером парсинга."""

SOURCES: list[dict] = [
    # TG-агрегаторы
    {"kind": "tg", "name": "Machine Learning Jobs", "url": "https://t.me/machinelearning_jobs", "tag": "ML/DS/MLOps"},
    {"kind": "tg", "name": "AI Jobs", "url": "https://t.me/ai_jobs", "tag": "AI/LLM"},
    {"kind": "tg", "name": "Datascience Jobs", "url": "https://t.me/datascience_jobs", "tag": "DS/Analytics"},
    # TG-каналы компаний
    {"kind": "tg", "name": "Яндекс Jobs", "url": "https://t.me/yandex_jobs", "tag": "Яндекс"},
    {"kind": "tg", "name": "Сбер Jobs", "url": "https://t.me/sber_jobs", "tag": "Сбер"},
    {"kind": "tg", "name": "Авито Jobs", "url": "https://t.me/avito_jobs", "tag": "Авито"},
    {"kind": "tg", "name": "Ozon Jobs", "url": "https://t.me/ozon_jobs", "tag": "Ozon"},
    {"kind": "tg", "name": "T-Bank Jobs", "url": "https://t.me/tbank_jobs", "tag": "T-Bank"},
    {"kind": "tg", "name": "МТС Jobs", "url": "https://t.me/mts_jobs", "tag": "МТС"},
    {"kind": "tg", "name": "Альфа-Банк Jobs", "url": "https://t.me/alfabank_jobs", "tag": "Альфа"},
    # Job-борды
    {"kind": "board", "name": "hh.ru", "url": "https://hh.ru", "tag": "API"},
    {"kind": "board", "name": "Habr Career", "url": "https://career.habr.com/vacancies", "tag": "IT"},
    {"kind": "board", "name": "getmatch.ru", "url": "https://getmatch.ru", "tag": "IT"},
    {"kind": "board", "name": "ML Tracker", "url": "https://mltracker.ru", "tag": "ML/DS"},
    {"kind": "board", "name": "ODS.ai Jobs", "url": "https://ods.ai/jobs", "tag": "DS-комьюнити"},
    {"kind": "board", "name": "changellenge.com", "url": "https://changellenge.com/internships/", "tag": "Стажировки"},
    {"kind": "board", "name": "Future Today", "url": "https://futuretoday.ru", "tag": "Стажировки"},
    {"kind": "board", "name": "Kaggle Jobs", "url": "https://www.kaggle.com/jobs", "tag": "Международные"},
    # Сайты компаний
    {"kind": "company", "name": "Яндекс", "url": "https://yandex.ru/jobs/vacancies/", "tag": "стажировки"},
    {"kind": "company", "name": "Yandex Intern", "url": "https://yandex.ru/yaintern/", "tag": "школы"},
    {"kind": "company", "name": "Сбер Student", "url": "https://student.sber.ru/internship", "tag": "стажировки"},
    {"kind": "company", "name": "Avito Tech", "url": "https://avito.tech/vacancies", "tag": "REST"},
    {"kind": "company", "name": "Ozon Tech", "url": "https://ozon.tech/vacancies", "tag": ""},
    {"kind": "company", "name": "VK Career", "url": "https://vk.company/career/", "tag": ""},
    {"kind": "company", "name": "T-Bank", "url": "https://www.tbank.ru/career/vacancies/", "tag": "T-School"},
    {"kind": "company", "name": "MTS Rabota", "url": "https://rabota.mts.ru/", "tag": "Digital Academy"},
    {"kind": "company", "name": "Альфа-Банк HR", "url": "https://hr.alfabank.ru", "tag": ""},
    {"kind": "company", "name": "Газпромбанк", "url": "https://jobs.gpb.ru", "tag": ""},
    {"kind": "company", "name": "Касперский", "url": "https://careers.kaspersky.ru", "tag": "Intern"},
    {"kind": "company", "name": "JetBrains", "url": "https://www.jetbrains.com/ru-ru/careers/jobs/", "tag": "Intern"},
    {"kind": "company", "name": "X5 Group", "url": "https://job.x5.ru", "tag": ""},
    {"kind": "company", "name": "Selectel", "url": "https://careers.selectel.ru", "tag": ""},
    {"kind": "company", "name": "Cloud.ru", "url": "https://cloud.ru/ru/careers", "tag": ""},
    {"kind": "company", "name": "2ГИС", "url": "https://2gis.ru/career", "tag": ""},
]
