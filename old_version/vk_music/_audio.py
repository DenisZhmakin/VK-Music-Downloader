import time
from typing import Generator
from pathlib import Path

from bs4 import BeautifulSoup

from vk_api import VkApi

from ._album import VkAlbum
from ._artist import VkArtist
from audio_url_decoder import decode_audio_url

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
    def __init__(self, vk: VkApi):
        self.vk = vk

    def search_artist_nickname(self, author: str) -> VkArtist:
        if not isinstance(author, str):
            raise TypeError(f"Type {type(author)} was passed instead of string.")

        if not (author and not author.isspace()):
            raise ValueError("An empty string was passed.")

        response = self.vk.http.post(
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
        html = self.vk.http.get(link).text

        yield from VkAlbum.from_html(html)

    def get_artist_mini_albums_iter(self, artist: VkArtist) -> Generator[VkAlbum, None, None]:
        """Искать альбомы артиста по имени

        :param author: str - имя артиста.
        """
        if not artist.nickname:
            return

        link = f"https://vk.com/artist/{artist.nickname}/singles"
        html = self.vk.http.get(link).text

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
        html = self.vk.http.get(link).text

        for album in VkAlbum.from_html(html):
            if album.track_count > 1:
                continue

            yield album
    
    def get_artist_topaudios_iter(self, artist: str, is_nickname=False):
        """Искать альбомы артиста по имени

        :param author: str - имя артиста.
        """        
        if not is_nickname:
            nickname = self.search_artist_nickname(artist)
        else:
            nickname = artist

        link = f"https://vk.com/artist/{nickname}/top_audios"
        playlist_id = self.scrap_playlist_id(self.vk.http.get(link).text)
        
        start_from = ""
        while True:
            response = self.vk.http.post(
                'https://vk.com/al_audio.php?act=load_catalog_section',
                headers=DEFAULT_HEADERS,
                data={
                    'al': 1,
                    'section_id': playlist_id,
                    'start_from': start_from
                }
            ).json()
            
            data = response['payload'][1][1]['playlist']
                 
            yield from scrap_tracks(data['list'])
            
            if data['hasMore']:
                start_from = data['nextOffset']
            else:
                break

def scrap_tracks(track_list: dict):
    last_request = 0.0

    for track in track_list:
        delay = RPS_DELAY_RELOAD_AUDIO - (time.time() - last_request)
    
        if delay > 0:
            time.sleep(delay)
            
        audio_hashes = track[13].split("/")
        track_id = f"{track[1]}_{track[0]}_{audio_hashes[2]}_{audio_hashes[5]}"
        
        response = self.vk.http.post(
            'https://vk.com/al_audio.php?act=reload_audio',
            headers=DEFAULT_HEADERS,
            data={
                'al': 1,
                'ids': track_id
            }
        ).json()

        last_request = time.time()

        link = decode_audio_url(response['payload'][1][0][0][2], self.user_id)

        yield {
            'id': track[0],
            'owner_id': track[1],
            'track_covers': track[14].split(',') if track[14] else [],
            'url': link,
            'artist': track[4],
            'title': track[3],
            'duration': track[5],
        }
             

def scrap_playlist_id(html: str):
    """ddddddddd"""
    soup = BeautifulSoup(html, 'html.parser')
    playlist_id = soup.find('div', {'class': [
        "audio_page__audio_rows_list",
        "_audio_page__audio_rows_list"
    ]})['data-playlist-id']
        
    return playlist_id
