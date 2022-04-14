# import sys
#
# from estore.gateway.user_gw import UserGateway
# from estore.domain.usecase.auth_uc import AuthUseCase
# from estore.gui.auth_window import AuthWindow
# from estore.gui.captcha_window import CaptchaWindow
#
#
# def auth_entrypoint(app, db_conn):
#     auth_window = AuthWindow()
#     captcha_window = CaptchaWindow()
#     user_gw = UserGateway(db_conn=db_conn)
#     auth_uc = AuthUseCase(gw=user_gw, auth_window=auth_window, captcha_window=captcha_window)
#     auth_window.show()
#     captcha_window.hide()
#     sys.exit(app.exec())
#
