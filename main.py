#!/usr/bin/env python3
import sys
import json

from pathlib import Path
from vk_api.audio import VkAudio
from vk_api.exceptions import AuthError
from vk_api.vk_api import VkApi

from PyQt5 import uic
from PyQt5.QtCore import QObject, Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHeaderView, QMainWindow, QTableWidgetItem


from auth import Auth


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = uic.loadUiType('forms/main.ui')[0]()
        self.ui.setupUi(self)

        self.configure_table()
        
        if not Path(Path.home() / '.vkmusicload.conf').exists():
            self.auth = Auth()
            self.auth.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.auth.com.authorized_successfull.connect(self.fill_album_tbl)
            self.auth.show()
        else:
            self.fill_album_tbl()
        
        self.ui.load_btn.clicked.connect(self.load_btn_click)
    
    def configure_table(self):
        self.ui.album_lst.setHorizontalHeaderLabels(
            [
                "Автор", "Название альбома", "album_id", "owner_id", "access_hash"
            ]
        )

        self.ui.album_lst.setColumnHidden(2, True)
        self.ui.album_lst.setColumnHidden(3, True)
        self.ui.album_lst.setColumnHidden(4, True)
        

        self.ui.album_lst.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.ui.album_lst.cellClicked.connect(self.get_current_guid)
    
    def fill_album_tbl(self):
        with open(Path.home() / '.vkmusicload.conf', "r") as read_file:
            data = json.load(read_file)
        
        vk_session = VkApi(
            login=data['login'],
            password=['password']
        )

        try:
            vk_session.auth(token_only=True)
        except AuthError as error_msg:
            print(error_msg)
            
        vkaudio = VkAudio(vk_session)

        self.ui.album_lst.setRowCount(0)

        for album in vkaudio.get_albums_iter():
            groupRow = self.ui.album_lst.rowCount()
            self.ui.album_lst.insertRow(groupRow)

            self.ui.album_lst.setItem(groupRow, 0, QTableWidgetItem(album['author']))
            self.ui.album_lst.setItem(groupRow, 1, QTableWidgetItem(album['title']))
            self.ui.album_lst.setItem(groupRow, 2, QTableWidgetItem(album['id']))
            self.ui.album_lst.setItem(groupRow, 3, QTableWidgetItem(album['owner_id']))
            self.ui.album_lst.setItem(groupRow, 4, QTableWidgetItem(album['access_hash']))
        
    def load_btn_click(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()

    sys.exit(app.exec())