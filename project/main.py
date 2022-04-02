from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget

from forms.auth import AuthWindow
from utils import print_message


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("designs/main.ui", self)

        self.search_button.clicked.connect(self.search_button_click)

        self.check_authorization()

    def check_authorization(self):
        """ Заполнить строку документации """
        if not (Path.home() / '.vkmusicload.conf').exists():
            self.auth_window = AuthWindow()
            self.auth_window.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.auth_window.show()

    def search_button_click(self):
        search_text = self.search_lineedit.text()
        
        if search_text and not search_text.isspace():
            pass
        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
