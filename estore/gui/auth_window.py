from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QMessageBox)
from estore.domain.entity.user import User



class AuthWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Estore")

        self.label_login = QLabel("Логин")
        self.label_password = QLabel("Пароль")
        self.input_login = QLineEdit()
        self.input_password = QLineEdit()
        self.button_login = QPushButton("Войти!")
        self.button_see_as_guest = QPushButton("Зайти как гость")

        layout = QVBoxLayout()
        layout.addWidget(self.label_login)
        layout.addWidget(self.input_login)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.button_login)
        layout.addWidget(self.button_see_as_guest)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
