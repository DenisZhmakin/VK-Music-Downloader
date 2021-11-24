import json
from pathlib import Path
from typing import Optional
from PyQt5.QtCore import QObject, pyqtSignal
import vk_api

import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox


class Communicate(QObject):                                                 
    authorized_successfull = pyqtSignal()   
    

class Auth(QMainWindow):
    def __init__(self):
        super(Auth, self).__init__()

        self.com = Communicate()

        self.ui = uic.loadUiType('forms/auth.ui')[0]()
        self.ui.setupUi(self)

        self.ui.auth_btn.clicked.connect(self.auth_btn_click)

    def auth_btn_click(self):
        """ ЗАПОЛНИТЬ КОММЕНТ """

        login = self.validate_string(self.ui.login_line.text(), "Поле логина пустое. Заполните его")
        password = self.validate_string(self.ui.password_line.text(), "Поле пароля пустое. Заполните его")

        if login is None or password is None:
            self.ui.login_line.clear()
            self.ui.password_line.clear()
            return

        vk_session = vk_api.VkApi(login, password)

        try:
            vk_session.auth(token_only=True)

            user_data = {
                "login": login,
                "password": password
            }
            
            with open(Path.home() / '.vkmusicload.conf', "w") as write_file:
                json.dump(user_data, write_file)
            
            self.com.authorized_successfull.emit()
            self.close()
        except vk_api.AuthError:
            msgBox = QMessageBox()

            msgBox.setWindowTitle("Сообщение о ошибке")
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Авторизация не удалась. Возможно, не правильный логи или пароль.")

            msgBox.exec()
            return
            
    def validate_string(self, input_str: str, message: str) -> Optional[str]:
        if input_str and not input_str.isspace():
            return input_str.strip()

        msgBox = QMessageBox()

        msgBox.setWindowTitle("Сообщение о ошибке")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(message)

        msgBox.exec()
        return
        
