from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    id: int
    vendor_code: str
    name: str
    description: str
    category: str
    category_id: int
    photo: str
    manufacturer: str
    manufacturer_id: int
    supplier: str
    supplier_id: int
    price: float
    discount: int
    max_discount: int
    amount: int
    amount_selected: int = 0
