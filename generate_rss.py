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
            print("⚠️ Could not find main content container.")
            await browser.close()
            return []

        links = await page.query_selector_all("div.col-lg-8 .card-body a")
        print(f"🔍 Found {len(links)} links")

        for link in links:
            title = (await link.inner_text()).strip()
            href = (await link.get_attribute("href") or "").strip()
            if not href or not title:
                continue
            if not href.startswith("http"):
                href = "https://www.ccsuniversity.ac.in/" + href.lstrip("/")
            items.append({
                "title": title,
                "link": href,
                "guid": href,
                "pubDate": datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
            })

        await browser.close()
    return items

async def generate_rss():
    fg = FeedGenerator()
    fg.title("CCSU News - Notices and PDFs")
    fg.link(href=URL, rel='alternate')
    fg.description("Latest official notices from CCSU")
    fg.language("en")
    fg.lastBuildDate(datetime.now(timezone.utc))
    fg.link(href="https://nitinnagar23.github.io/ccs-rss-feed/ccs-feed.xml", rel="self", type="application/rss+xml")

    items = await fetch_notices()
    for item in items:
        fe = fg.add_entry()
        fe.title(item["title"])
        fe.link(href=item["link"])
        fe.guid(item["guid"])
        fe.pubDate(item["pubDate"])

    fg.rss_file("ccs-feed.xml")

if __name__ == "__main__":
    asyncio.run(generate_rss())
