import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

URL = "https://www.ccsuniversity.ac.in/search-news?title=&category=&month=&year=&page=1"

def fetch_pdf_links():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)

    # ✅ Save HTML for debugging
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    soup = BeautifulSoup(response.content, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        href = a['href']
        if href.endswith(".pdf") and "cdn.ccsuniversity.ac.in" in href:
            title = a.get_text(strip=True)
            if not title:
                title = href.split("/")[-1]
            links.append({
                "title": title,
                "link": href,
                "guid": href,
                "pubDate": datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
            })

    # ✅ Print debug info
    print(f"🔍 Found {len(links)} PDF links.")
    return links

def generate_rss():
    fg = FeedGenerator()
    fg.title("CC
