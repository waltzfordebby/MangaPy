import requests
import threading
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class RequestThread(threading.Thread):
    def __init__(self, url):
        super(RequestThread, self).__init__()
        self._url = url
        self._html = ''

    def run(self):
        self._html = requests.get(self._url).text


class MangaPanda(object):
    manga_panda_home_url = 'https://www.mangapanda.com'

    def __init__(self):
        self._manga_panda_home_request = requests.get(
            'https://www.mangapanda.com')
        self._manga_panda_home_html = BeautifulSoup(
            self._manga_panda_home_request.text, 'lxml')
        self._latest_hot_manga_html = self._manga_panda_home_html.find(
            id="latesthot").find_all("div", class_="latesthotimages")
        self._popular_manga_html = self._manga_panda_home_html.find(
            "div", id="popularlist").find_all("li")

    def get_hot_manga_chapter(self):
        for manga in self._latest_hot_manga_html:
            yield manga.find("h3").find("a").text

    def get_hot_manga_url(self):
        for manga in self._latest_hot_manga_html:
            parsed_manga_url = urlparse(manga.find("h3").find("a").get("href"))
            yield f'{parsed_manga_url.scheme}://{parsed_manga_url.netloc}/{parsed_manga_url.path.split("/")[1]}'

    def get_each_hot_manga_html(self):
        for url in self.get_hot_manga_url():
            yield requests.get(url).text

    def get_each_manga_cover_url(self):
        for manga_html in self.get_each_hot_manga_html():
            manga_home_html = BeautifulSoup(manga_html, 'lxml')
            yield manga_home_html.find(id="mangaimg").find("img").get("src")

    def get_hot_manga_summary(self):
        for chapter, url in zip(self.get_hot_manga_chapter(), self.get_each_manga_cover_url()):
            yield {'chapter': chapter, 'cover_url': url}

    def get_popular_manga_url(self):
        for manga in self._popular_manga_html:
            yield f'{self.manga_panda_home_url}{manga.find("a").get("href")}'

    def get_each_popular_manga_html(self):
        for url in self.get_popular_manga_url():
            yield requests.get(url).text

    def get_popular_manga_cover_url(self):
        for manga_html in self.get_each_popular_manga_html():
            manga_home_html = BeautifulSoup(manga_html, 'lxml')
            print(manga_home_html.find(id="mangaimg").find("img").get("src"))
            # yield manga_home_html.find(id="mangaimg").find("img").get("src")


def hotMangaData():
    manga = MangaPanda()
    return manga.get_hot_manga_summary()


def test():
    manga = MangaPanda()
    manga.get_popular_manga_cover_url()


# test()
