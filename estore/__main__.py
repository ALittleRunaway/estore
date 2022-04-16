import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from estore.config.config import initConfig
from estore.domain.usecase.auth_uc import AuthUseCase
from estore.domain.usecase.catalog_uc import CatalogUseCase
from estore.domain.usecase.manage_uc import ManageUseCase
from estore.domain.usecase.order_uc import OrderUseCase
from estore.gateway.manage_gw import ManageGateway
from estore.gateway.order_gw import OrderGateway
from estore.gateway.user_gw import UserGateway
from estore.gateway.product_gw import ProductGateway
from estore.gui.auth_window import AuthWindow
from estore.gui.captcha_window import CaptchaWindow
from estore.gui.catalog_window import CatalogWindow
from estore.gui.manage_window import ManageWindow
from estore.gui.order_window import OrderWindow
from estore.infrastructure.db.new_db import new_db


if __name__ == '__main__':
    app = QApplication([])
    cfg = initConfig()
    db_conn = new_db(cfg.db)
    dir_path = os.path.dirname(os.path.realpath(__file__))

    auth_window = AuthWindow()
    captcha_window = CaptchaWindow()
    catalog_window = CatalogWindow()
    order_window = OrderWindow()
    manage_window = ManageWindow()

    user_gw = UserGateway(db_conn=db_conn)
    product_gw = ProductGateway(db_conn=db_conn)
    order_gw = OrderGateway(db_conn=db_conn)
    manage_gw = ManageGateway(db_conn=db_conn)

    auth_uc = AuthUseCase(user_gw, auth_window, captcha_window, catalog_window, manage_window)
    catalog_uc = CatalogUseCase(product_gw, order_gw, catalog_window, auth_window, order_window, manage_window, dir_path)
    order_uc = OrderUseCase(order_gw, order_window, catalog_window, auth_window, dir_path)
    manage_uc = ManageUseCase(manage_gw, manage_window)

    auth_window.show()
    captcha_window.hide()
    catalog_window.hide()
    order_window.hide()
    manage_window.show()

    print("The app has started")
    app.exec()
