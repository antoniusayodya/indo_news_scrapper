import requests
from bs4 import BeautifulSoup
import pandas as pd
##import re
import csv
import scrape_link

##Function for scrapping content from link
def content(url):
    link = url
    for links in link:
        r = requests.get(links)
        soup = BeautifulSoup(r.content, "html.parser")
        title = soup.find("title")
        content = soup.find("div", class_ = "post-content clearfix")
        ##pubDate = soup.find ("meta", {'property': 'article:published_time'} )['content']
        title = soup.find("title")
        content = soup.find("div", class_ = "post-content clearfix")
        pubDate = soup.find ("meta", {'property': 'article:published_time'} )['content']
        content.text.replace('</b><span>', '').strip()
        if content:
            ##re.sub(r'\b{}\b'.format(re.escape('Baca Juga')), '', content.text, flags=re.IGNORECASE)
            for a in content.find_all('a'):
                a.replace_with(' ')
            for b in content.find_all('/b'):
                a.replace_with(' ')
            for br in content.find_all('br'):
                br.replace_with('\n')
        content.text.replace('Baca Juga', '').strip()
        df = pd.DataFrame({"title": [title.text], "content": [content.text], "publish_date": [pubDate], "link": [url]})
        df.to_csv("content.csv")
        return content

##urlnya dipakai untuk directory news sitenya
url = ("https://antaranews.com/terkini/", "https://antaranews.com/politik/", "https://antaranews.com/hukum/", "https://antaranews.com/ekonomi/", "https://antaranews.com/metro/", "https://antaranews.com/sepakbola/", "https://antaranews.com/olahraga/", "https://antaranews.com/humaniora/", "https://antaranews.com/lifestyle/", "https://antaranews.com/hiburan/")

##function dari awal sampai akhir
def scrap_antara():
    scrap_link = scrape_link.list_url(url)
    news_link = scrape_link.news_link_scrapper(scrap_link)
    content_database = content(news_link)
    return content_database

if __name__ == "__main__":
    scrap_antara()