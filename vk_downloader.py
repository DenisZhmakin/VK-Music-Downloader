import os
import random 
import string
import requests

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

    def quit(self):
        self.quit()

    def run(self):
        vkaudio = VkAudio(VkSession().get_session())

        owner_id = self.vk_album.owner_id
        album_id = self.vk_album.album_id
        access_hash = self.vk_album.access_hash

        album_folder = Path.home() / "Музыка" / self.vk_album.artist.replace("/", "_") / self.vk_album.title
        album_folder.mkdir(parents=True, exist_ok=True)
       
        for i, val in enumerate(vkaudio.get_iter(owner_id, album_id, access_hash), 1):
            self.download_track(VkSong(
                number=i,
                title=val['title'],
                album=self.vk_album.title,
                artist=self.vk_album.artist,
                url=val['url']    
            ), album_folder)
        
    def download_track(self, track: VkSong, tmp: Path):
        save_path = Path(tmp / f"{str(track.number).zfill(2)}. {track.title}.mp3")

        letters = string.ascii_lowercase
    
        if 'long_chunk=1' in track.url:
            r = requests.get(track.url)

            with open(save_path, 'wb') as f: 
                f.write(r.content)
        elif 'index.m3u8' in track.url:
            ts_file = f"{''.join(random.choice(letters) for i in range(16))}.ts"
            os.system(f"""
                cd /tmp
                streamlink --output {ts_file} {track.url} best
                ffmpeg -i {ts_file} -ab 320k "{str(save_path)}"
            """)
        
