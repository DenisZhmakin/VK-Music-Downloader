import time
from typing import Generator
from pathlib import Path

from bs4 import BeautifulSoup

from vk_api import VkApi
from vk_api.audio_url_decoder import decode_audio_url
from entities.album import VkAlbum

from entities.artist import VkArtist

RPS_DELAY_RELOAD_AUDIO = 1.5
RPS_DELAY_LOAD_SECTION = 2.0

DEFAULT_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Connection': 'keep-alive'
}


class VkAudioNG:
    def __init__(self, vk_api: VkApi):
        self.vk_api = vk_api

    def search_artist_nickname(self, author: str) -> VkArtist:
        if not isinstance(author, str):
            raise TypeError(f"Type {type(author)} was passed instead of string.")

        if not (author and not author.isspace()):
            raise ValueError("An empty string was passed.")

        response = self.vk_api.http.post(
            'https://m.vk.com/audio',
            headers=DEFAULT_HEADERS,
            data={
                '_ajax': 1,
                'q': author.strip()
            }
        ).json()

        result = VkArtist(response['data'][2])

        return result

    def get_artist_albums_iter(self, artist: VkArtist) -> Generator[VkAlbum, None, None]:
        """Искать альбомы артиста по имени

        :param author: str - имя артиста.
        """
        if not artist.nickname:
            return

        link = f"https://vk.com/artist/{artist.nickname}/albums"
        html = self.vk_api.http.get(link).text

        yield from VkAlbum.from_html(html)

    def get_artist_mini_albums_iter(self, artist: VkArtist) -> Generator[VkAlbum, None, None]:
        """Искать альбомы артиста по имени

        :param author: str - имя артиста.
        """
        if not artist.nickname:
            return

        link = f"https://vk.com/artist/{artist.nickname}/singles"
        html = self.vk_api.http.get(link).text

        for album in VkAlbum.from_html(html):
            if album.track_count == 1:
                continue

            yield album

    def get_artist_singles_iter(self, artist: VkArtist) -> Generator[VkAlbum, None, None]:
        """Искать альбомы артиста по имени

        :param author: str - имя артиста.
        """
        if not artist.nickname:
            return

        link = f"https://vk.com/artist/{artist.nickname}/singles"
        html = self.vk_api.http.get(link).text

        for album in VkAlbum.from_html(html):
            if album.track_count > 1:
                continue

            yield album
