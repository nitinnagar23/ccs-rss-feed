import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
import re

# Set the directory to scan
BASE_URL = "https://cdn.ccsuniversity.ac.in/public/pdf/2025/06/"

def fetch_pdfs():
    response = requests.get(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.content, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        href = a['href']
        if href.lower().endswith(".pdf"):
            full_url = BASE_URL + href
            title = href.replace(".pdf", "").replace("%20", " ").replace("_", " ").strip()
            links.append({
                "title": title,
                "link": full_url,
                "guid": full_url,
                "pubDate": datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
            })

    return links

def generate_rss():
    fg = FeedGenerator()
    fg.title("CCSU PDF Notices - June 2025")
    fg.link(href=BASE_URL, rel='alternate')
    fg.description("Latest PDF notices from CCSU CDN")
    fg.language("en")
    fg.lastBuildDate(datetime.now(timezone.utc))
    fg.link(href="https://nitinnagar23.github.io/ccs-rss-feed/ccs-feed.xml", rel="self", type="application/rss+xml")

    for item in fetch_pdfs():
        fe = fg.add_entry()
        fe.title(item["title"])
        fe.link(href=item["link"])
        fe.guid(item["guid"])
        fe.pubDate(item["pubDate"])

    fg.rss_file("ccs-feed.xml")

if __name__ == "__main__":
    generate_rss()
