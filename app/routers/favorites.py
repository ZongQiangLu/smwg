from fastapi import APIRouter, Depends, Query
from app.models import Favorite, Product, User
from app.utils import success, get_current_user

router = APIRouter()

@router.get("")
async def get_favorites(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    user: User = Depends(get_current_user)
):
    query = Favorite.filter(user_id=user.id)
    total = await query.count()
    favorites = await query.order_by("-created_at").offset((page - 1) * size).limit(size)
    
    items = []
    for f in favorites:
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

@router.post("/{product_id}")
async def add_favorite(product_id: int, user: User = Depends(get_current_user)):
    product = await Product.get_or_none(id=product_id)
    if not product:
        return success(None, "商品不存在")
    
    await Favorite.get_or_create(user_id=user.id, product_id=product_id)
    return success()

@router.delete("/{product_id}")
async def remove_favorite(product_id: int, user: User = Depends(get_current_user)):
    await Favorite.filter(user_id=user.id, product_id=product_id).delete()
    return success()
