#!/usr/bin/env python3
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (QApplication, QHeaderView, QTableWidgetItem,
                             QWidget)
from vk_api.audio import VkAudio

from entities.album import VkAlbum
from entities.session import VkSession
from forms.album_form import AlbumForm
from forms.auth_form import AuthForm
from threads.album_loader import AlbumLoader
from threads.downloader import VkDownloader
from utils import find_album_by_artist, print_message, validate_QLineEdit


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("designs/main.ui", self)

        self._album_info: dict = None

        self.download_button.clicked.connect(self.download_button_click)
        self.search_button.clicked.connect(self.search_button_click)
        self.configure_table()

        if not Path(Path.home() / '.vkmusicload.conf').exists():
            self.auth = AuthForm()
            self.auth.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.auth.show()

    def configure_table(self):
        self.albums_tablewidget.setHorizontalHeaderLabels(
            [
                "Исполнитель",
                "Название альбома",
                "Тип",
                "album_id",
                "owner_id",
                "access_hash"
            ]
        )

        self.albums_tablewidget.setColumnHidden(3, True)
        self.albums_tablewidget.setColumnHidden(4, True)
        self.albums_tablewidget.setColumnHidden(5, True)

        self.albums_tablewidget.horizontalHeader()\
            .setSectionResizeMode(QHeaderView.Stretch)
      
    def search_button_click(self):
        self.albums_tablewidget.setRowCount(0)
        
        if validate_QLineEdit(self.artist_lineedit):
            self.album_loader = AlbumLoader(self.artist_lineedit.text())
            self.album_loader.album_get.connect(self.album_get_handler)
            self.album_loader.start()
    
    @pyqtSlot(dict)
    def album_get_handler(self, value):
        albumRow = self.albums_tablewidget.rowCount()
        
        self.albums_tablewidget.insertRow(albumRow)

        self.albums_tablewidget.setItem(
            albumRow, 0, QTableWidgetItem(value['artist']))
        self.albums_tablewidget.setItem(
            albumRow, 1, QTableWidgetItem(value['title']))
        self.albums_tablewidget.setItem(
            albumRow, 2, QTableWidgetItem(value['type']))
        self.albums_tablewidget.setItem(
            albumRow, 3, QTableWidgetItem(str(value['id'])))
        self.albums_tablewidget.setItem(
            albumRow, 4, QTableWidgetItem(str(value['owner_id'])))
        self.albums_tablewidget.setItem(
            albumRow, 5, QTableWidgetItem(value['access_hash']))
            
    def download_button_click(self):
        row = self.albums_tablewidget.currentRow()
        artist = self.albums_tablewidget.item(row, 0).text().strip()
        title = self.albums_tablewidget.item(row, 1).text().strip()
        
        result = find_album_by_artist(artist, title)
                
        if result:
            self.album_form = AlbumForm(
                artist=result[0],
                title=result[1],
                album_id=int(self.albums_tablewidget.item(row, 3).text()),
                owner_id=int(self.albums_tablewidget.item(row, 4).text()),
                access_hash=self.albums_tablewidget.item(row, 5).text()
            )
            
            self.album_form.finished.connect(self.selected_album_handler)
            self.album_form.show()
        else:
            print_message("Информация для данного альбома не найдена")

    @pyqtSlot(VkAlbum)
    def selected_album_handler(self, value):
        self.vk_downloader = VkDownloader(value)

        self.vk_downloader.started.connect(self.download_started)
        self.vk_downloader.finished.connect(self.download_finished)
        self.vk_downloader.start()
    
    @pyqtSlot()
    def download_started(self):
        self.download_button.setEnabled(False)
        print_message("Загрузка альбома началась!")

    @pyqtSlot()
    def download_finished(self):
        self.download_button.setEnabled(True)
        print_message("Загрузка альбома завершилась!")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
