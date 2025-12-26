from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    phone: Optional[str]
    avatar: Optional[str]
    created_at: datetime

class AddressCreate(BaseModel):
    name: str
    phone: str
    province: str
    city: str
    district: str
    detail: str
    is_default: bool = False

class AddressOut(BaseModel):
    id: int
    name: str
    phone: str
    province: str
    city: str
    district: str
    detail: str
    is_default: bool
