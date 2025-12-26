from typing import Any, Optional
from pydantic import BaseModel

class ResponseModel(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None

def success(data: Any = None, message: str = "success") -> dict:
    return {"code": 200, "message": message, "data": data}

def error(message: str = "error", code: int = 400) -> dict:
    return {"code": code, "message": message, "data": None}
