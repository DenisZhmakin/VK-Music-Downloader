#!/usr/bin/env python3
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (QApplication, QHeaderView, QTableWidgetItem,
                             QWidget)
from vk_api.audio import VkAudio

from downloader import VkDownloader
from entities.album import VkAlbum
from entities.session import VkSession
from forms.album_form import AlbumForm
from forms.auth_form import AuthForm
from utils import find_album_by_artist, print_message


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("designs/main.ui", self)

        self._album_info: dict = None

        self.download_button.clicked.connect(self.download_button_click)
        self.configure_table()

        if not Path(Path.home() / '.vkmusicload.conf').exists():
            self.auth = AuthForm()
            self.auth.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.auth.authorized_successfull.connect(self.fill_album_table)
            self.auth.show()
        else:
            self.fill_album_table()

    def configure_table(self):
        self.album_table.setHorizontalHeaderLabels(
            [
                "Исполнитель",
                "Название альбома",
                "album_id",
                "owner_id",
                "access_hash"
            ]
        )

        self.album_table.setColumnHidden(2, True)
        self.album_table.setColumnHidden(3, True)
        self.album_table.setColumnHidden(4, True)

        self.album_table.horizontalHeader()\
            .setSectionResizeMode(QHeaderView.Stretch)

    def fill_album_table(self):
        vkaudio = VkAudio(VkSession().get_session())

        self.album_table.setRowCount(0)

        for album in vkaudio.get_albums_iter():
            albumRow = self.album_table.rowCount()
            self.album_table.insertRow(albumRow)

            self.album_table.setItem(
                albumRow, 0, QTableWidgetItem(album['artist']))
            self.album_table.setItem(
                albumRow, 1, QTableWidgetItem(album['title']))
            self.album_table.setItem(
                albumRow, 2, QTableWidgetItem(str(album['id'])))
            self.album_table.setItem(
                albumRow, 3, QTableWidgetItem(str(album['owner_id'])))
            self.album_table.setItem(
                albumRow, 4, QTableWidgetItem(album['access_hash']))

    def download_button_click(self):
        row = self.album_table.currentRow()
        artist = self.album_table.item(row, 0).text().strip()
        title = self.album_table.item(row, 1).text().strip()
        
        result = find_album_by_artist(artist, title)
                
        if result:
            self.album_form = AlbumForm(
                artist=result[0],
                title=result[1],
                album_id=int(self.album_table.item(row, 2).text()),
                owner_id=int(self.album_table.item(row, 3).text()),
                access_hash=self.album_table.item(row, 4).text()
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
