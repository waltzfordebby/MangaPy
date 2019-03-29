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

    def get_manga_html(self, url_list):
        for url in url_list:
            yield requests.get(url).text

    def get_manga_cover_url(self, manga_html_list):
        for manga_html in manga_html_list:
            manga_home_html = BeautifulSoup(manga_html, 'lxml')
            yield manga_home_html.find(id="mangaimg").find("img").get("src")

    def get_hot_manga_chapter(self):
        for manga in self._latest_hot_manga_html:
            yield manga.find("h3").find("a").text

    def get_hot_manga_url(self):
        for manga in self._latest_hot_manga_html:
            parsed_manga_url = urlparse(manga.find("h3").find("a").get("href"))
            yield f'{parsed_manga_url.scheme}://{parsed_manga_url.netloc}/{parsed_manga_url.path.split("/")[1]}'

    def get_popular_manga_url(self):
        for manga in self._popular_manga_html:
            yield f'{self.manga_panda_home_url}{manga.find("a").get("href")}'

    def get_popular_manga_title(self):
        for manga in self._popular_manga_html:
            yield f'{manga.find("a").text}'

    def get_hot_manga_data(self):
        chapters = self.get_hot_manga_chapter()
        url_list = self.get_hot_manga_url()
        manga_html_list = self.get_manga_html(url_list)
        manga_cover_list = self.get_manga_cover_url(manga_html_list)

        for chapter, url in zip(chapters, manga_cover_list):
            yield {'chapter': chapter, 'cover_url': url}

    def get_popular_manga_data(self):
        url_list = self.get_popular_manga_url()
        manga_html_list = self.get_manga_html(url_list)
        manga_title_list = self.get_popular_manga_title()
        manga_cover_list = self.get_manga_cover_url(manga_html_list)

        for title, url in zip(manga_title_list, manga_cover_list):
            yield {'title': title, 'cover_url': url}


def hot_manga_data():
    manga = MangaPanda()
    return manga.get_hot_manga_data()


def popular_manga_data():
    manga = MangaPanda()
    return manga.get_popular_manga_data()


# test()
