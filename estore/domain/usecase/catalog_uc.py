from PyQt6.QtWidgets import QLabel

from estore.gateway.product_gw import ProductGateway


class CatalogUseCase():
    def __init__(self, gw: ProductGateway, catalog_window):
        self.gw = gw
        self.catalog_window = catalog_window
        self.fill_products()

        self.catalog_window.search_input.returnPressed.connect(self.fill_products)
        self.catalog_window.search_input.selectionChanged.connect(self.fill_products)
        self.catalog_window.search_input.textChanged.connect(self.fill_products)
        self.catalog_window.search_input.textEdited.connect(self.fill_products)

        self.catalog_window.toggle_filter.currentIndexChanged.connect(self.fill_products)
        self.catalog_window.toggle_sort.currentIndexChanged.connect(self.fill_products)

    def fill_products(self):

        for i in reversed(range(self.catalog_window.scrollLayout.count())):
            self.catalog_window.scrollLayout.itemAt(i).widget().setParent(None)

        filter = str(self.catalog_window.toggle_filter.currentText())
        sort = str(self.catalog_window.toggle_sort.currentText())
        search = self.catalog_window.search_input.text()

        for product in self.gw.select(filter=filter, sort=sort, search=search):
            label = QLabel(product.name)
            self.catalog_window.scrollLayout.addRow(label)


