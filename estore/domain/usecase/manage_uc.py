import random

from PyQt6.QtWidgets import QMessageBox, QButtonGroup, QGroupBox, QLabel, QPushButton, QVBoxLayout
from PyQt6 import QtTest

from estore.gateway.manage_gw import ManageGateway


class ManageUseCase():
    def __init__(self, gw: ManageGateway, manage_window):
        self.gw = gw
        self.manage_window = manage_window

        self.manage_window.toggle_filter.currentIndexChanged.connect(self.fill_orders)
        self.manage_window.toggle_sort.currentIndexChanged.connect(self.fill_orders)

        self.buttons_orders = {}

        self.fill_orders()

    def fill_orders(self):
        for i in reversed(range(self.manage_window.scrollLayout.count())):
            self.manage_window.scrollLayout.itemAt(i).widget().setParent(None)

        filter = str(self.manage_window.toggle_filter.currentText())
        sort = str(self.manage_window.toggle_sort.currentText())

        self.btn_grp = QButtonGroup()
        self.btn_grp.setExclusive(True)
        i = 0

        for order in (orders := self.gw.get_orders(filter=filter, sort=sort)):
        # for order in (orders := self.gw.get_orders()):
            groupBox = QGroupBox()

            label_no = QLabel(f"Заказ № {order.id}")
            label_status = QLabel(f"Статус: {order.status}")
            label_client = QLabel(f"Заказчик: {order.client_name}")
            label_sum = QLabel(f"Общая сумма заказа: {float(order.sum)} ₽")
            label_discount = QLabel(f"Общая скидка заказа: {order.discount} %")
            label_order_date = QLabel(f"Дата заказа: {order.order_date.strftime('%d/%M/%Y')}")
            label_delivery_date = QLabel(f"Дата доставки: {order.delivery_date.strftime('%d/%M/%Y')}")
            products_string = "Состав: \n" + "\n".join([f" + {product.name}; цена: {product.price} ₽; скидка: {product.discount} %" for product in order.products])
            label_products = QLabel(products_string)

            button_order = QPushButton("Добавить в корзину")
            button_order.setStatusTip(str(i))
            self.buttons_orders[str(i)] = order
            i += 1
            self.btn_grp.addButton(button_order)

            vbox = QVBoxLayout()
            vbox.maximumSize()
            vbox.addWidget(label_no)
            vbox.addWidget(label_status)
            vbox.addWidget(label_client)
            vbox.addWidget(label_sum)
            vbox.addWidget(label_discount)
            vbox.addWidget(label_order_date)
            vbox.addWidget(label_delivery_date)
            vbox.addWidget(label_products)
            vbox.addWidget(button_order)
            vbox.addStretch(1)
            groupBox.setLayout(vbox)

            if order.discount > 15:
                groupBox.setStyleSheet("background-color: #7fff00")

            self.manage_window.scrollLayout.addRow(groupBox)

        self.btn_grp.buttonClicked.connect(self.a)

    def a(self, btn):
        order_to_edit = self.buttons_orders[btn.statusTip()]
        # order_to_edit.amount_selected = 1
        # self.order_products.append(order_to_edit)
        # self.fill_order_products()
        # self.order_window.show()
