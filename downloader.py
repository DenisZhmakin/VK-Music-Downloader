import os
import utils
import requests

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3 

from pathlib import Path
from PyQt5.QtCore import QThread
from vk_api.audio import VkAudio
from pathvalidate import sanitize_filename

from entities.album import VkAlbum
from entities.session import VkSession
from entities.song import VkSong

class VkDownloader(QThread):
    def __init__(self, album: VkAlbum):
        QThread.__init__(self)
        self.album = album
        self.music_dir = Path.home() / "Музыка" / sanitize_filename(album.artist, "_") / sanitize_filename(album.title, "_")
        self.music_dir.mkdir(parents=True, exist_ok=True)

        self.tmp_dir = Path("/tmp") / sanitize_filename(album.artist, "_") / sanitize_filename(album.title, "_")
        self.tmp_dir.mkdir(parents=True, exist_ok=True)

    def run(self):
        vkaudio = VkAudio(VkSession().get_session())

        owner_id = self.album.owner_id
        album_id = self.album.album_id
        access_hash = self.album.access_hash
       
        for i, track in enumerate(vkaudio.get_iter(owner_id, album_id, access_hash), 1):
            vk_song = VkSong(
                number=i,
                cover=self.album.cover,
                track_code=utils.generate_track_code(),
                artist=self.album.artist,
                album=self.album.title,
                title=track['title'],
                genre=self.album.genre,
                year=self.album.year,
                url=track['url']
            )

            self.download_track(vk_song)
            self.set_mp3_tags(vk_song)
            self.set_cover_image(vk_song)
            self.rename_file(vk_song)
        
    def download_track(self, track: VkSong):
        save_file_path = Path(self.music_dir / f"{track.track_code}.mp3")

        if 'long_chunk=1' in track.url:
            r = requests.get(track.url)

            with open(save_file_path, 'wb') as f: 
                f.write(r.content)
        elif 'index.m3u8' in track.url:
            # TODO: заменить на subprocess

            ts_file = str(self.tmp_dir / f"{track.track_code}.ts")
            os.system(f"""           
                streamlink --output "{ts_file}" {track.url} best
                ffmpeg -i "{ts_file}" -ab 320k "{str(save_file_path)}"
            """)
        
    def set_mp3_tags(self, track: VkSong):
        audio = MP3(filename=str(Path(self.music_dir / f"{track.track_code}.mp3")), ID3=EasyID3)

        audio['title'] = track.title
        audio['artist'] = track.artist
        audio['tracknumber'] = str(track.number)
        audio['date'] = track.year
        audio['album'] = track.album
        audio['genre'] = track.genre

        audio.save()
    
    def set_cover_image(self, track: VkSong):
        audio = ID3(Path(self.music_dir / f"{track.track_code}.mp3"))

        with open(track.cover, 'rb') as album_art:
            audio['APIC'] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3, desc=u'Cover',
                data=album_art.read()
            )

        audio.save()

    def rename_file(self, track: VkSong):
        file = Path(self.music_dir / f"{track.track_code}.mp3")
        
        new_name = f"{str(track.number).zfill(2)}. {sanitize_filename(track.title, '_')}.mp3"

        if "/" in new_name:
            new_name = new_name.replace('/', '_')

        file.rename(self.music_dir / new_name)
    
