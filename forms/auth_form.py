import json

from pathlib import Path
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from vk_api.vk_api import VkApi

from utils import print_message, validate_QLineEdit


class AuthForm(QWidget):
    authorized_successfull = pyqtSignal() 
    
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("designs/auth.ui", self)

        self.auth_button.clicked.connect(self.auth_button_click)
    
    def auth_button_click(self):
        """ ЗАПОЛНИТЬ КОММЕНТ """

        if not validate_QLineEdit(self.login_line):
            print_message("Поле логина пустое. Заполните его")
            return

        if not validate_QLineEdit(self.password_line):
            print_message("Поле пароля пустое. Заполните его")
            return

        session = VkApi(self.login_line.text(), self.password_line.text())

        try:
            session.auth(token_only=True)
            auth_ok = True
        except:
            auth_ok = False

        if auth_ok:
            user_data = {
                "login": self.login_line.text(),
                "password": self.password_line.text()
            }
            
            with open(Path.home() / '.vkmusicload.conf', "w") as write_file:
                json.dump(user_data, write_file)
            
            self.authorized_successfull.emit()
            self.close()
        else:
            self.login_line.clear()
            self.password_line.clear()
            
            print_message(
                "Авторизация не удалась.\nВозможно, не правильный логин или пароль."
                )