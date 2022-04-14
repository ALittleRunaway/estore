import sys

from estore.gateway.user_gw import UserGateway
from estore.domain.usecase.auth_uc import AuthUseCase
from estore.gui.auth_window import AuthWindow


def auth_entrypoint(app, db_conn):
    auth_window = AuthWindow()
    user_gw = UserGateway(db_conn=db_conn)
    auth_uc = AuthUseCase(gw=user_gw, window=auth_window)
    auth_window.show()
    sys.exit(app.exec())

