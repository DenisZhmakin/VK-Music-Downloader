from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIntValidator


class TwoFA(QWidget):
    code_received = pyqtSignal(str)

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("designs/twoFA.ui", self)

        self.ok_button.clicked.connect(self.ok_button_click)
        self.code_lineedit.setValidator(
            QIntValidator(100000, 999999, self)
        )

    def ok_button_click(self):
        auth_code = self.code_lineedit.text()

        if len(auth_code) == 6:
            self.code_received.emit(auth_code)
            self.close()
        else:
            pass
