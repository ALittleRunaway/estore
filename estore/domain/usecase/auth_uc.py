import random

from estore.gateway.user_gw import UserGateway
from PyQt6.QtWidgets import QMessageBox
from PyQt6 import QtTest


class AuthUseCase():
    def __init__(self, gw: UserGateway, auth_window, captcha_window, catalog_window, manage_window):
        self.gw = gw
        self.auth_window = auth_window
        self.captcha_window = captcha_window
        self.catalog_window = catalog_window
        self.manage_window = manage_window
        self.captcha_number = None
        self.one_fail_left = True

        self.auth_window.button_login.clicked.connect(self.authorise)
        self.auth_window.button_see_as_guest.clicked.connect(self.authorise_as_guest)
        self.captcha_window.button_submit.clicked.connect(self.verify_capctha)
        self.captcha_window.button_new_captcha.clicked.connect(self.generate_captcha)

    def verify_capctha(self):
        if self.captcha_window.captcha_input.text() == self.captcha_number:
            self.captcha_window.hide()
            self.auth_window.show()
            self.auth_window.setDisabled(False)
            self.captcha_window.captcha_input.clear()
        else:
            QMessageBox.about(self.captcha_window, "Title", "Неверно. Приложение заблокировано на 10 сек")
            self.captcha_window.setDisabled(True)
            QtTest.QTest.qWait(10000)
            self.captcha_window.setDisabled(False)
            self.captcha_window.captcha_input.clear()

    def generate_captcha(self):
        letters, digits = "abcdefghijklmnopqrstuvwxyz", "0123456789"
        whole_string = letters + letters.upper() + digits
        self.captcha_number = "".join([random.choice(whole_string) for i in range(4)])
        self.captcha_window.captcha_label.setText(self.captcha_number)

    def authorise(self):
        # Successfull authorisation
        if (user := self.gw.authorise(self.auth_window.input_login.text(), self.auth_window.input_password.text())) is not None:
            self.catalog_window.fio_button.setText(f"{user.surname} {user.name} {user.patronymic}")
            if user.role_id == 3 or user.role_id == 4:
                self.catalog_window.manage_button.setVisible(True)
                self.catalog_window.manage_button.setText("Управление заказами")
                self.catalog_window.manage_button.setStatusTip("Функционал для менеджеров и администраторов")
            self.captcha_window.user = user
            self.captcha_window.hide()
            self.auth_window.hide()
            self.catalog_window.show()
        else:
            if self.one_fail_left:
                QMessageBox.about(self.auth_window, "Title", "Неверный логин или пароль. Попробуйте снова")
                self.one_fail_left = False
            else:
                self.one_fail_left = True
                self.generate_captcha()
                self.captcha_window.show()
                self.auth_window.setDisabled(True)

    def authorise_as_guest(self):
        global current_user
        current_user = 'guest'
        self.captcha_window.hide()
        self.auth_window.hide()
        self.catalog_window.show()

