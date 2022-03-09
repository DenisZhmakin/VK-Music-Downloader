import json
from pathlib import Path
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QCheckBox, QWidget
from utils import print_message, validate_QLineEdit
from vk_api.vk_api import AuthError, BadPassword, VkApi

from forms.twoFA import TwoFA


class AuthWindow(QWidget):
    authorized_successfull = pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("designs/auth.ui", self)

        self.auth_button.clicked.connect(self.auth_button_click)
        self.tFA_checkbox: QCheckBox = self.tFA_checkbox

    def auth_button_click(self):
        if not validate_QLineEdit(self.login_line):
            print_message("Поле логина пустое. Заполните его")
            return
        
        if not validate_QLineEdit(self.password_line):
            print_message("Поле пароля пустое. Заполните его")
            return

        if self.tFA_checkbox.isChecked():
            self.two_fa_window = TwoFA()
            self.two_fa_window.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.two_fa_window.code_received.connect(self.authentication_with_twoFA)
            self.two_fa_window.show()
        else:
            self.simple_authentication()
                
    def simple_authentication(self):
        session = VkApi(self.login_line.text(), self.password_line.text())

        try:
            session.auth(token_only=True)
            self.save_auth_data()
            self.authorized_successfull.emit()
            self.close()
        except BadPassword:
            print_message("Некорректный пароль. Введите правильный")
            self.password_line.clear()
        except AuthError:
            print_message("Требуется двухфакторная аутентификация")

    @pyqtSlot(str)
    def authentication_with_twoFA(self, value):
        session = VkApi(
            self.login_line.text(), self.password_line.text(),
            auth_handler=lambda: (value, True)
        )

        try:
            session.auth(token_only=True)
            self.save_auth_data()
            self.authorized_successfull.emit()
            self.close()
        except BadPassword:
            print_message("Некорректный пароль. Введите правильный")
            self.password_line.clear()
        except AuthError:
            print_message("Код двухфакторной аутентификации не корректен.")

    def save_auth_data(self):
        user_data = {
            "login": self.login_line.text(),
            "password": self.password_line.text()
        }

        with open(Path.home() / '.vkmusicload.conf', "w") as write_file:
            json.dump(user_data, write_file)