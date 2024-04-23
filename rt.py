import requests
from bs4 import BeautifulSoup
import json
from time import sleep


URL = 'https://russian.rt.com/news'
HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
}


def getting_main_link_rt():
    """ Получаем список статей новостей """
    links_rt = []
    r = requests.get(url=URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, "lxml")
    titles = soup.find_all('li', class_='listing__column listing__column_all-news listing__column_js')
    for title in titles:
        link = f"https://russian.rt.com{title.find_all('a')[1].get('href')}"
        links_rt.append(link)

    return links_rt


def get_rt():
    """ Собираем новости из полученных ссылок """
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    links = getting_main_link_rt()
    fresh_news_rt = {}
    for link in links:
        try:
            r = requests.get(url=link, headers=HEADERS)
            print(f"{r.status_code} RT")
            sleep(3)
            soup = BeautifulSoup(r.text, "lxml")
            article_id = link.split("/")[-1]
            article_id = article_id.split("-")[0]
            if article_id in news_dict:
                pass
            else:
                article_title = soup.find('h1', class_='article__heading article__heading_article-page').text
                article_main_news = soup.find('div', class_='article__text article__text_article-page js-mediator-article').find('p').text
                article_main_img = soup.find('div', class_='article__cover article__cover_article-page')
                if article_main_img is not None:
                    article_main_img = article_main_img.find('img', class_='article__cover-image').get('src')
                    img_response = requests.get(article_main_img)
                    with open(f"img_downloaded/{article_id}.png", "wb") as file:
                        file.write(img_response.content)
                else:
                    pass

                news_dict[article_id] = {
                    "article_title": article_title,
                    "article_news": article_main_news,
                    "source": "Источник: Russia Today",
                    "article_img": article_main_img
                }
                fresh_news_rt[article_id] = {
                    "article_title": article_title,
                    "article_news": article_main_news,
                    "source": "Источник: Russia Today",
                    "article_img": article_main_img
                }

            with open("news_dict.json", "w") as file:
                json.dump(news_dict, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"{e} Ошибка в коде у РТ")

    return fresh_news_rt
