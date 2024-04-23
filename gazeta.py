import requests
from bs4 import BeautifulSoup
import json
from time import sleep


URL = 'https://www.gazeta.ru/news/?updated'
HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
}


def getting_main_link_gazeta():
    """ Получаем список статей новостей """
    links_gazeta = []
    r = requests.get(url=URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, "lxml")
    titles = soup.find('div', class_='w_col_840').find_all('a')
    for title in titles:
        links = f"https://www.gazeta.ru/{title.get('href')}"
        links_gazeta.append(links)

    return links_gazeta


def get_gazeta():
    """ собираем новости из списка ссылок """
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    links = getting_main_link_gazeta()
    fresh_news_gazeta = {}
    for link in links:
        try:
            if link.endswith("page=2"):
                pass
            else:
                r = requests.get(url=link, headers=HEADERS)
                print(f"{r.status_code} Газета.ru")
                soup = BeautifulSoup(r.text, "lxml")
                sleep(3)
                article_id = link.split("/")[-1]
                article_id = article_id.split(".")[0]
                if article_id in news_dict:
                    pass
                else:
                    article_title = soup.find('div',class_='b_article-header').find('h2',class_='headline').text
                    if article_title is None:
                        pass
                    article_main_news = soup.find('div', class_='b_article-text')
                    article_news = article_main_news.find('p').text
                    if article_news is None:
                        pass
                    article_main_img = soup.find('div', class_='mainarea')
                    if article_main_img is not None:
                        article_img = article_main_img.find('img').get('data-hq')
                        if article_img:
                            img_src = requests.get(article_img)
                            with open(f"img_downloaded/{article_id}.png", "wb") as file:
                                file.write(img_src.content)
                    else:
                        pass

                    news_dict[article_id] = {
                        "article_title": article_title,
                        "article_news": article_news,
                        "source": "Источник: Газета ру",
                        "article_img": article_img
                    }
                    fresh_news_gazeta[article_id] = {
                        "article_title": article_title,
                        "article_news": article_news,
                        "source": "Источник: Газета ру",
                        "article_img": article_img
                    }
            with open("news_dict.json", "w") as file:
                json.dump(news_dict, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"{e} Ошибка в коде у Газету ру")

    return fresh_news_gazeta
