import json
from pathlib import Path
from vk_api.audio import VkAudio
from vk_api.exceptions import AuthError
from vk_api.vk_api import VkApi
from entities.vk_album import VkAlbum


def download_album(vk_album: VkAlbum):
    with open(Path.home() / '.vkmusicload.conf', "r") as read_file:
        data = json.load(read_file)
    
    vk_session = VkApi(
        login=data['login'],
        password=['password']
    )

    try:
        vk_session.auth(token_only=True)
    except AuthError as error_msg:
        print(error_msg)
            
    vkaudio = VkAudio(vk_session)

    for track in vkaudio.get_iter(vk_album.owner_id, vk_album.album_id, vk_album.access_hash):
        print(track)

    
        