import json

from pathlib import Path
from typing import Optional
from PyQt5 import uic
from vk_api.vk_api import VkApi
from vk_session import VkSession
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QWidget


class AuthForm(QWidget):
    authorized_successfull = pyqtSignal() 
    
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("designs/auth.ui", self)

        self.auth_button.clicked.connect(self.auth_button_click)
    
    def auth_button_click(self):
        """ ЗАПОЛНИТЬ КОММЕНТ """

        if not self.validate_field(self.login_line):
            self.print_message("Поле логина пустое. Заполните его")
            return

        if not self.validate_field(self.password_line):
            self.print_message("Поле пароля пустое. Заполните его")
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
            
            self.print_message(
                "Авторизация не удалась.\nВозможно, не правильный логин или пароль."
                )
        
    def validate_field(self, field: QLineEdit):
        input_str = field.text()

        if input_str and not input_str.isspace():
            field.setText(input_str.strip())
            return True
        else:
            field.clear()
            return False

    def print_message(self, message):
        msgBox = QMessageBox()

        msgBox.setWindowTitle("Сообщение о ошибке")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(message)
        
        msgBox.exec()

        