from pathlib import Path
from PyQt5 import uic
from PyQt5.QtCore import QLine, pyqtSignal
from PyQt5.QtWidgets import QComboBox, QFileDialog, QLineEdit, QWidget

from utils import print_message, validate_QLineEdit

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

        self.cover_button.clicked.connect(self.cover_button_click)
        self.result_button.clicked.connect(self.result_button_click)
        
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
            print_message("Поле года альбома пустое. Заполните его")
            return
            
        self.vk_album['cover'] = self.cover_line.text()
        self.vk_album['artist'] = self.artist_line.text()
        self.vk_album['title'] = self.album_line.text()
        self.vk_album['genre'] = self.genre_combobox.currentText()
        self.vk_album['year'] = int(self.year_line.text())

        self.finished.emit(self.vk_album)
        self.close()
