# pylint: disable=no-name-in-module
# pylint: disable=import-error
from pathlib import Path

import requests
from pathvalidate import sanitize_filename
from PyQt5 import uic
from PyQt5.QtCore import QRect, Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (QComboBox, QFileDialog, QGraphicsPixmapItem,
                             QGraphicsScene, QGraphicsView, QLineEdit, QWidget)
from entities.album import VkAlbum
from utils import get_album_description, print_message, validate_QLineEdit


class AlbumForm(QWidget):
    finished = pyqtSignal(VkAlbum)

    def __init__(self, album_info: dict):
        QWidget.__init__(self)
        uic.loadUi("designs/album.ui", self)
        
        self.music_dir = Path.home() / "Музыка"
                
        try:
            self.album_dict = get_album_description(album_info['artist'], album_info['title'])
            
            self.save_path = Path(self.music_dir /
                sanitize_filename(self.album_dict['artist'], "_") /
                sanitize_filename(self.album_dict['title'], "_")
            )
            self.save_path.mkdir(parents=True, exist_ok=True)
            
            self.downlaod_image_cover()
            self.set_album_cover()
            self.fill_form_field()
            
            self.finished.emit(VkAlbum(
                artist=self.album_dict['artist'],
                title=self.album_dict['title'],
                genre=self.album_dict['genre'],
            ))
            self.close()
        except TypeError:
            # self.cover_button.clicked.connect(self.cover_button_click)
            # self.result_button.clicked.connect(self.result_button_click)
            
            print_message("Информация для данного альбома не найдена")
            
    def downlaod_image_cover(self):           
        response = requests.get(self.album_dict['cover_url'])

        with open(self.save_path / "cover.jpeg", 'wb') as file:
            file.write(response.content)
    
    def set_album_cover(self):       
        scene = QGraphicsScene(self)
        image = QImage()
        image.load(str(self.save_path / "cover.jpeg"))
        image = image.scaled(308, 308, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        item = QGraphicsPixmapItem(QPixmap.fromImage(image))
        scene.addItem(item)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setScene(scene)
    
    def fill_form_field(self):                
        self.cover_line.setText(str(self.save_path / "cover.jpeg"))
        self.artist_line.setText(self.album_dict['artist'])
        self.album_line.setText(self.album_dict['title'])
        self.genre_line.setText(self.album_dict['genre'])
        self.year_line.setText(f"{self.album_dict['year']}")
        self.cover_button.setEnabled(False)
                             
    # def cover_button_click(self):
    #     files_filter = "Image file (*.jpeg *.jpg *.png)"
    #     cover = QFileDialog.getOpenFileName(self, 'Select a cover image', str(Path.home() / 'Загрузки'), files_filter)
    #     self.cover_line.setText(cover[0])

    # def result_button_click(self):
    #     if not validate_QLineEdit(self.cover_line):
    #         print_message("Обложка не выбрана.")
    #         return
        
    #     if not validate_QLineEdit(self.artist_line):
    #         print_message("Поле артиста пустое. Заполните его")
    #         return

    #     if not validate_QLineEdit(self.album_line):
    #         print_message("Поле альбома пустое. Заполните его")
    #         return

    #     if not validate_QLineEdit(self.year_line):
    #         print_message("Отсутствует год выпуска альбома")
    #         return
            
    #     self.vk_album['cover'] = self.cover_line.text()
    #     self.vk_album['artist'] = self.artist_line.text()
    #     self.vk_album['title'] = self.album_line.text()
    #     self.vk_album['genre'] = self.genre_combobox.currentText()
    #     self.vk_album['year'] = self.year_line.text()

    #     self.finished.emit(self.vk_album)
    #     self.close()
