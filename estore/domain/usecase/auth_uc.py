
from estore.gateway.user_gw import UserGateway
from PyQt6.QtWidgets import QMessageBox


class AuthUseCase():
    def __init__(self, gw: UserGateway, window):
        self.gw = gw
        self.window = window
        print(self.window.button_login)
        # self.window.button_login.clicked.connect(a)

        self.window.button_login.clicked.connect(self.authorise)
        # self.window.button_see_as_guest.clicked.connect(hello())

    def authorise(self):

        if self.gw.authorise(self.window.input_login.text(), self.window.input_password.text()) is not None:
            QMessageBox.about(self.window, "Title", "Ok")
        else:
            QMessageBox.about(self.window, "Capcha", "Not ok")
