# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=import-error
import contextlib
import os
import re
import random
import string
from typing import Union

from fuzzywuzzy import fuzz
from pathvalidate import sanitize_filename
from PyQt5.QtWidgets import QLineEdit, QMessageBox
from vk_api.audio import VkAudio
from yandex_music import Client
from yandex_music.album.album import Album
from yandex_music.artist.artist import Artist

from entities.album import VkAlbum
from entities.session import VkSession
from entities.song import VkSong


def _search(input_t: str):
    with contextlib.redirect_stderr(open(os.devnull, "w", encoding="UTF-8")):
        with contextlib.redirect_stdout(open(os.devnull, "w", encoding="UTF-8")):
            return Client().search(sanitize_filename(input_t))

def _get_name(artist: str, title: str):
    result = ""
    
    if "feat" in title or "при участии" in title:
        result = title
    elif "feat" in artist:
        re_text = re.search(r'feat\.* .*', artist)
        result = f"{title} ({re_text.group(0)})"
    else:
        result = title

    return result

def get_album_description(artist_name: str, album_title: str) -> dict:
    """ TODO: generate docstring """ 
    
    response = _search(artist_name)

    if response.best and response.best.type != 'artist':
        raise TypeError("Артист не найден")

    artist: Artist = response.best.result

    for album in artist.get_albums(page_size=100):
        if fuzz.WRatio(album.title, album_title) > 95:
            result = {
                'artist': artist.name,
                'title': album.title,
                'genre': album.genre,
                'year': album.year,
                'cover_url': f"https://{album.cover_uri.replace('%%', '600x600')}",
                'track_count': album.track_count
            }
            break
    else:
        raise TypeError("Альбом не найден")

    return result

def find_album_by_artist(artist_name: str, album_title: str) -> Union[tuple, bool]:
    if ',' not in artist_name:
        return (artist_name, album_title)
    
    result: tuple = tuple() 
    names = [item.strip() for item in artist_name.split(',')]
    
    for name in names:
        response = _search(f"{name} {album_title}")

        if response.best and response.best.type == "album":
            album: Album = response.best.result
            result = (album.artists[0].name, album.title)
            break
    else:
        return False
        
    return result

def validate_QLineEdit(field: QLineEdit):
    input_str = field.text()

    if input_str and not input_str.isspace():
        field.setText(input_str.strip())
        return True
    else:
        field.clear()
    
    return False

def print_message(message):
    msgBox = QMessageBox()

    msgBox.setWindowTitle("Сообщение о ошибке")
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(message)

    msgBox.exec()

def get_tracklist_iter(album: VkAlbum):
    vkaudio = VkAudio(VkSession().get_session())

    owner_id = album.owner_id
    album_id = album.album_id
    access_hash = album.access_hash

    for i, track in enumerate(vkaudio.get_iter(owner_id, album_id, access_hash), 1):
        yield VkSong(
            track_num=i,
            artist=album.artist,
            album=album.title,
            title=_get_name(track['artist'], track['title']),
            track_code="".join(random.choice(string.ascii_lowercase) for i in range(25)),
            genre=album.genre,
            year=album.year,
            url=track['url']
        )