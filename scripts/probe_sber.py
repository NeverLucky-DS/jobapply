"""Разведка структуры rabota.sber.ru — открыть, дождаться, сдампить разметку карточки."""

import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0",
            locale="ru-RU",
        )
        page = await ctx.new_page()
        url = "https://rabota.sber.ru/search/?type=internship"
        await page.goto(url, wait_until="domcontentloaded", timeout=45_000)
        try:
            await page.wait_for_selector('a[href*="/vacancy/"]', timeout=20_000)
        except Exception as e:
            print("selector wait failed:", e)
        await page.wait_for_timeout(2000)
        # сохраним рендер для разбора
        html = await page.content()
        with open("/tmp/sber_rendered.html", "w") as f:
            f.write(html)
        print(f"saved {len(html)} bytes")
        # ищем возможные карточки
        for sel in ['[data-cy*="vacancy"]', 'article', '[class*="VacancyCard"]', '[class*="Card"]', 'a[href*="/vacancies/"]']:
            cnt = await page.locator(sel).count()
            print(f"  {sel}: {cnt}")
        await browser.close()


asyncio.run(main())
