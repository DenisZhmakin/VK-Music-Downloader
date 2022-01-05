import subprocess
import tempfile
from pathlib import Path

import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3
from pathvalidate import sanitize_filename
from PyQt5.QtCore import QThread
from vk_api.audio import VkAudio

from entities.album import VkAlbum
from entities.session import VkSession
from entities.song import VkSong
from utils import get_tracklist_iter


class VkDownloader(QThread):
    def __init__(self, album: VkAlbum):
        QThread.__init__(self)
        self.album = album

        self.tmp_dir = Path(tempfile.gettempdir()) / sanitize_filename(album.artist, "_") / sanitize_filename(album.title, "_")
        self.tmp_dir.mkdir(parents=True, exist_ok=True)

        self.music_dir = Path.home() / "Музыка" / sanitize_filename(album.artist, "_") / sanitize_filename(album.title, "_")       
        self.music_dir.mkdir(parents=True, exist_ok=True)

        responce = requests.get(album.cover_url)
        self.cover_file = self.tmp_dir / "cover.jpeg"
        self.cover_file.write_bytes(responce.content)
        
    def run(self):
        for vk_song in get_tracklist_iter(self.album):
            self.download_track(vk_song)
            self.set_mp3_tags(vk_song)
            self.set_cover_image(vk_song)
            self.rename_file(vk_song)
   
    def download_track(self, track: VkSong):
        mp3_file = self.music_dir / f"{track.track_code}.mp3"
        ts_file = self.tmp_dir / f"{track.track_code}.ts"

        if 'index.m3u8' in track.url:
            subprocess.call(["streamlink", "--output", ts_file, track.url, "best"])
            subprocess.call(["ffmpeg", "-i", ts_file, "-ab", "320k", mp3_file])
        elif 'long_chunk=1' in track.url:
            responce = requests.get(track.url)
            mp3_file.write_bytes(responce.content)

    def set_mp3_tags(self, track: VkSong):
        audio = MP3(filename=self.music_dir / f"{track.track_code}.mp3", ID3=EasyID3)

        audio['title'] = track.title
        audio['artist'] = track.artist
        audio['tracknumber'] = str(track.track_num)
        audio['date'] = str(track.year)
        audio['album'] = track.album
        audio['genre'] = track.genre

        audio.save()

    def set_cover_image(self, track: VkSong):
        audio = ID3(Path(self.music_dir / f"{track.track_code}.mp3"))

        with open(self.cover_file, 'rb') as album_art:
            audio['APIC'] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3, desc='Cover',
                data=album_art.read()
            )

        audio.save()

    def rename_file(self, track: VkSong):
        file = Path(self.music_dir / f"{track.track_code}.mp3")

        new_name = f"{str(track.track_num).zfill(2)}. {sanitize_filename(track.title)}.mp3"

        file.rename(self.music_dir / new_name)
