"""Парсер rabota.sber.ru через Playwright. URL-фильтр уровня не работает —
постфильтруем по словам в заголовке.
"""

import logging
import re

from playwright.async_api import async_playwright

log = logging.getLogger(__name__)

BASE = "https://rabota.sber.ru"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0"

INTERN_RE = re.compile(r"\b(стажёр|стажер|интерн|intern|без опыта|начинающ)\w*", re.I)
JUNIOR_RE = re.compile(r"\b(junior|младший|ассистент)\b", re.I)
SENIOR_RE = re.compile(
    r"\b(senior|lead|ведущ|главн|старш|principal|архитектор|руководит|head|директор|chief|tech\s*lead)\w*",
    re.I,
)


def detect_level(title: str) -> str | None:
    """intern > junior, исключаем senior/lead/etc."""
    if SENIOR_RE.search(title):
        return None
    if INTERN_RE.search(title):
        return "intern"
    if JUNIOR_RE.search(title):
        return "junior"
    return None


async def fetch_sber(max_pages: int = 2) -> list[dict]:
    """Парсит несколько страниц Сбера, оставляет только intern/junior. На ошибке — []."""
    out: list[dict] = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            ctx = await browser.new_context(user_agent=UA, locale="ru-RU")
            page = await ctx.new_page()
            for pg in range(1, max_pages + 1):
                url = f"{BASE}/search/?page={pg}"
                await page.goto(url, wait_until="domcontentloaded", timeout=45_000)
                try:
                    await page.wait_for_selector('a[href^="/search/"][href*="-"]', timeout=20_000)
                except Exception:
                    break
                await page.wait_for_timeout(1500)
                cards = await page.evaluate("""
                    () => {
                      const out = [];
                      document.querySelectorAll('[class*="styled__Card"]').forEach(card => {
                        const a = card.querySelector('a[href^="/search/"]');
                        if (!a) return;
                        const title = (a.innerText || '').trim();
                        const secs = card.querySelectorAll('[class*="LocationSection"] [class*="Text-sc"]');
                        out.push({
                          href: a.getAttribute('href'),
                          title,
                          loc: secs[0] ? secs[0].innerText.trim() : null,
                          company: secs[1] ? secs[1].innerText.trim() : null,
                        });
                      });
                      return out;
                    }
                """)
                if not cards:
                    break
                for c in cards:
                    level = detect_level(c.get("title") or "")
                    if not level:
                        continue
                    m = re.search(r"-(\d+)/?$", c.get("href") or "")
                    if not m:
                        continue
                    out.append({
                        "source": "sber",
                        "source_id": m.group(1),
                        "title": c["title"],
                        "company": c.get("company") or "ПАО Сбербанк",
                        "location": c.get("loc"),
                        "level": level,
                        "url": BASE + c["href"],
                    })
            await browser.close()
    except Exception as e:
        log.warning("sber fetch failed: %s", e)
    # дедуп по source_id (на случай пересечения страниц)
    seen, uniq = set(), []
    for it in out:
        if it["source_id"] in seen:
            continue
        seen.add(it["source_id"]); uniq.append(it)
    return uniq
