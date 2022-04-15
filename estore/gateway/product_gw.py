from estore.domain.entity.user import User
from typing import Union
from typing import List
from estore.domain.entity.product import Product


class ProductGateway():

    filter_map = {
        "price_acs": " ORDER BY p.price ASC",
        "price_desc": " ORDER BY p.price DESC",
    }
    sort_map = {
        "<10": "WHERE p.discount < 10",
        "<15": "WHERE p.discount >= 10 AND WHERE p.discount < 15",
        ">15": "WHERE p.discount > 15",
    }

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def form_select_query(self, filter, sort, search, raw_query):
        query = raw_query
        if sort:
            query += self.sort_map[sort]
            if search:
                query += f" AND p.name LIKE '{search}%%'"
        else:
            if search:
                query += f" WHERE p.name LIKE '{search}%%'"
        if filter:
            query += self.filter_map[filter]
        return query + ";"


    def select(self, filter=None, sort=None, search=None) -> Union[List[Product], List]:
        raw_query = f"""
        SELECT p.id,
               p.vendor_code,
               p.name,
               p.description,
               c.name,
               p.category_id,
               p.photo,
               m.name,
               p.manufacturer_id,
               s.name,
               p.supplier_id,
               p.price,
               p.discount,
               p.max_discount,
               p.amount
        FROM estore.product p
        INNER JOIN estore.category c ON p.category_id = c.id
        INNER JOIN estore.manufacturer m ON p.manufacturer_id = m.id
        INNER JOIN estore.supplier s ON p.supplier_id = s.id
        """

        query = self.form_select_query(filter, sort, search, raw_query)
        res = [list(x) for x in self.db_conn.execute(query).fetchall()]
        products = []
        if len(res) == 0:
            return products
        for i in range(len(res)):
            products.append(
                Product(
                    id=res[i][0],
                    vendor_code=res[i][1],
                    name=res[i][2],
                    description=res[i][3],
                    category=res[i][4],
                    category_id=res[i][5],
                    photo=res[i][6],
                    manufacturer=res[i][7],
                    manufacturer_id=res[i][8],
                    supplier=res[i][9],
                    supplier_id=res[i][10],
                    price=res[i][11],
                    discount=res[i][12],
                    max_discount=res[i][13],
                    amount=res[i][14],
                )
            )
        return products
