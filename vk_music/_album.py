import re
from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup

RE_ALBUM_YEAR = re.compile(r'\w{4}')


@dataclass
class VkAlbum:
    album_id: int
    owner_id: int
    access_hash: str
    title: str
    artists: List[str]
    year: str
    url: str
    track_count: int

    @staticmethod
    def from_html(html: str):
        soup = BeautifulSoup(html, 'html.parser')
        root_element = soup.find('div', {'class': 'audio_page_block__playlists_items'})

        for album in root_element.find_all('div', {"class": ["_audio_pl", "_audio_pl_item"]}):
            info = album.find('div', {'class': 'audio_pl__info'})

            href = info.find('a', {'class': 'audio_item__title'})['href']
            owner_id, album_id, access_hash = href.split('/')[-1].split('_')
            year_text = info.find('div', {'class': 'audio_pl__year_subtitle'}).text

            artists = []
            for item in info.find_all('a', {'class': 'audio_pl_snippet__artist_link'}):
                artists.append(item.text)

            yield VkAlbum(
                album_id=int(album_id),
                owner_id=int(owner_id),
                access_hash=access_hash,
                track_count=int(album.find('div', {'class': 'audio_pl__stats_count'}).text),
                title=info.find('a', {'class': 'audio_item__title'}).text,
                artists=artists,
                year=RE_ALBUM_YEAR.search(year_text).group(0),
                url=f"https://vk.com{href}"
            )
