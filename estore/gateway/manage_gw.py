from typing import List

from estore.domain.entity.order import Order
from estore.domain.entity.product import ProductSimple


def filter_price_asc(orders):
    return sorted(orders, key=lambda order: order.sum)

def filter_price_desc(orders):
    return sorted(orders, key=lambda order: order.sum, reverse=True)

def nothing(orders):
    return orders

def less_ten(orders):
    sorter_orders = []
    for order in orders:
        if order.discount < 10:
            sorter_orders.append(order)
    return sorter_orders

def less_fifteen(orders):
    sorter_orders = []
    for order in orders:
        if (order.discount >= 10) and (order.discount < 15):
            sorter_orders.append(order)
    return sorter_orders

def more_fifteen(orders):
    sorter_orders = []
    for order in orders:
        if order.discount > 15:
            sorter_orders.append(order)
    return sorter_orders

class ManageGateway():
    filter_map = {
        "Нет": nothing,
        "по возрастанию цены": filter_price_asc,
        "По убыванию цены": filter_price_desc,
    }
    sort_map = {
        "Все диапазоны": nothing,
        "0-9.99%": less_ten,
        "10-14.99%": less_fifteen,
        ">15%": more_fifteen,
    }

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_order_details(self, order_id):
        query = f"""
        SELECT p.name, p.price, p.discount, p.amount FROM estore.order_details od
        INNER JOIN estore.product p ON od.product_id = p.id
        WHERE od.order_id = {order_id};
        """

        res = [list(x) for x in self.db_conn.execute(query).fetchall()]
        products_in_order = []
        total_price = 0
        total_discount = 0
        for r in res:
            products_in_order.append(
                ProductSimple(
                    name=r[0],
                    price=r[1],
                    discount=r[2],
                    amount=r[3],
                )
            )
            total_price += r[1]
            total_discount += r[2]
        return products_in_order, total_price, total_discount

    def get_orders(self, filter, sort) -> List[Order]:
        query = f"""
            SELECT o.id, s.name, o.order_date, o.delivery_date, u.surname, u.name, u.patronymic
            FROM estore.order o
            INNER JOIN estore.status s ON o.status_id = s.id
            INNER JOIN estore.user u ON o.user_id = u.id;
            """
        res = [list(x) for x in self.db_conn.execute(query).fetchall()]
        orders = []
        for r in res:
            orders.append(Order(
                id=r[0],
                status=r[1],
                order_date=r[2],
                delivery_date=r[3],
                sum=0,
                discount=0,
                client_name=f"{r[4]} {r[5]} {r[6]}",
                products=[],
            ))
        for order in orders:
            order.products, order.sum, order.discount = self.get_order_details(order.id)

        orders = self.filter_map[filter](orders)
        orders = self.sort_map[sort](orders)

        return orders



