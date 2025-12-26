from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class OrderItemCreate(BaseModel):
    sku_id: int
    quantity: int

class OrderCreate(BaseModel):
    address_id: int
    items: List[OrderItemCreate]
    coupon_id: Optional[int] = None
    remark: Optional[str] = None

class OrderItemOut(BaseModel):
    id: int
    product_name: str
    product_image: str
    spec_info: Dict[str, Any]
    quantity: int
    price: Decimal
    is_reviewed: bool

class LogisticsOut(BaseModel):
    company: str
    tracking_no: str
    status: int
    traces: List[Dict[str, Any]]

class OrderOut(BaseModel):
    id: int
    order_no: str
    total_amount: Decimal
    pay_amount: Decimal
    status: int
    created_at: datetime
    item_count: int = 0
    first_item_image: Optional[str] = None

class OrderDetail(BaseModel):
    id: int
    order_no: str
    total_amount: Decimal
    pay_amount: Decimal
    status: int
    address_snapshot: Dict[str, Any]
    remark: Optional[str]
    created_at: datetime
    items: List[OrderItemOut]
    logistics: Optional[LogisticsOut] = None
