from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QPushButton, QFormLayout, QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QApplication, \
    QMainWindow, QComboBox, QLineEdit, QStackedLayout, QLabel, QToolBar, QStatusBar, QCheckBox


# from estore.config.config import current_user

class CatalogWindow(QMainWindow):
    def __init__(self, parent=None):
        super(CatalogWindow, self).__init__(parent)

        self.setFixedSize(600, 500)
        self.setWindowTitle("Каталог")

        self.toolbar = QToolBar("My main toolbar")
        self.addToolBar(self.toolbar)

        self.fio_button = QAction("Гость", self)
        self.fio_button.setStatusTip("Это вы")
        self.toolbar.addAction(self.fio_button)

        self.toolbar.addSeparator()

        self.sign_out_button = QAction("Выйти", self)
        self.sign_out_button.setStatusTip("Вы уверены, что хотите выйти?")

        self.sign_out_button.setCheckable(True)
        self.toolbar.addAction(self.sign_out_button)

        self.setStatusBar(QStatusBar(self))


        # sorting
        self.toggle_sort = QComboBox()
        self.label_sort = QLabel("Сортировка:")
        self.toggle_sort.addItems(["Все диапазоны", "0-9.99%", "10-14.99%", ">15%"])

        # filtering
        self.toggle_filter = QComboBox()
        self.label_filter = QLabel("Фильтр:")
        self.toggle_filter.addItems(["Нет", "по возрастанию цены", "По убыванию цены"])

        # search
        self.search_input = QLineEdit()
        self.label_search = QLabel("Поиск:")
        self.label_amount = QLabel("")
        self.search_input.setPlaceholderText("Введите что-нибудь")

        self.scrollLayout = QFormLayout()

        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        self.main_layout = QVBoxLayout()
        self.head_layout = QHBoxLayout()
        self.head_layout2 = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        self.main_layout.addLayout(self.head_layout)
        self.main_layout.addLayout(self.head_layout2)
        self.main_layout.addLayout(self.stacklayout)

        self.head_layout.addWidget(self.label_sort)
        self.head_layout.addWidget(self.toggle_sort)
        self.head_layout.addWidget(self.label_filter)
        self.head_layout.addWidget(self.toggle_filter)
        self.head_layout2.addWidget(self.label_search)
        self.head_layout2.addWidget(self.search_input)
        self.head_layout2.addWidget(self.label_amount)

        self.main_layout.addWidget(self.scrollArea)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.head_layout)
        self.centralWidget.setLayout(self.main_layout)

        self.setCentralWidget(self.centralWidget)
