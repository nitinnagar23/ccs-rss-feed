import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime

BASE = 'https://www.ccsuniversity.ac.in'
NEWS_URL = BASE + '/search-news?title=&category=&month=&year=&page=1'

res = requests.get(NEWS_URL)
soup = BeautifulSoup(res.text, 'html.parser')

fg = FeedGenerator()
fg.title('CCS University - Latest News')
fg.link(href=NEWS_URL)
fg.description('News updates from CCS University Meerut')
fg.language('en')

for item in soup.select('.news-detail'):
    title_tag = item.select_one('h5')
    link_tag = item.select_one('a')
    date_tag = item.select_one('.date')

    if not (title_tag and link_tag and date_tag):
        continue

    title = title_tag.get_text(strip=True)
    detail_href = BASE + link_tag['href']
    date_text = date_tag.get_text(strip=True)

    # Try to get redirected PDF URL
    try:
        detail_res = requests.get(detail_href, allow_redirects=True)
        final_url = detail_res.url  # Will be cdn.ccsuniversity.ac.in if redirect happens
    except:
        final_url = detail_href  # Fallback to detail page if request fails

    try:
        pub_date = datetime.strptime(date_text, '%d-%m-%Y')
    except:
        pub_date = datetime.utcnow()

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=final_url)
    fe.pubDate(pub_date)

fg.rss_file('ccs-feed.xml', encoding='utf-8')
