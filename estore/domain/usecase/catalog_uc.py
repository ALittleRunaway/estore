# coding: utf8
import datetime
import os
import random
import sys

from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import QLabel, QMessageBox, QGroupBox, QRadioButton, QVBoxLayout, QPushButton, QStyle, QButtonGroup
from fpdf import FPDF

from estore.gateway.product_gw import ProductGateway


class CatalogUseCase():
    def __init__(self, product_gw: ProductGateway, order_gw, catalog_window, auth_window, order_window, path):
        self.product_gw = product_gw
        self.order_gw = order_gw
        self.catalog_window = catalog_window
        self.auth_window = auth_window
        self.order_window = order_window
        self.path = path
        self.user = None
        self.order_products = []
        self.buttons_products = {}
        self.pickup_points = {}
        self.order_available = False
        self.sum = 0
        self.discount = 0
        self.fill_products()
        self.get_pickup_points()

        self.catalog_window.search_input.returnPressed.connect(self.fill_products)
        self.catalog_window.search_input.selectionChanged.connect(self.fill_products)
        self.catalog_window.search_input.textChanged.connect(self.fill_products)
        self.catalog_window.search_input.textEdited.connect(self.fill_products)

        self.catalog_window.toggle_filter.currentIndexChanged.connect(self.fill_products)
        self.catalog_window.toggle_sort.currentIndexChanged.connect(self.fill_products)

        self.catalog_window.sign_out_button.triggered.connect(self.sign_out)
        self.order_window.button_pdf.clicked.connect(self.form_pdf)
        self.order_window.button_decline_order.clicked.connect(self.clear_order)
        self.order_window.button_order.clicked.connect(self.new_order)
        self.get_pickup_points()

    def fill_products(self):
        for i in reversed(range(self.catalog_window.scrollLayout.count())):
            self.catalog_window.scrollLayout.itemAt(i).widget().setParent(None)

        filter = str(self.catalog_window.toggle_filter.currentText())
        sort = str(self.catalog_window.toggle_sort.currentText())
        search = self.catalog_window.search_input.text()

        self.btn_grp = QButtonGroup()
        self.btn_grp.setExclusive(True)
        i = 0

        for product in (products := self.product_gw.select(filter=filter, sort=sort, search=search)):
            groupBox = QGroupBox()

            # TODO: clean this mess
            label_product_name = QLabel("Название: " + product.name)
            label_product_description = QLabel("Описание: " + product.description[:70])
            label_product_manufacturer = QLabel("Производитель: " + product.manufacturer)
            label_product_price = QLabel("Цена: " + str(float(product.price)) + " ₽")
            label_product_discount = QLabel("Скидка: " + str(product.discount) + " %")
            if product.photo is None:
                product.photo = "picture.png"
            label_product_photo = QLabel()
            image_product_photo = QPixmap(self.path + "/gui/static/" + product.photo).scaledToWidth(70)
            label_product_photo.setPixmap(image_product_photo)

            button_order = QPushButton("Добавить в корзину")
            button_order.setStatusTip(str(i))
            self.buttons_products[str(i)] = product
            i += 1
            self.btn_grp.addButton(button_order)

            vbox = QVBoxLayout()
            vbox.maximumSize()
            vbox.addWidget(label_product_name)
            vbox.addWidget(label_product_description)
            vbox.addWidget(label_product_manufacturer)
            vbox.addWidget(label_product_price)
            vbox.addWidget(label_product_discount)
            vbox.addWidget(label_product_photo)
            vbox.addWidget(button_order)
            vbox.addStretch(1)
            groupBox.setLayout(vbox)

            if product.discount > 15:
                groupBox.setStyleSheet("background-color: #7fff00")

            self.catalog_window.scrollLayout.addRow(groupBox)

        self.btn_grp.buttonClicked.connect(self.add_to_order)

        total_amount_str = f"{len(products)} из {self.product_gw.select_total_amount()}"
        self.catalog_window.label_amount.setText(total_amount_str)

    def sign_out(self):
        reply = QMessageBox()
        reply.setText("Вы уверены, что хотите выйти?")
        reply.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        x = reply.exec()
        if x == QMessageBox.StandardButton.Yes:
            self.catalog_window.hide()
            self.auth_window.show()

    def get_pickup_points(self):
        pp = self.order_gw.get_pickup_points()
        self.pickup_points = {}
        for p in pp:
            self.pickup_points[p.address] = p.id
        lst = [p.address for p in pp]
        # TODO: fix it
        self.order_window.toggle_pickup_point.addItems(lst[:len(lst) // 2])

    def form_pdf(self):
        order_date =datetime.datetime.now().strftime("%m/%d/%Y")
        delivery_days = 0
        order_no = self.order_window.label_order_no_actual.text()
        fio = self.order_window.label_fio.text()
        sum = self.order_window.label_sum.text()
        discount = self.order_window.label_discount.text()
        pp = str(self.order_window.toggle_pickup_point.currentText())


        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('Anonymous_Pro', '', f'{self.path}/gui/font/Anonymous_Pro.ttf', uni=True)
        pdf.set_font('Anonymous_Pro', '', 14)

        pdf.cell(200, 10, txt=f"Заказ № {order_no}", ln=1, align='C')
        pdf.cell(200, 10, txt=f"", ln=1, align='C')

        pdf.cell(200, 10, txt=f"{fio}", ln=1, align='L')
        pdf.cell(200, 10, txt=f"{sum}", ln=2, align='L')
        pdf.cell(200, 10, txt=f"{discount}", ln=2, align='L')
        pdf.cell(200, 10, txt=f"", ln=1, align='C')

        pdf.cell(200, 10, txt=f"Дата заказа: {order_date}", ln=2, align='L')
        pdf.cell(200, 10, txt=f"Срок доставки: {delivery_days}", ln=2, align='L')
        pdf.cell(200, 10, txt=f"Пункт выдачи: {pp}", ln=2, align='L')
        pdf.cell(200, 10, txt=f"Код получения: {random.randint(100, 1000)}", ln=2, align='L')
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        pdf.output(desktop + "/order.pdf")

        QMessageBox.about(self.order_window, "Title", "Ваш талон сформирован. Сохранен на рабочий стол")


    def clear_order(self):
        for i in reversed(range(self.order_window.scrollLayout.count())):
            self.order_window.scrollLayout.itemAt(i).widget().setParent(None)

        self.sum = 0
        self.discount = 0
        self.order_products = []

        self.order_window.label_sum.setText("Общая сумма: 0 ₽")
        self.order_window.label_discount.setText("Общая скидка: 0 %")
        self.order_window.label_order_no_actual.setText("")


    def fill_order_products(self):
        for i in reversed(range(self.order_window.scrollLayout.count())):
            self.order_window.scrollLayout.itemAt(i).widget().setParent(None)

        for product in self.order_products:

            self.sum += product.price
            self.discount += product.discount
            groupBox = QGroupBox()

            label_product_name = QLabel("Название: " + product.name)
            # label_product_description = QLabel("Описание: " + product.description[:70])
            label_product_manufacturer = QLabel("Производитель: " + product.manufacturer)
            label_product_price = QLabel("Цена: " + str(float(product.price)) + " ₽")
            label_product_discount = QLabel("Скидка: " + str(product.discount) + " %")
            if product.photo is None:
                product.photo = "picture.png"
            label_product_photo = QLabel()
            image_product_photo = QPixmap(self.path + "/gui/static/" + product.photo).scaledToWidth(70)
            label_product_photo.setPixmap(image_product_photo)
            vbox = QVBoxLayout()
            vbox.minimumSize()
            vbox.addWidget(label_product_name)
            # vbox.addWidget(label_product_description)
            vbox.addWidget(label_product_manufacturer)
            vbox.addWidget(label_product_price)
            vbox.addWidget(label_product_discount)
            vbox.addWidget(label_product_photo)
            vbox.addStretch(1)
            groupBox.setLayout(vbox)
            self.order_window.scrollLayout.addRow(groupBox)

        self.order_window.label_fio.setText("ФИО: " + self.catalog_window.fio_button.text())
        self.order_window.label_sum.setText("Общая сумма: " + str(self.sum) + " ₽")
        self.order_window.label_discount.setText("Общая скидка: " + str(self.discount) + " %")
        self.order_window.label_order_no_actual.setText(str(int(self.order_gw.get_last_order_id()) + 1))

    def add_to_order(self, btn):
        self.order_available = True
        self.order_products.append(self.buttons_products[btn.statusTip()])
        self.fill_order_products()
        self.order_window.show()

    def new_order(self):
        user_id = ''
        if self.user is None:
            user_id = 'NULL'
        else:
            user_id = self.user.id
        pickup_point_id = self.pickup_points[str(self.order_window.toggle_pickup_point.currentText())]
        self.order_gw.new_order(pickup_point_id, user_id, datetime.datetime.now(), self.order_products)

        self.form_pdf()
        self.clear_order()