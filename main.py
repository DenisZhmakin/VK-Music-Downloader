#!/usr/bin/env python3
import sys
import json

from pathlib import Path
from vk_api.audio import VkAudio
from vk_api.exceptions import AuthError
from vk_api.vk_api import VkApi

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHeaderView, QMainWindow, QTableWidgetItem


from auth import Auth
from entities.vk_album import VkAlbum
from entities.vk_session import VkSession
from vkdownloader import download_album


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = uic.loadUiType('designs/main.ui')[0]()
        self.ui.setupUi(self)

        self.vkalbum = None

        self.configure_table()
        
        if not Path(Path.home() / '.vkmusicload.conf').exists():
            self.auth = Auth()
            self.auth.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.auth.com.authorized_successfull.connect(self.fill_album_tbl)
            self.auth.show()
        else:
            with open(Path.home() / '.vkmusicload.conf', "r") as read_file:
                data = json.load(read_file)
            
            VkSession().set_session(data['login'], password=['password'])
            self.fill_album_tbl()
        
        self.ui.load_btn.clicked.connect(self.load_btn_click)
    
    def configure_table(self):
        self.ui.album_lst.setHorizontalHeaderLabels(
            [
                "Исполнитель", "Название альбома", "album_id", "owner_id", "access_hash"
            ]
        )

        self.ui.album_lst.setColumnHidden(2, True)
        self.ui.album_lst.setColumnHidden(3, True)
        self.ui.album_lst.setColumnHidden(4, True)
        
        self.ui.album_lst.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.album_lst.cellClicked.connect(self.get_current_element)

    def get_current_element(self, row):
        self.vkalbum = VkAlbum(
            artist=self.ui.album_lst.item(row, 0).text().strip(),
            title=self.ui.album_lst.item(row, 1).text().strip(),
            album_id=int(self.ui.album_lst.item(row, 2).text()),
            owner_id=int(self.ui.album_lst.item(row, 3).text()),
            access_hash=self.ui.album_lst.item(row, 4).text()
        )
        
    def fill_album_tbl(self):
        vkaudio = VkAudio(VkSession().get_session())

        self.ui.album_lst.setRowCount(0)

        for album in vkaudio.get_albums_iter():
            albumRow = self.ui.album_lst.rowCount()
            self.ui.album_lst.insertRow(albumRow)

            self.ui.album_lst.setItem(albumRow, 0, QTableWidgetItem(album['author']))
            self.ui.album_lst.setItem(albumRow, 1, QTableWidgetItem(album['title']))
            self.ui.album_lst.setItem(albumRow, 2, QTableWidgetItem(str(album['id'])))
            self.ui.album_lst.setItem(albumRow, 3, QTableWidgetItem(str(album['owner_id'])))
            self.ui.album_lst.setItem(albumRow, 4, QTableWidgetItem(album['access_hash']))
        
    def load_btn_click(self):
        if self.vkalbum is not None:
            download_album(self.vkalbum)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()

    sys.exit(app.exec())
    