import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv


##url = ("https://antaranews.com/terkini/", "https://antaranews.com/politik/")

##For making list of pages you want to scrap the headline from
def list_url(url):
    url_list = []
    number = list(range(2, 100))
    num_str = [str(i) for i in number]
    for link in url:
        for a in num_str:
                urlpage = [link.rsplit('/', 1)[0] + '/' + a]
                url_list.append(urlpage)
                ##url_flat_list = [url for sublist in url_list for url in sublist]
        df_url = pd.DataFrame(url_list)
    df_url.to_csv("url_NTB.csv")
    return url_list

##For making list of the news you want to take the content from
def news_link_scrapper(url_list):
     news_link = []
     judul = []
     navigasi = []
     for page in url_list:
          str_page = str(page).strip("['']")
          r = requests.get(str_page)
          soup = BeautifulSoup(r.content, 'html.parser')
          simple_thumbs = soup.find_all('div', class_='simple-thumb')
          for simple_thumb in simple_thumbs:
               headline = simple_thumb.find_all('a', href=True)
          for headline_tag in headline:
               headline_news = headline_tag['href']
               judul_berita = headline_tag['title']
          news_link.append(headline_news)
          judul.append(judul_berita)
          judul_cln = (list(set(judul)))
          news_link_cln = (list(set(news_link)))
          df_link = pd.DataFrame({"Navigasi": str_page, "Link":news_link_cln})
          df_link.to_csv('link_list.csv')
     return news_link_cln

