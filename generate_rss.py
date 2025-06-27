import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

URL = "https://www.ccsuniversity.ac.in/search-news?title=&category=&month=&year=&page=1"
BASE_URL = "https://www.ccsuniversity.ac.in/"

def fetch_notices():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the table containing the links
    table = soup.find("table")
    items = []

    if table:
        for a in table.find_all("a", href=True):
            title = a.get_text(strip=True)
            link = a["href"]

            # Skip empty titles or links
            if not title or not link:
                continue

            # Handle relative URLs just in case
            if not link.startswith("http"):
                link = BASE_URL + link.lstrip("/")

            items.append({
                "title": title,
                "link": link,
                "pubDate": datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000"),
                "guid": link,
            })
    return items

def generate_rss():
    fg = FeedGenerator()
    fg.title("CCS University - Latest News")
    fg.link(href=URL, rel='alternate')
    fg.description("News updates from CCS University Meerut")
    fg.language("en")
    fg.lastBuildDate(datetime.now(timezone.utc))
    fg.link(href="https://nitinnagar23.github.io/ccs-rss-feed/ccs-feed.xml", rel="self", type="application/rss+xml")

    for item in fetch_notices():
        fe = fg.add_entry()
        fe.title(item["title"])
        fe.link(href=item["link"])
        fe.guid(item["guid"])
        fe.pubDate(item["pubDate"])

    fg.rss_file("ccs-feed.xml")

if __name__ == "__main__":
    generate_rss()
