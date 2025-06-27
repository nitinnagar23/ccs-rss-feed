import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

URL = "https://www.ccsuniversity.ac.in/search-news?title=&category=&month=&year=&page=1"

def fetch_pdf_links():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
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

    return links

def generate_rss():
    fg = FeedGenerator()
    fg.title("CCSU News PDFs")
    fg.link(href=URL, rel='alternate')
    fg.description("Latest PDF-based notices from CCSU")
    fg.language("en")
    fg.lastBuildDate(datetime.now(timezone.utc))
    fg.link(href="https://nitinnagar23.github.io/ccs-rss-feed/ccs-feed.xml", rel="self", type="application/rss+xml")

    for item in fetch_pdf_links():
        fe = fg.add_entry()
        fe.title(item["title"])
        fe.link(href=item["link"])
        fe.guid(item["guid"])
        fe.pubDate(item["pubDate"])

    fg.rss_file("ccs-feed.xml")

if __name__ == "__main__":
    generate_rss()
