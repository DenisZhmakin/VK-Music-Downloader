# pylint: disable=no-name-in-module
# pylint: disable=import-error
from pathlib import Path

import requests
from pathvalidate import sanitize_filename
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QComboBox, QFileDialog, QGraphicsPixmapItem,
                             QGraphicsScene, QGraphicsView, QLineEdit, QWidget)
from utils import get_cover_url_of_album, print_message, validate_QLineEdit

mp3_genre = ["Rap", "Rock"]

class AlbumForm(QWidget):
    finished = pyqtSignal(dict)

    def __init__(self, vk_album: dict):
        QWidget.__init__(self)
        uic.loadUi("designs/album.ui", self)

        self.vk_album = vk_album
        self.genre_combobox: QComboBox = self.genre_combobox
        self.artist_line: QLineEdit = self.artist_line
        self.album_line: QLineEdit = self.album_line
        self.cover_line: QLineEdit = self.cover_line
        self.year_line: QLineEdit = self.year_line

        self.genre_combobox.addItems(mp3_genre)
        self.artist_line.setText(vk_album['artist'])
        self.album_line.setText(vk_album['title'])
        
        self.music_dir = Path.home() / "Музыка" / sanitize_filename(vk_album['artist'], "_") / sanitize_filename(vk_album['title'], "_")
        self.music_dir.mkdir(parents=True, exist_ok=True)

        self.cover_button.clicked.connect(self.cover_button_click)
        self.result_button.clicked.connect(self.result_button_click)
                
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
               
        self.load_cover()
    
    def load_cover(self):
        cover_url = get_cover_url_of_album(self.vk_album['artist'], self.vk_album['title'])
        
        img_path = Path(self.music_dir / "cover.jpeg")
        response = requests.get("http://" + cover_url)

        with open(img_path, 'wb') as file:
            file.write(response.content)
                        
    def cover_button_click(self):
        files_filter = "Image file (*.jpeg *.jpg *.png)"
        cover = QFileDialog.getOpenFileName(self, 'Select a cover image', str(Path.home() / 'Загрузки'), files_filter)
        self.cover_line.setText(cover[0])

    def result_button_click(self):
        if not validate_QLineEdit(self.cover_line):
            print_message("Обложка не выбрана.")
            return
        
        if not validate_QLineEdit(self.artist_line):
            print_message("Поле артиста пустое. Заполните его")
            return

        if not validate_QLineEdit(self.album_line):
            print_message("Поле альбома пустое. Заполните его")
            return

        if not validate_QLineEdit(self.year_line):
            print_message("Отсутствует год выпуска альбома")
            return
            
        self.vk_album['cover'] = self.cover_line.text()
        self.vk_album['artist'] = self.artist_line.text()
        self.vk_album['title'] = self.album_line.text()
        self.vk_album['genre'] = self.genre_combobox.currentText()
        self.vk_album['year'] = self.year_line.text()

        self.finished.emit(self.vk_album)
        self.close()
