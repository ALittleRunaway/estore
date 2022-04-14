from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from estore.config.config import initConfig
from estore.infrastructure.db.new_db import new_db
from estore.entrypoint.auth import auth_entrypoint


if __name__ == '__main__':
    app = QApplication([])
    cfg = initConfig()
    db_conn = new_db(cfg.db)
    auth_entrypoint(app, db_conn=db_conn)
    print("The app has started")
    app.exec()
