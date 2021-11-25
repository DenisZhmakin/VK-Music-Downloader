import wget
import random
import string
import os
from pathlib import Path
from vk_api.audio import VkAudio
from entities.vk_album import VkAlbum
from entities.vk_session import VkSession
from entities.vk_song import VkSong


def download_album(vk_album: VkAlbum):   
    vkaudio = VkAudio(VkSession().get_session())

    tmp = Path.home() / "Музыка" / vk_album.artist.replace("/", "_") / vk_album.title

    tmp.mkdir(parents=True, exist_ok=True)

    number = 1

    for track in vkaudio.get_iter(vk_album.owner_id, vk_album.album_id, vk_album.access_hash):
        download_track(VkSong(
            number=number,
            title=track['title'],
            album=vk_album.title,
            artist=vk_album.artist,
            url=track['url']    
        ), tmp)

        number += 1

def download_track(track: VkSong, tmp: Path):
    save_path = Path(tmp / f"{str(track.number).zfill(2)}. {track.title}.mp3")

    letters = string.ascii_lowercase

    if 'long_chunk=1' in track.url:
        wget.download(track.url, str(save_path))
    elif 'index.m3u8' in track.url:
        ts_file = f"{''.join(random.choice(letters) for i in range(16))}.ts"
        os.system(f"""
            cd /tmp
            streamlink --output {ts_file} {track.url} best
            ffmpeg -i {ts_file} -ab 320k "{str(save_path)}"
        """)
