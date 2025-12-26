from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class CouponOut(BaseModel):
    id: int
    name: str
    type: int
    value: Decimal
    min_amount: Decimal
    start_time: datetime
    end_time: datetime
    remain: int

class UserCouponOut(BaseModel):
    id: int
    coupon_id: int
    name: str
    type: int
    value: Decimal
    min_amount: Decimal
    end_time: datetime
    status: int
