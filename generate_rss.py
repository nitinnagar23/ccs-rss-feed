import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime

URL = 'https://www.ccsuniversity.ac.in/search-news?title=&category=&month=&year=&page=1'
BASE = 'https://www.ccsuniversity.ac.in'

res = requests.get(URL)
soup = BeautifulSoup(res.text, 'html.parser')

fg = FeedGenerator()
fg.title('CCS University - Latest News')
fg.link(href=URL)
fg.description('News updates from CCS University Meerut')
fg.language('en')

for item in soup.select('.news-detail'):
    title_tag = item.select_one('h5')
    link_tag = item.select_one('a')
    date_tag = item.select_one('.date')  # Adjust this selector based on actual structure

    if not (title_tag and link_tag and date_tag):
        continue

    title = title_tag.get_text(strip=True)
    link = BASE + link_tag['href']
    date_text = date_tag.get_text(strip=True)

    try:
        pub_date = datetime.strptime(date_text, '%d-%m-%Y')
    except:
        pub_date = datetime.utcnow()

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=link)
    fe.pubDate(pub_date)

fg.rss_file('ccs-feed.xml')
