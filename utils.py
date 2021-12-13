import random
import string
from PyQt5.QtWidgets import QLineEdit, QMessageBox


def validate_QLineEdit(field: QLineEdit):
    input_str = field.text()

    if input_str and not input_str.isspace():
        field.setText(input_str.strip())
        return True
    else:
        field.clear()
        return False

def print_message(message):
    msgBox = QMessageBox()

    msgBox.setWindowTitle("Сообщение о ошибке")
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(message)
    
    msgBox.exec()

def generate_track_code():
    return f"{''.join(random.choice(string.ascii_lowercase) for i in range(25))}"