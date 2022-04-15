from PyQt6.QtWidgets import QPushButton, QFormLayout, QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QApplication, QMainWindow

# from estore.config.config import current_user

class CatalogWindow(QMainWindow):
    def __init__(self, parent=None):
        super(CatalogWindow, self).__init__(parent)

        self.setFixedSize(600, 500)

        # main button
        self.addButton = QPushButton('button to add other widgets')
        self.addButton.clicked.connect(self.addWidget)

        # scroll area widget contents - layout
        self.scrollLayout = QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        # main layout
        self.mainLayout = QVBoxLayout()

        # add all main to the main vLayout
        self.mainLayout.addWidget(self.addButton)
        self.mainLayout.addWidget(self.scrollArea)

        # central widget
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)

    def addWidget(self):
        self.scrollLayout.addRow(Test())


class Test(QWidget):
    def __init__(self, parent=None):
        super(Test, self).__init__(parent)

        # self.pushButton = QPushButton(current_user.name)

        layout = QHBoxLayout()
        layout.addWidget(self.pushButton)
        self.setLayout(layout)

