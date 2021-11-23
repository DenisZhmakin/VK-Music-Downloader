import json
from pathlib import Path
from typing import Optional
import vk_api

import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox


class Auth(QMainWindow):
    def __init__(self):
        super(Auth, self).__init__()

        self.ui = uic.loadUiType('forms/auth.ui')[0]()
        self.ui.setupUi(self)

        self.ui.auth_btn.clicked.connect(self.auth_btn_click)

    def auth_btn_click(self):
        """ ЗАПОЛНИТЬ КОММЕНТ """

        login = self.validate_string(self.ui.login_line.text())

        if login is None:
            self.ui.login_line.clear()

            msgBox = QMessageBox()

            msgBox.setWindowTitle("Сообщение о ошибке")
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Поле логина пустое. Заполните его")

            msgBox.exec()
            return

        password = self.validate_string(self.ui.password_line.text()) 

        if password is None:
            self.ui.password_line.clear()

            msgBox = QMessageBox()

            msgBox.setWindowTitle("Сообщение о ошибке")
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Поле пароля пустое. Заполните его")

            msgBox.exec()
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
            
            self.close()
        except vk_api.AuthError as error_msg:
            msgBox = QMessageBox()

            msgBox.setWindowTitle("Сообщение о ошибке")
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Авторизация не удалась. Возможно, не правильный логи или пароль.")

            msgBox.exec()
            return
            
    def validate_string(self, input_str: str) -> Optional[str]:
        return input_str.strip() if input_str and not input_str.isspace() else None