# pylint: disable=no-name-in-module
# pylint: disable=import-error
from pathlib import Path
from tempfile import TemporaryFile
import tempfile

import requests
from entities.album import VkAlbum
from pathvalidate import sanitize_filename
from PyQt5 import uic
from PyQt5.QtCore import QRect, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QComboBox, QFileDialog, QGraphicsPixmapItem,
                             QGraphicsScene, QGraphicsView, QLineEdit, QWidget)
from utils import get_album_description, print_message, validate_QLineEdit


class AlbumForm(QWidget):
    finished = pyqtSignal(VkAlbum)

    def __init__(self, artist: str, title: str, album_id: int, owner_id: int, access_hash: str):
        QWidget.__init__(self)
        uic.loadUi("designs/album.ui", self)
        
        self.result_button.clicked.connect(self.result_button_click)

        album_dict = get_album_description(artist, title)
        
        if album_dict:
            self.set_album_cover(album_dict['cover_url'])
            self.fill_form_field(album_dict)
            
            self.vk_album = VkAlbum(
                artist=album_dict['artist'],
                title=album_dict['title'],
                genre=album_dict['genre'],
                year=album_dict['year'],
                cover_url=album_dict['cover_url'],
                album_id=album_id,
                owner_id=owner_id,
                access_hash=access_hash
            )
        else:
            print_message("Информация для данного альбома не найдена")
            

    def set_album_cover(self, cover_url: str):
        response = requests.get(cover_url)
        scene = QGraphicsScene(self)
        
        image = QImage()
        image.loadFromData(response.content)
        
        image = image.scaled(308, 308, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        item = QGraphicsPixmapItem(QPixmap.fromImage(image))
        scene.addItem(item)
        
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setScene(scene)
    
    def fill_form_field(self, album_dict: dict):                
        self.artist_line.setText(album_dict['artist'])
        self.album_line.setText(album_dict['title'])
        self.genre_line.setText(album_dict['genre'])
        self.year_line.setText(f"{album_dict['year']}")

    def result_button_click(self):
        self.finished.emit(self.vk_album)
        self.close()
