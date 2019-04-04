import requests
from bs4 import BeautifulSoup
# from mangadownloader import db
# from mangadownloader.models import Manga, Artist, Author, Genre


class MyAnimeList(object):

    my_anime_list_all_manga_url = 'https://myanimelist.net/topmanga.php'

    def __init__(self):
        self._all_manga_request = requests.get(
            self.my_anime_list_all_manga_url)
        self._all_manga_html = BeautifulSoup(
            self._all_manga_request.text, "lxml")
        self._raw_manga_list = self._all_manga_html.find(
            class_="top-ranking-table").find_all("tr", class_="ranking-list")

    def get_manga_title_list(self):
        for manga in self._raw_manga_list:
            yield manga.find_all("td")[1].find(class_="detail").find(class_="hoverinfo_trigger").text

    def get_manga_link_list(self):
        for manga in self._raw_manga_list:
            yield manga.find_all("td")[1].find(class_="detail").find(class_="hoverinfo_trigger").get("href")


manga = MyAnimeList()

for manga in manga.get_manga_link_list():
    print(manga)
