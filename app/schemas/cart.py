from typing import Dict, Any, Optional
from pydantic import BaseModel
from decimal import Decimal

class CartAdd(BaseModel):
    sku_id: int
    quantity: int = 1

class CartUpdate(BaseModel):
    quantity: Optional[int] = None
    selected: Optional[bool] = None

class CartOut(BaseModel):
    id: int
    sku_id: int
    product_id: int
    product_name: str
    product_image: str
    spec_info: Dict[str, Any]
    price: Decimal
    stock: int
    quantity: int
    selected: bool
