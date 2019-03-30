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
        self._todays_manga_html = self._manga_panda_home_html.find(
            id="latestchapters").find_all("table")[0].find_all("tr")
        self._yesterdays_manga_html = self._manga_panda_home_html.find(
            id="latestchapters").find_all("table")[1].find_all("tr")
        self._older_manga_html = self._manga_panda_home_html.find(
            id="latestchapters").find_all("table")[2].find_all("tr")

    # Manga information methods

    def get_manga_html(self, url_list):
        for url in url_list:
            yield requests.get(url).text

    def get_manga_cover_url(self, manga_html_list):
        for manga_html in manga_html_list:
            manga_home_html = BeautifulSoup(manga_html, 'lxml')
            yield manga_home_html.find(id="mangaimg").find("img").get("src")

    def get_manga_genre(self, manga_html_list):
        genre_list = []
        for manga_html in manga_html_list:
            manga_home_html = BeautifulSoup(manga_html, 'lxml')
            for genre in manga_home_html.find(id="mangaproperties").find_all(class_="genretags"):
                if genre.text not in genre_list:
                    genre_list.append(genre.text)
            yield genre_list

    def get_todays_manga(self):
        for manga in self._todays_manga_html:
            chapter_list = []
            title = manga.find_all("td")[1].find_all("a")[0].text
            chapters = manga.find_all("td")[1].find_all("a")[1:]

            for chapter in chapters:
                chapter_list.append(chapter.text)

            yield {'title': title, 'chapters': chapter_list}

    def get_yesterdays_manga(self):
        for manga in self._todays_manga_html:
            chapter_list = []
            title = manga.find_all("td")[1].find_all("a")[0].text
            chapters = manga.find_all("td")[1].find_all("a")[1:]

            for chapter in chapters:
                chapter_list.append(chapter.text)

            yield {'title': title, 'chapters': chapter_list}

    def get_older_manga(self):
        for manga in self._older_manga_html:
            chapter_list = []
            title = manga.find_all("td")[1].find_all("a")[0].text
            chapters = manga.find_all("td")[1].find_all("a")[1:]
            date = manga.find_all("td")[2].text

            for chapter in chapters:
                chapter_list.append(chapter.text)

            yield {'title': title, 'chapters': chapter_list, 'date': date}

    # Hot manga methods
    def get_hot_manga_chapter(self):
        for manga in self._latest_hot_manga_html:
            yield manga.find("h3").find("a").text

    def get_hot_manga_url(self):
        for manga in self._latest_hot_manga_html:
            parsed_manga_url = urlparse(manga.find("h3").find("a").get("href"))
            yield f'{parsed_manga_url.scheme}://{parsed_manga_url.netloc}/{parsed_manga_url.path.split("/")[1]}'

    # Popular manga methods
    def get_popular_manga_url(self):
        for manga in self._popular_manga_html:
            yield f'{self.manga_panda_home_url}{manga.find("a").get("href")}'

    def get_popular_manga_title(self):
        for manga in self._popular_manga_html:
            yield f'{manga.find("a").text}'

    def get_popular_manga_chapter(self):
        for manga in self._popular_manga_html:
            yield f'{manga.find(class_="chapters").text}'

    def get_popular_manga_summary(self, manga_html_list):
        for manga_html in manga_html_list:
            manga_home_html = BeautifulSoup(manga_html, 'lxml')
            yield f'{manga_home_html.find(id="readmangasum").find("p").text}'

    def get_popular_manga_cover_genre_summary(self, manga_html_list):
        for manga_html in manga_html_list:
            genre_list = []
            manga_home_html = BeautifulSoup(manga_html, 'lxml')
            cover_url = manga_home_html.find(
                id="mangaimg").find("img").get("src")
            summary = manga_home_html.find(id="readmangasum").find("p").text
            for genre in manga_home_html.find(id="mangaproperties").find_all(class_="genretags"):
                if genre.text not in genre_list:
                    genre_list.append(genre.text)
            yield {'cover_url': cover_url, 'summary': summary, 'genre': genre_list}

    # Summary methods
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
        manga_chapter_list = self.get_popular_manga_chapter()
        manga_cover_genre_summary = self.get_popular_manga_cover_genre_summary(
            manga_html_list)

        for title, chapter, manga in zip(manga_title_list, manga_chapter_list, manga_cover_genre_summary):
            yield {'title': title, 'chapter': chapter, 'cover_url': manga['cover_url'],
                   'summary': manga['summary'], 'genre': manga['genre']}


def hot_manga_data():
    manga = MangaPanda()
    return manga.get_hot_manga_data()


def popular_manga_data():
    manga = MangaPanda()
    return manga.get_popular_manga_data()


def todays_manga_data():
    manga = MangaPanda()
    return manga.get_todays_manga()


def yesterdays_manga_data():
    manga = MangaPanda()
    return manga.get_yesterdays_manga()


def older_manga_data():
    manga = MangaPanda()
    return manga.get_older_manga()

# todays_manga_data()
# test()

# popular_manga_data()
