from fastapi import APIRouter
from app.models import Banner
from app.utils import success

router = APIRouter()

@router.get("")
async def get_banners():
    banners = await Banner.filter(status=1).order_by("sort_order")
    items = [{"id": b.id, "image": b.image, "link": b.link} for b in banners]
    return success(items)
