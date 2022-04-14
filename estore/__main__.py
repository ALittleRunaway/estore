from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from estore.config.config import initConfig
from estore.domain.usecase.auth_uc import AuthUseCase
from estore.gateway.user_gw import UserGateway
from estore.gui.auth_window import AuthWindow
from estore.gui.captcha_window import CaptchaWindow
from estore.gui.catalog_window import CatalogWindow
from estore.infrastructure.db.new_db import new_db


if __name__ == '__main__':
    app = QApplication([])
    cfg = initConfig()
    db_conn = new_db(cfg.db)

    auth_window = AuthWindow()
    captcha_window = CaptchaWindow()
    catalog_window = CatalogWindow()

    user_gw = UserGateway(db_conn=db_conn)
    auth_uc = AuthUseCase(user_gw, auth_window, captcha_window, catalog_window)

    auth_window.show()
    captcha_window.hide()
    catalog_window.hide()

    print("The app has started")
    app.exec()
