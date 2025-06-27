import asyncio
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator
from playwright.async_api import async_playwright, TimeoutError

URL = "https://www.ccsuniversity.ac.in/search-news?title=&category=&month=&year=&page=1"

async def fetch_notices():
    items = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL, wait_until="networkidle")

        try:
            await page.wait_for_selector("div.col-lg-8", timeout=30000)
        except TimeoutError:
            print("⚠
