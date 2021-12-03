from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from entities.vk_album import VkAlbum


class AlbumForm(QWidget):
    def __init__(self, vk_album: dict):
        QWidget.__init__(self)
        uic.loadUi("designs/album.ui", self)

        self.artist_line.setText(vk_album['artist'])
        self.album_line.setText(vk_album['title'])
        
        self.result_button.clicked.connect(self.result_button_click)        
    
    def result_button_click(self):
        print('ok')