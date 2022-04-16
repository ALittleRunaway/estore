from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QPushButton, QFormLayout, QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QApplication, \
    QMainWindow, QComboBox, QLineEdit, QStackedLayout, QLabel, QToolBar, QStatusBar, QCheckBox, QSpinBox


class OrderWindow(QMainWindow):
    def __init__(self, parent=None):
        super(OrderWindow, self).__init__(parent)

        self.setFixedSize(370, 550)
        self.setWindowTitle("Заказ")

        self.scrollLayout = QFormLayout()

        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        self.buttom_layout = QVBoxLayout()
        self.main_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        self.buttom_layout.addLayout(self.main_layout)
        self.buttom_layout.addLayout(self.stacklayout)

        self.main_layout.addWidget(self.scrollArea)

        self.button_order = QPushButton("Заказать")
        self.button_decline_order = QPushButton("Отменить заказ")
        self.toggle_pickup_point = QComboBox()
        self.label_pickup_point = QLabel("Пункт выдачи:")
        self.button_pdf = QPushButton("Сформировать талон")

        self.label_sum = QLabel("Общая сумма:")
        self.label_fio = QLabel("ФИО:")
        self.label_discount = QLabel("Общая скидка:")
        self.label_order_no = QLabel("Номер заказа:")
        self.label_order_no_actual = QLabel("")
        self.label_order_no_actual.setStyleSheet("font-weight: bold; font-size: 27px")

        self.buttom_layout.addWidget(self.label_fio)
        self.buttom_layout.addWidget(self.label_sum)
        self.buttom_layout.addWidget(self.label_discount)
        self.buttom_layout.addWidget(self.label_order_no)
        self.buttom_layout.addWidget(self.label_order_no_actual)
        self.buttom_layout.addWidget(self.label_pickup_point)
        self.buttom_layout.addWidget(self.toggle_pickup_point)
        self.buttom_layout.addWidget(self.button_pdf)
        self.buttom_layout.addWidget(self.button_order)
        self.buttom_layout.addWidget(self.button_decline_order)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.buttom_layout)
        self.centralWidget.setLayout(self.main_layout)

        self.setCentralWidget(self.centralWidget)
