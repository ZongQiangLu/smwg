from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class ReviewCreate(BaseModel):
    order_item_id: int
    rating: int
    content: Optional[str] = None
    images: List[str] = []

class ReviewOut(BaseModel):
    id: int
    user_id: int
    username: str
    avatar: Optional[str]
    rating: int
    content: Optional[str]
    images: List[str]
    created_at: datetime
