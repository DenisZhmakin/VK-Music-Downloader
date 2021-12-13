import os
import utils
import requests

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3 

from pathlib import Path
from PyQt5.QtCore import QThread
from vk_api.audio import VkAudio

from entities.vk_album import VkAlbum
from vk_session import VkSession
from entities.vk_song import VkSong

class VkDownloader(QThread):
    def __init__(self, vk_album: VkAlbum):
        QThread.__init__(self)
        self.vk_album = vk_album

    def run(self):
        vkaudio = VkAudio(VkSession().get_session())

        owner_id = self.vk_album.owner_id
        album_id = self.vk_album.album_id
        access_hash = self.vk_album.access_hash

        album_folder = Path.home() / "Музыка" / self.vk_album.artist.replace("/", "_") / self.vk_album.title
        album_folder.mkdir(parents=True, exist_ok=True)
       
        for i, track in enumerate(vkaudio.get_iter(owner_id, album_id, access_hash), 1):
            vk_song = VkSong(
                number=i,
                cover=self.vk_album.cover,
                track_code=utils.generate_track_code(),
                artist=self.vk_album.artist,
                album=self.vk_album.title,
                title=track['title'],
                genre=self.vk_album.genre,
                year=self.vk_album.year,
                url=track['url']
            )

            self.download_track(vk_song, album_folder)
            self.set_mp3_tags(vk_song, album_folder)
            self.set_cover_image(vk_song, album_folder)
            self.rename_file(vk_song, album_folder)
        
    def download_track(self, track: VkSong, music_dir: Path):
        save_file = Path(music_dir / f"{track.track_code}.mp3")

        if 'long_chunk=1' in track.url:
            r = requests.get(track.url)

            with open(save_file, 'wb') as f: 
                f.write(r.content)
        elif 'index.m3u8' in track.url:
            ts_file = f"{track.track_code}.ts"
            os.system(f"""
                cd /tmp
                streamlink --output {ts_file} {track.url} best
                ffmpeg -i {ts_file} -ab 320k "{str(save_file)}"
            """)
        
    def set_mp3_tags(self, track: VkSong, music_dir: Path):
        audio = MP3(filename=str(Path(music_dir / f"{track.track_code}.mp3")), ID3=EasyID3)

        audio['title'] = track.title
        audio['artist'] = track.artist
        audio['tracknumber'] = str(track.number)
        audio['date'] = str(track.year)
        audio['album'] = track.album
        audio['genre'] = track.genre

        audio.save()
    
    def set_cover_image(self, track: VkSong, music_dir: Path):
        audio = ID3(Path(music_dir / f"{track.track_code}.mp3"))

        with open(track.cover, 'rb') as album_art:
            audio['APIC'] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3, desc=u'Cover',
                data=album_art.read()
            )

        audio.save()

    def rename_file(self, track: VkSong, music_dir: Path):
        file = Path(music_dir / f"{track.track_code}.mp3")

        new_name = f"{str(track.number).zfill(2)}. {track.title}.mp3"

        if "/" in new_name:
            new_name = new_name.replace('/', '_')

        file.rename(music_dir / new_name)
    
