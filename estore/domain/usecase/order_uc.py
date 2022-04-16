import os

from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import QLabel, QMessageBox, QGroupBox, QRadioButton, QVBoxLayout, QPushButton, QStyle

from estore.gateway.order_gw import OrderGateway


class OrderUseCase():
    def __init__(self, gw: OrderGateway, order_window, catalog_window, auth_window, path):
        self.gw = gw
        self.order_window = order_window
        self.catalog_window = catalog_window
        self.auth_window = auth_window
        self.path = path
        self.user = None
        self.products = []
        self.fill_order_products()


    def fill_order_products(self):
        for i in reversed(range(self.order_window.scrollLayout.count())):
            self.order_window.scrollLayout.itemAt(i).widget().setParent(None)

        for product in self.products:
            groupBox = QGroupBox()

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

            # button_order = QPushButton("Добавить в корзину")

            vbox = QVBoxLayout()
            vbox.maximumSize()
            vbox.addWidget(label_product_name)
            vbox.addWidget(label_product_description)
            vbox.addWidget(label_product_manufacturer)
            vbox.addWidget(label_product_price)
            vbox.addWidget(label_product_discount)
            vbox.addWidget(label_product_photo)
            # vbox.addWidget(button_order)
            vbox.addStretch(1)
            groupBox.setLayout(vbox)
            #
            # if product.discount > 15:
            #     groupBox.setStyleSheet("background-color: #7fff00")

            self.catalog_window.scrollLayout.addRow(groupBox)
        #
        # total_amount_str = f"{len(products)} из {self.gw.select_total_amount()}"
        # self.catalog_window.label_amount.setText(total_amount_str)
