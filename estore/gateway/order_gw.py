from typing import List

from estore.domain.entity.pickup_point import PickupPoint


class OrderGateway():

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_pickup_points(self) -> List[PickupPoint]:
        query = f"""
        SELECT pp.id, pp.address FROM estore.pickup_point pp;
        """
        res = [list(x) for x in self.db_conn.execute(query).fetchall()]
        pickup_points = []
        [pickup_points.append(PickupPoint(id=pp[0], address=pp[1])) for pp in res]
        return pickup_points

    def get_last_order_id(self):
        query_order_id = """SELECT o.id FROM estore.`order` o ORDER BY o.id DESC LIMIT 1;"""
        res = [list(x) for x in self.db_conn.execute(query_order_id).fetchall()]
        return str(res[0][0]) if len(res[0]) != 0 else "0"

    def new_order(self, pickup_point_id, user_id, delivery_date, products):
        query_order = f"""
        INSERT INTO estore.`order` (status_id, delivery_date, pickup_point_id, user_id)
        VALUES (1, '{delivery_date}', {pickup_point_id}, {user_id});
        """

        query_order_details = """
        INSERT INTO estore.order_details (order_id, product_id, amount) 
        VALUES ({}, {}, {});
        """

        self.db_conn.execute(query_order)
        order_id = self.get_last_order_id()

        for product in products:
            self.db_conn.execute(query_order_details.format(order_id, product.id, product.amount_selected))
