import json
from pathlib import Path
from vk_api.audio import VkAudio
from vk_api.exceptions import AuthError
from vk_api.vk_api import VkApi
from entities.vk_album import VkAlbum
from entities.vk_session import VkSession


def download_album(vk_album: VkAlbum):   
    vkaudio = VkAudio(VkSession().get_session())

    tmp = Path.home() / "Музыка" / vk_album.artist.replace('/', '_') / vk_album.title

    tmp.mkdir(parents=True, exist_ok=True)

    # for track in vkaudio.get_iter(vk_album.owner_id, vk_album.album_id, vk_album.access_hash):
    #     print(track)

    
        