import requests
import threading
from bs4 import BeautifulSoup


def get_fresh_manga():
    manga_panda_home = requests.get('https://www.mangapanda.com/')
    manga_panda_home_html = BeautifulSoup(manga_panda_home.text, 'lxml')

    latest_hot_manga = manga_panda_home_html.find(
        id="latesthot").find_all("div", class_="latesthotimages")

    manga_list = []
    for div in latest_hot_manga:
        manga_data = {
            "home": div.find("h3").find("a").get("href"),
            "chapter": div.find("h3").find("a").text
        }
        # print(div.find("h3").find("a").get("href"))
        manga_list.append(manga_data)

        # title.append(div.find('h3').find('a').text)

    return manga_list


print(get_fresh_manga())
