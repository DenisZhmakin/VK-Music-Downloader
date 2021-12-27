import subprocess
import tempfile
from pathlib import Path

import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3
from pathvalidate import sanitize_filename
from PyQt5.QtCore import QThread

from utils import get_tracklist_iter
from entities.album import VkAlbum
from entities.song import VkSong


class VkDownloader(QThread):
    def __init__(self, album: VkAlbum):
        QThread.__init__(self)
        self.album = album
        
        self.tmp_dir = Path(
            Path(tempfile.gettempdir()) /
            sanitize_filename(album.artist, "_") /
            sanitize_filename(album.title, "_")
        )
        self.music_dir = Path.home() / "Музыка"
        self.tmp_dir = Path(tempfile.gettempdir())
        
        self.tmp_dir.mkdir(parents=True, exist_ok=True)

    def run(self):
        for vk_song in get_tracklist_iter(self.album):
            self.download_track(vk_song)
            self.set_mp3_tags(vk_song)
            self.set_cover_image(vk_song)
            self.rename_file(vk_song)
   
    def download_track(self, track: VkSong):
        mp3_file = self.album.album_path / f"{track.track_code}.mp3"
        ts_file = self.tmp_dir / f"{track.track_code}.ts"

        if 'index.m3u8' in track.url:
            subprocess.call(["streamlink", "--output", ts_file, track.url, "best"])
            subprocess.call(["ffmpeg", "-i", ts_file, "-ab", "320k", mp3_file])
        elif 'long_chunk=1' in track.url:
            responce = requests.get(track.url)
            mp3_file.write_bytes(responce.content)

    def set_mp3_tags(self, track: VkSong):
        audio = MP3(filename=Path(self.album.album_path / f"{track.track_code}.mp3"), ID3=EasyID3)

        audio['title'] = track.title
        audio['artist'] = track.artist
        audio['tracknumber'] = str(track.number)
        audio['date'] = str(track.year)
        audio['album'] = track.album
        audio['genre'] = track.genre

        audio.save()

    def set_cover_image(self, track: VkSong):
        audio = ID3(Path(self.album.album_path / f"{track.track_code}.mp3"))

        with open(track.cover, 'rb') as album_art:
            audio['APIC'] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3, desc='Cover',
                data=album_art.read()
            )

        audio.save()

    def rename_file(self, track: VkSong):
        file = Path(self.album.album_path / f"{track.track_code}.mp3")

        new_name = f"{str(track.number).zfill(2)}. {sanitize_filename(track.title, '_')}.mp3"

        file.rename(self.album.album_path / new_name)
