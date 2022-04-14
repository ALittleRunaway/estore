
from estore.gateway.user_gw import UserGateway
from PyQt6.QtWidgets import QMessageBox

class AuthUseCase():
    def __init__(self, gw: UserGateway, window):
        self.gw = gw
        self.window = window

        # self.window.button_login.clicked.connect(self.authorise("self.window.input_login", "self.window.input_password"))
        # self.window.button_see_as_guest.clicked.connect(hello())

    def authorise(self, login, password):

        if self.gw.authorise(login, password) is not None:
            QMessageBox.about(self.window, "Title", "Ok")
        else:
            QMessageBox.about(self.window, "Capcha", "Ok")
