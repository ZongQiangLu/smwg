from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from decimal import Decimal

class CategoryOut(BaseModel):
    id: int
    name: str
    icon: Optional[str]

class SkuOut(BaseModel):
    id: int
    spec_info: Dict[str, Any]
    price: Decimal
    original_price: Optional[Decimal]
    stock: int
    image: Optional[str]

class ProductOut(BaseModel):
    id: int
    name: str
    cover: str
    base_price: Decimal
    sales: int
    category_id: int

class ProductDetail(BaseModel):
    id: int
    name: str
    cover: str
    images: List[str]
    description: Optional[str]
    base_price: Decimal
    sales: int
    category_id: int
    skus: List[SkuOut]
    is_favorite: bool = False
    review_count: int = 0
    avg_rating: float = 0
