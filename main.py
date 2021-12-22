#!/usr/bin/env python3
import json
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QApplication, QHeaderView, QTableWidgetItem, QWidget
from vk_api.audio import VkAudio
from utils import print_message

from entities.album import VkAlbum
from entities.session import VkSession
from forms.album_form import AlbumForm
from forms.auth_form import AuthForm

from downloader import VkDownloader


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("designs/main.ui", self)

        self.selected_album: dict = None

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

        self.album_table.cellClicked.connect(self.get_current_album)

        self.album_table.setColumnHidden(2, True)
        self.album_table.setColumnHidden(3, True)
        self.album_table.setColumnHidden(4, True)

        self.album_table.horizontalHeader()\
            .setSectionResizeMode(QHeaderView.Stretch)

    def get_current_album(self, row):
        self.selected_album = {
            'artist': self.album_table.item(row, 0).text().strip(),
            'title': self.album_table.item(row, 1).text().strip(),
            'album_id': int(self.album_table.item(row, 2).text()),
            'owner_id': int(self.album_table.item(row, 3).text()),

            'access_hash': self.album_table.item(row, 4).text()
        }

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
        if self.selected_album is not None:
            self.album_form = AlbumForm(self.selected_album)
            self.album_form.finished.connect(self.selected_album_handler)
            self.album_form.show()

    @pyqtSlot(dict)
    def selected_album_handler(self, value):
        self.vk_downloader = VkDownloader(
            VkAlbum(
                    artist=value['artist'],
                    title=value['title'],
                    cover=value['cover'],
                    genre=value['genre'],
                    year=value['year'],
                    album_id=value['album_id'],
                    owner_id=value['owner_id'],
                    access_hash=value['access_hash']
                )
            )

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
