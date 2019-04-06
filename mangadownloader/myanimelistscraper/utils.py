import requests
from bs4 import BeautifulSoup
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

    # Cleaning data
    def clean_data(self, data):
        return data.split(':')[1].strip('\n').strip(' ')

    def clean_summary(self, data):
        indices = [0, 1]
        splitted_summary = data.replace('\n', '').split('\r')
        return (" ").join([p for i, p in enumerate(splitted_summary) if i in indices])

    def clean_author_artist(self, data):
        author_artist = data.split('(')
        if len(author_artist) > 2:
            return {"artist": author_artist[0].strip(' '), "author": author_artist[1].split(',')[1].strip(' ')}

        return {"artist": author_artist[0].strip(' '), "author": author_artist[0].strip(' ')}

    def clean_genre(self, data):
        return data.split(',')

    # Helper getter
    def get_artist_author_url(self, html):
        artist_author = html.find_all("a")

        if len(artist_author) > 1:
            return {"artist_url": f'https://myanimelist.net{artist_author[0].get("href")}', "author_url": f'https://myanimelist.net{artist_author[1].get("href")}'}

        return {"artist_url": f'https://myanimelist.net{artist_author[0].get("href")}', "author_url": f'https://myanimelist.net{artist_author[0].get("href")}'}

    # Getting data
    def get_manga_title_list(self):
        for manga in self._raw_manga_list:
            yield manga.find_all("td")[1].find(class_="detail").find(class_="hoverinfo_trigger").text

    def get_manga_link_list(self):
        for manga in self._raw_manga_list:
            yield manga.find_all("td")[1].find(class_="detail").find(class_="hoverinfo_trigger").get("href")

    def get_manga_data(self, url="https://myanimelist.net/manga/2/Berserk"):
        # Request and HTML
        manga_request = requests.get(url)
        manga_html = BeautifulSoup(manga_request.text, "lxml")

        # Titles
        english = manga_html.find(
            "h2", text="Alternative Titles").find_next_sibling("div")
        synonyms = english.find_next_sibling("div")
        japanese = synonyms.find_next_sibling("div")

        # Information
        _type = manga_html.find(
            "h2", text="Information").find_next_sibling("div")
        volumes = _type.find_next_sibling("div")
        chapters = volumes.find_next_sibling("div")
        status = chapters.find_next_sibling("div")
        published = status.find_next_sibling("div")
        genres = published.find_next_sibling("div")
        authors = genres.find_next_sibling("div")
        serialization = authors.find_next_sibling("div")

        # Summary and Image
        image_url = manga_html.find(
            class_="profileRows pb0").find_previous_sibling("div").find("img").get("src")
        summary = manga_html.find(itemprop="description").text

        full_data = {
            "image_url": image_url,
            "title": self.clean_data(english.text),
            "japanese_title": self.clean_data(japanese.text),
            "type": self.clean_data(_type.text),
            "volumes": self.clean_data(volumes.text) if self.clean_data(volumes.text) != "Unknown" else 0,
            "chapters": self.clean_data(chapters.text) if self.clean_data(chapters.text) != "Unknown" else 0,
            "status": self.clean_data(status.text),
            "published": self.clean_data(published.text),
            "genres": self.clean_genre(self.clean_data(genres.text)),
            "serialization": self.clean_data(serialization.text),
            "summary": self.clean_summary(summary)
        }

        full_data.update(self.clean_author_artist(
            self.clean_data(authors.text)))
        full_data.update(self.get_artist_author_url(authors))
        return full_data

    def get_author_artist_data(self, url):
        # Request and HTML
        author_artist_request = requests.get(url)
        author_artist_html = BeautifulSoup(author_artist_request.text, "lxml")

        # Information
        full_name = author_artist_html.find(
            class_="h1").text.strip(' ').split(',')
        image_url = author_artist_html.find(
            id="profileRows").find_previous_sibling("div").find("img").get("src")
        birthday = self.clean_data(author_artist_html.find_all(
            class_="spaceit_pad")[1].text)

        full_data = {
            "image_url": image_url,
            "last_name": full_name[0],
            "first_name": full_name[1],
            "birth_date": birthday
        }

        return full_data


manga = MyAnimeList()
# print(manga.get_manga_data('https://myanimelist.net/manga/44347/One_Punch-Man'))
print(manga.get_author_artist_data(
    'https://myanimelist.net/people/10951/Yoshitoki_Ooima'))
# for manga in manga.get_manga_link_list():
#     print(manga)
