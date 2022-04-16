from dataclasses import dataclass
from datetime import datetime
from typing import List
from estore.domain.entity.product import ProductSimple

@dataclass
class Order:
    id: int
    status: str
    order_date: datetime
    delivery_date: datetime
    sum: float
    discount: int
    client_name: str
    products: List[ProductSimple]


