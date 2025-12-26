from fastapi import APIRouter
from app.models import Category
from app.utils import success

router = APIRouter()

@router.get("")
async def get_categories():
    categories = await Category.all().order_by("sort_order")
    items = [{"id": c.id, "name": c.name, "icon": c.icon} for c in categories]
    return success(items)
