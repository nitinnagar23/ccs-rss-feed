import requests
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

API_URL = "https://www.ccsuniversity.ac.in/web/GetNewsList"
POST_DATA = {
    "title": "",
    "category": "",
    "month": "",
    "year": "",
    "page": 1
}
BASE_CDN = "https://cdn.ccsuniversity.ac.in"

def fetch_notices():
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(API_URL, json=POST_DATA, headers=headers)
    data = response.json()

    items = []

    for news_item in data.get("data", []):
        title = news_item.get("title", "").strip()
        url = news_item.get("url", "").strip()
        full_url = url if url.startswith("http") else f"{BASE_CDN}/{url.lstrip('/')}"
        date_str = news_item.get("uploaded_date", "")
        pub_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

        items.append({
            "title": title,
            "link": full_url,
            "guid": full_url,
            "pubDate": pub_date,
        })

    return items

def generate_rss():
    fg = FeedGenerator()
    fg.title("CCS University - Latest News")
    fg.link(href="https://www.ccsuniversity.ac.in/search-news?title=&category=&month=&year=&page=1", rel='alternate')
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
