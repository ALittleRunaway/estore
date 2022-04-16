import random
from datetime import datetime

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMessageBox, QButtonGroup, QGroupBox, QLabel, QPushButton, QVBoxLayout, QComboBox, \
    QCalendarWidget, QLineEdit
from PyQt6 import QtTest

from estore.gateway.manage_gw import ManageGateway


class ManageUseCase():
    def __init__(self, gw: ManageGateway, manage_window):
        self.gw = gw
        self.manage_window = manage_window

        self.manage_window.toggle_filter.currentIndexChanged.connect(self.fill_orders)
        self.manage_window.toggle_sort.currentIndexChanged.connect(self.fill_orders)

        self.buttons_orders = {}
        self.buttons_labels = {}
        self.buttons_edit_lines = {}

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

            # button_edit = QPushButton("Добавить в корзину")
            toggle_status = QComboBox()
            toggle_status.addItems(["Новый", "Завершен"])
            toggle_status.setCurrentText(order.status)
            toggle_status.setStatusTip(str(i))

            date_edit_line = QLineEdit()
            date_edit_line.setPlaceholderText("Введите новую дату доставки в формате dd/mm/yyyy")

            button_edit = QPushButton("Заменить")
            button_edit.setStatusTip(str(i))
            self.buttons_orders[str(i)] = order
            self.buttons_labels[str(i)] = toggle_status
            self.buttons_edit_lines[str(i)] = date_edit_line
            i += 1
            self.btn_grp.addButton(button_edit)

            vbox = QVBoxLayout()
            vbox.maximumSize()
            vbox.addWidget(label_no)

            vbox.addWidget(label_status)
            vbox.addWidget(toggle_status)
            vbox.addWidget(label_client)
            vbox.addWidget(label_sum)
            vbox.addWidget(label_discount)
            vbox.addWidget(label_order_date)
            vbox.addWidget(label_delivery_date)
            vbox.addWidget(date_edit_line)
            vbox.addWidget(label_products)
            vbox.addWidget(button_edit)
            vbox.addStretch(1)
            groupBox.setLayout(vbox)

            for product in order.products:
                if product.amount < 3:
                    groupBox.setStyleSheet("background-color: #20b2aa")
                if product.amount == 0:
                    groupBox.setStyleSheet("background-color: #ff8c00")

            self.manage_window.scrollLayout.addRow(groupBox)

        self.btn_grp.buttonClicked.connect(self.edit)

    def edit(self, btn):
        order_to_edit = self.buttons_orders[btn.statusTip()]
        new_status = self.buttons_labels[btn.statusTip()].currentText()
        self.gw.edit_status(order_to_edit.id, new_status)

        new_date_str = self.buttons_edit_lines[btn.statusTip()].text()
        if new_date_str != "":
            try:
                new_date = datetime.strptime(new_date_str, '%d/%M/%Y')
                self.gw.edit_delivery_date(order_to_edit.id, new_date)
            except:
                QMessageBox.about(self.manage_window, "Title", "Новая дата доставки введдена в неверном формате")
                self.buttons_edit_lines[btn.statusTip()].clear()

        self.fill_orders()
