from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


class Mainwindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My app")


if __name__ == '__main__':
    app = QApplication([])
    window = Mainwindow()
    window.show()
    app.exec()
