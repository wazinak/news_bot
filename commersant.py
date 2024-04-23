import requests
from bs4 import BeautifulSoup
import json
from time import sleep


URL = 'https://www.kommersant.ru/?from=logo'
HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
}


def getting_links_commersant():
    """ Получаем список ссылок на новости """
    links_commersant = []
    r = requests.get(url=URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, "lxml")
    titles = soup.find_all('article', class_='top_news__item')
    for title in titles:
        link = f"https://www.kommersant.ru/{title.find('a').get('href')}"
        links_commersant.append(link)

    return links_commersant


def commersant_news():
    """ Собираем новости в словарь """
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    links = getting_links_commersant()
    fresh_news_commersant = {}
    for link in links:
        try:
            r = requests.get(url=link, headers=HEADERS)
            print(f"{r.status_code} Коммерсант")
            soup = BeautifulSoup(r.text, "lxml")
            sleep(3)
            article_id = link.split("/")[-1]
            article_id = article_id.split("?")[0]
            if article_id in news_dict:
                pass
            else:
                article_title = soup.find('h1', class_='doc_header__name js-search-mark').text.strip()
                article_main_news = soup.find('p').text
                news_dict[article_id] = {
                    "article_title": article_title,
                    "article_news": article_main_news,
                    "source": "Источник: Коммерсантъ",
                    "article_img": None
                }
                fresh_news_commersant[article_id] = {
                    "article_title": article_title,
                    "article_news": article_main_news,
                    "source": "Источник: Коммерсантъ",
                    "article_img": None
                }
            with open("news_dict.json", "w") as file:
                json.dump(news_dict, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"{e} Ошибка в коде у Коммерсанта")

    return fresh_news_commersant
