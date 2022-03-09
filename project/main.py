from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget

from forms.auth import AuthWindow


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("designs/main.ui", self)
        self.check_authorization()

    def check_authorization(self):
        """ Заполнить строку документации """
        if not (Path.home() / '.vkmusicload.conf').exists():
            self.auth_window = AuthWindow()
            self.auth_window.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.auth_window.authorized_successfull.connect(self.create_session)
            self.auth_window.show()
        else:
            self.create_session()

    def create_session(self):
        print("session created")



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
