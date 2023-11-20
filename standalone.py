import requests
from bs4 import BeautifulSoup
import pandas as pd
##import re
import csv
import scrape_link

url = pd.read_csv("link_database.csv")["0"]

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
    content = soup.find("div", class_ = "post-content clearfix")
    pubmeta = soup.find ("meta", {"property": "article:published_time"})
    if pubmeta and "content" in pubmeta.attrs :
        pubDate = soup.find ("meta", {"property": "article:published_time"})["content"]
    else:
        pubDate = "null"
        title = soup.find("title")
        content = soup.find("div", class_ = "post-content clearfix")
        content.text.replace('</b><span>', '').strip()
    if content:
        for a in content.find_all('a'):
            a.replace_with(' ')
        for b in content.find_all('/b'):
            a.replace_with(' ')
        for br in content.find_all('br'):
            br.replace_with('\n')
    content.text.replace('Baca Juga', '').strip()
    content_title.append(title.text)
    content_data.append(content.text)
    content_pubdate.append(pubDate)
    content_link.append(links)
    df = pd.DataFrame({"Title": content_title, "Tanggal Rilis": content_pubdate, "Text Berita": content_data, "Link": content_link })
    df.to_csv("content_rungkad.csv")