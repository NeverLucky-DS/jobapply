"""Генерация сопроводительного письма через Mistral."""

import os
from mistralai import Mistral

_client = None

def get_client() -> Mistral:
    global _client
    if _client is None:
        key = os.environ.get("MISTRAL") or os.environ.get("MISTRAL_API_KEY")
        if not key:
            raise RuntimeError("MISTRAL env var not set")
        _client = Mistral(api_key=key)
    return _client


async def generate_cover_letter(vacancy: dict, profile: dict) -> str:
    """Генерирует сопроводительное письмо под конкретную вакансию."""
    stack = ", ".join(profile.get("stack", []))
    prompt = f"""Ты помогаешь написать короткое сопроводительное письмо для отклика на вакансию.

Профиль кандидата:
- Имя: {profile.get('name')}
- Цель: {profile.get('target_position')}
- Стек: {stack}
- О себе: {profile.get('about')}
- Опыт: {profile.get('experience') or 'нет коммерческого опыта, учебные проекты'}

Вакансия:
- Название: {vacancy.get('title') or vacancy.get('name')}
- Компания: {vacancy.get('company') or vacancy.get('employer')}
- Описание/требования: {vacancy.get('snippet') or ''}

Напиши сопроводительное письмо на русском языке. Требования:
- 3-5 предложений, максимум 120 слов
- Живой тон, без канцелярита
- Конкретно упомяни компанию и позицию
- Покажи релевантные навыки из стека
- Заканчивай призывом к действию (готов к собеседованию)
- Только текст письма, без темы и подписи"""

    client = get_client()
    resp = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()
