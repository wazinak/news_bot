import requests
from bs4 import BeautifulSoup
import json
from time import sleep


URL = "https://www.rbc.ru/"
HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
}


def getting_main_link_rbk():
    """ Собираем Список ссылок с новостями """
    links_rbk = []
    r = requests.get(url=URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, "lxml")

    title = soup.find('div', class_='l-row js-main-news-big').find('a').get('href')
    main_title = soup.find_all('div', class_='main__feed js-main-reload-item')
    other_title = soup.find_all('div', class_='main__feed js-main-reload-item last2')
    links_rbk.append(title)
    for i in main_title:
        all_title = i.find('a').get('href')
        links_rbk.append(all_title)
    for ii in other_title:
        last2_title = ii.find('a').get('href')
        links_rbk.append(last2_title)

    return links_rbk


# def get_rbc():
#     """ Собираем информацию из каждой ссылки """
#     rbc_dict = {}
#     links = getting_main_link_rbk()
#     for link in links:
#         r = requests.get(url=link, headers=HEADERS)
#         soup = BeautifulSoup(r.text, "lxml")
#         article_id = soup.find('div', class_='js-rbcslider').find('div').get('data-id')
#         article_title = soup.find('div', class_='article__header__title').text.strip() or soup.find('hi', class_='article__header__title-in js-slide-title').text
#         article_main_news = soup.find('div', class_='l-col-main')
#         article_news = article_main_news.find('p').text.strip()
#         article_main_img = soup.find('div', class_='article__main-image')
#         if article_main_img is not None:
#             article_img = article_main_img.find('img').get('src')
#             if article_img:
#                 img_src = requests.get(article_img)
#                 with open(f"img_downloaded/{article_id}.png", "wb") as file:
#                     file.write(img_src.content)
#         else:
#             pass
#
#         rbc_dict[article_id] = {
#             "article_title": article_title,
#             "article_news": article_news,
#             "source": "Источник: РБК",
#             "article_img": article_img
#         }
#         with open("news_dict.json", "w") as file:
#             json.dump(rbc_dict, file, indent=4, ensure_ascii=False)


def checking_updates_rbc():
    """ Собираем обновление на сайте """
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    links = getting_main_link_rbk()
    fresh_news_rbk = {}
    for link in links:
        try:
            if link.startswith("https://quote.ru"):
                pass
            else:
                r = requests.get(url=link, headers=HEADERS)
                print(f"{r.status_code} РБК")
                soup = BeautifulSoup(r.text, "lxml")
                sleep(3)
                article_id = soup.find('div', class_='js-rbcslider').find('div').get('data-id')
                if article_id in news_dict:
                    pass
                else:
                    article_title = soup.find('div', class_='article__header__title').text.strip()
                    article_main_news = soup.find('div', class_='l-col-main')
                    article_news = article_main_news.find('p').text.strip()
                    if article_news is None:
                        article_news = soup.find('div', class_='article__text__overview').find('span').text.strip()
                    article_main_img = soup.find('div', class_='article__main-image')
                    if article_main_img is not None:
                        article_img = article_main_img.find('img').get('src')
                        if article_img:
                            img_src = requests.get(article_img)
                            with open(f"img_downloaded/{article_id}.png", "wb") as file:
                                file.write(img_src.content)
                    else:
                        pass

                    news_dict[article_id] = {
                        "article_title": article_title,
                        "article_news": article_news,
                        "source": "Источник: РБК",
                        "article_img": article_img
                    }
                    fresh_news_rbk[article_id] = {
                        "article_title": article_title,
                        "article_news": article_news,
                        "source": "Источник: РБК",
                        "article_img": article_img
                    }
            with open("news_dict.json", "w") as file:
                json.dump(news_dict, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"{e} Ошибка в коде у РБК")

    return fresh_news_rbk


def main():
    # get_rbc()
    print(checking_updates_rbc())
    # pass


if __name__ == "__main__":
    main()
