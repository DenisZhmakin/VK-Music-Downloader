from entities.session import VkSession
from PyQt5.QtCore import QThread, pyqtSignal
from vk_api.audio_ng import VkAudioNG


class AlbumLoader(QThread):
    album_get = pyqtSignal(dict)
    
    def __init__(self, artist: str):
        QThread.__init__(self)
        self.artist = artist

    def run(self):
        vkaudio = VkAudioNG(VkSession().get_session())
        artist_nick = vkaudio.search_artist_nickname(self.artist)
        
        for album in vkaudio.get_artist_albums_iter(artist_nick):
            _temp = {
                "artist": ", ".join(album.artists),
                "title": album.title,
                "type": "Альбом",
                "id": album.album_id,
                "owner_id": album.owner_id,
                "access_hash": album.access_hash,
            }
            self.album_get.emit(_temp)
        
        for album in vkaudio.get_artist_mini_albums_iter(artist_nick):
            _temp = {
                "artist": ", ".join(album.artists),
                "title": album.title,
                "type": "Мини-альбом",
                "id": album.album_id,
                "owner_id": album.owner_id,
                "access_hash": album.access_hash,
            }
            self.album_get.emit(_temp)
              
        for album in vkaudio.get_artist_singles_iter(artist_nick):
            _temp = {
                "artist": ", ".join(album.artists),
                "title": album.title,
                "type": "Сингл",
                "id": album.album_id,
                "owner_id": album.owner_id,
                "access_hash": album.access_hash,
            }
            self.album_get.emit(_temp)
