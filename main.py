#!/usr/bin/env python3
import time
import sys

from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

from auth import Auth


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = uic.loadUiType('forms/main.ui')[0]()
        self.ui.setupUi(self)
        self.check_auth()
        
        self.ui.load_btn.clicked.connect(self.load_btn_click)

    def check_auth(self):
        if not Path(Path.home() / '.vkmusicload.conf').exists():
            self.auth = Auth()
            self.auth.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.auth.show()
        else:
            print('auth ok')
        


    def load_btn_click(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()

    sys.exit(app.exec())