"""Playwright-автоотклик на hh.ru.

Читает HH_LOGIN + HH_PASSWORD из env. При первом запуске логинится и сохраняет
куки в hh_cookies.json — последующие запуски переиспользуют сессию.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright

from db import async_session
from models import Application

log = logging.getLogger(__name__)
COOKIES_PATH = Path(__file__).parent.parent / "hh_cookies.json"


async def _login(page, login: str, password: str):
    """Проходит форму входа hh.ru."""
    await page.goto("https://hh.ru/account/login", wait_until="domcontentloaded", timeout=30_000)
    await page.wait_for_timeout(1000)

    # email input
    await page.fill('input[name="login"]', login)
    await page.click('button[data-qa="account-login-submit"]')
    await page.wait_for_timeout(1500)

    # password
    pwd_input = page.locator('input[name="password"]')
    if await pwd_input.count() > 0:
        await pwd_input.fill(password)
        await page.click('button[data-qa="account-login-submit"]')
        await page.wait_for_timeout(2000)


async def _load_session(ctx):
    """Грузит куки из файла в контекст."""
    if COOKIES_PATH.exists():
        cookies = json.loads(COOKIES_PATH.read_text())
        await ctx.add_cookies(cookies)
        return True
    return False


async def _save_session(ctx):
    """Сохраняет текущие куки контекста."""
    cookies = await ctx.cookies()
    COOKIES_PATH.write_text(json.dumps(cookies, ensure_ascii=False))


async def _is_logged_in(page) -> bool:
    """Проверяет, залогинен ли пользователь."""
    await page.goto("https://hh.ru", wait_until="domcontentloaded", timeout=20_000)
    return await page.locator('[data-qa="mainmenu_myResume"]').count() > 0


async def apply_hh(url: str, cover_letter: str, title: str = "", company: str = ""):
    """Открывает вакансию и жмёт Откликнуться. Результат пишет в таблицу Application."""
    login = os.environ.get("HH_LOGIN", "")
    password = os.environ.get("HH_PASSWORD", "")

    status = "sent"
    error_msg = None

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            ctx = await browser.new_context(
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                locale="ru-RU",
            )

            # Грузим сохранённую сессию или логинимся
            page = await ctx.new_page()
            await _load_session(ctx)

            if not await _is_logged_in(page):
                if not login or not password:
                    error_msg = "Нет HH_LOGIN / HH_PASSWORD в secrets и сохранённой сессии нет"
                    log.error(error_msg)
                    status = "error"
                else:
                    await _login(page, login, password)
                    if await _is_logged_in(page):
                        await _save_session(ctx)
                    else:
                        error_msg = "Логин не удался (возможно CAPTCHA)"
                        status = "error"

            if status != "error":
                await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
                await page.wait_for_timeout(1500)

                # Жмём кнопку отклика
                btn = page.locator('[data-qa="vacancy-response-link-top"]')
                if await btn.count() == 0:
                    btn = page.locator('[data-qa="vacancy-response-link-bottom"]')
                if await btn.count() == 0:
                    btn = page.locator('text=Откликнуться')

                await btn.first.click()
                await page.wait_for_timeout(2000)

                # Вводим сопроводительное письмо
                letter_area = page.locator('[data-qa="vacancy-response-popup-letter-input"]')
                if await letter_area.count() == 0:
                    letter_area = page.locator('textarea[name="letter"]')
                if await letter_area.count() > 0 and cover_letter:
                    await letter_area.fill(cover_letter)
                    await page.wait_for_timeout(500)

                # Submit
                submit = page.locator('[data-qa="vacancy-response-submit-popup"]')
                if await submit.count() == 0:
                    submit = page.locator('button[type="submit"]').last
                await submit.click()
                await page.wait_for_timeout(2000)

                log.info(f"Applied: {title} at {company} | {url}")

            await browser.close()

    except Exception as e:
        log.exception(f"apply_hh error: {e}")
        status = "error"
        error_msg = str(e)

    # Сохраняем в БД
    async with async_session() as s:
        app = Application(
            vacancy_url=url,
            vacancy_title=title or url,
            company=company,
            source="hh",
            cover_letter=cover_letter,
            status=status,
            applied_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        s.add(app)
        await s.commit()

    if error_msg:
        log.error(f"Apply failed: {error_msg}")
    return status
