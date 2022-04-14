import random

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QMessageBox, QGridLayout)
from estore.domain.entity.user import User



class CaptchaWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Captha")
        self.label = QLabel("Введите капчу:")
        self.setFixedSize(QSize(250, 200))

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.captcha_label = QLabel()
        font = QFont("{}".format('Brush Script MT'), 72)
        font.setStrikeOut(True)
        self.captcha_label.setFont(font)

        self.captcha_input = QLineEdit()
        self.captcha_input.clear()

        self.button_submit = QPushButton("Подтвердить")
        self.button_new_captcha = QPushButton("Новая капча")

        grid = QGridLayout(centralWidget)
        grid.addWidget(self.label)
        grid.addWidget(self.captcha_label)
        grid.addWidget(self.captcha_input)
        grid.addWidget(self.button_submit)
        grid.addWidget(self.button_new_captcha)
