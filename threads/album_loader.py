from entities.session import VkSession
from PyQt5.QtCore import QThread, pyqtSignal
from vk_api.audio import VkAudio


class AlbumLoader(QThread):
    album_get = pyqtSignal(dict)
    
    def __init__(self, artist: str):
        QThread.__init__(self)
        self.artist = artist

    def run(self):
        vkaudio = VkAudio(VkSession().get_session())
        
        for album in vkaudio.search_artist_albums(self.artist):
            album['type'] = "Альбом"
            self.album_get.emit(album)
        
        for album in vkaudio.search_artist_ep_and_singles(self.artist):
            count_track = len(vkaudio.get(album['owner_id'], album['id'], album['access_hash']))
            
            if count_track > 1:
                album['type'] = "Мини-альбом"
            else:
                album['type'] = "Сингл"
            
            self.album_get.emit(album)
