from fastapi import APIRouter, Depends, Query
from app.models import Footprint, Product, User
from app.utils import success, get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/{product_id}")
async def add_footprint(product_id: int, user: User = Depends(get_current_user)):
    product = await Product.get_or_none(id=product_id)
    if not product:
        return success()  # 静默失败
    
    # 检查是否已存在，存在则更新时间
    footprint = await Footprint.get_or_none(user_id=user.id, product_id=product_id)
    if footprint:
        footprint.created_at = datetime.now()
        await footprint.save()
    else:
        await Footprint.create(user_id=user.id, product_id=product_id)
    
    return success()

@router.get("")
async def get_footprints(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    user: User = Depends(get_current_user)
):
    query = Footprint.filter(user_id=user.id)
    total = await query.count()
    footprints = await query.order_by("-created_at").offset((page - 1) * size).limit(size)
    
    items = []
    for f in footprints:
        product = await Product.get(id=f.product_id)
        items.append({
            "id": f.id,
            "product_id": product.id,
            "name": product.name,
            "cover": product.cover,
            "base_price": float(product.base_price),
            "created_at": f.created_at.isoformat()
        })
    
    return success({"total": total, "items": items})

@router.delete("/clear")
async def clear_footprints(user: User = Depends(get_current_user)):
    await Footprint.filter(user_id=user.id).delete()
    return success()
