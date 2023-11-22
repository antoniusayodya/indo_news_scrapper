import requests
from bs4 import BeautifulSoup
import pandas as pd
##import re
import csv
import scrape_link

url = pd.read_csv("dibuangsayang.csv")["0"]

news_url = url
content_title = []
content_data = []
content_pubdate = []
content_link =[]
excl = ['/foto', '/infografik', '/video']
linkss = [link for link in news_url if not any(pattern in link for pattern in excl)]
for links in linkss:
    r = requests.get(links)
    soup = BeautifulSoup(r.content, "html.parser")
    title = soup.find("title")
    content = soup.find("div", class_ = "post-content")
    text_news = ""
    pubmeta = soup.find ("meta", {"property": "article:published_time"})
    if pubmeta and "content" in pubmeta.attrs :
        pubDate = soup.find ("meta", {"property": "article:published_time"})["content"]
    else:
        pubDate = "null"
        content.text.replace('</b><span>', '').strip()
    if content:
        for a in content.find_all('a'):
            a.replace_with('')
        for b in content.find_all('/b'):
            b.replace_with('')
        for br in content.find_all('br'):
            br.replace_with('\n')
    text_news = content.get_text(strip=True)
    text_news.replace('Baca Juga:', '').strip()
    content_title.append(title.text)
    content_data.append(text_news)
    content_pubdate.append(pubDate)
    content_link.append(links)
    df = pd.DataFrame({"Title": content_title, "Tanggal Rilis": content_pubdate, "Text Berita": content_data, "Link": content_link })
    df.to_csv("content_list.csv")