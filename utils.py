# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=import-error
import contextlib
import os
import random
import string

from fuzzywuzzy import fuzz
from pathvalidate import sanitize_filename
from PyQt5.QtWidgets import QLineEdit, QMessageBox
from vk_api.audio import VkAudio
from yandex_music import Client
from yandex_music.artist.artist import Artist
from entities.album import VkAlbum
from entities.session import VkSession
from entities.song import VkSong


def get_album_description(artist_name: str, album_title: str) -> dict:
    """ TODO: generate docstring """   
    with contextlib.redirect_stderr(open(os.devnull, "w", encoding="UTF-8")):
        with contextlib.redirect_stdout(open(os.devnull, "w", encoding="UTF-8")):
            response = Client().search(sanitize_filename(artist_name))

    if response.best and response.best.type != 'artist':
        raise TypeError("Артист не найден")

    artist: Artist = response.best.result

    for album in artist.get_albums(page_size=100):
        if fuzz.WRatio(album.title, album_title) > 90:
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

def get_cover_url_of_album(artist_name: str, album_title: str):
    response = Client().search(artist_name.replace('/', '_'))
    
    if response.best and response.best.type != 'artist':
        raise TypeError("Артист не найден")
    
    artist: Artist = response.best.result

    for album in artist.get_albums(page_size=100):
        if fuzz.WRatio(album.title, album_title) > 92:
            result = album.cover_uri.replace("%%", "600x600")
            break
    else:
        raise TypeError("Альбом не найден")
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

def generate_track_code():
    return f"{''.join(random.choice(string.ascii_lowercase) for i in range(25))}"

def vk_song_iter(vk_album: VkAlbum):
    vkaudio = VkAudio(VkSession().get_session())

    owner_id = vk_album.owner_id
    album_id = vk_album.album_id
    access_hash = vk_album.access_hash

    for i, track in enumerate(vkaudio.get_iter(owner_id, album_id, access_hash), 1):
        yield VkSong(
            number=i,
            cover=vk_album.cover,
            track_code=generate_track_code(),
            artist=vk_album.artist,
            album=vk_album.title,
            title=track['title'],
            genre=vk_album.genre,
            year=vk_album.year,
            url=track['url']
        )
  