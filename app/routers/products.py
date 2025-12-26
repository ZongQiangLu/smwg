from fastapi import APIRouter, Query, Depends
from typing import Optional
from app.models import Product, ProductSku, Favorite, Footprint, Review, SearchHistory, User
from app.utils import success, get_current_user
from tortoise.functions import Avg

router = APIRouter()

@router.get("")
async def get_products(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    category_id: Optional[int] = None,
    keyword: Optional[str] = None,
    sort: str = Query("default", regex="^(default|sales|price_asc|price_desc)$")
):
    query = Product.filter(status=1)
    if category_id:
        query = query.filter(category_id=category_id)
    if keyword:
        query = query.filter(name__icontains=keyword)
    
    if sort == "sales":
        query = query.order_by("-sales")
    elif sort == "price_asc":
        query = query.order_by("base_price")
    elif sort == "price_desc":
        query = query.order_by("-base_price")
    else:
        query = query.order_by("-id")
    
    total = await query.count()
    products = await query.offset((page - 1) * size).limit(size)
    
    items = [{
        "id": p.id,
        "name": p.name,
        "cover": p.cover,
        "base_price": float(p.base_price),
        "sales": p.sales,
        "category_id": p.category_id
    } for p in products]
    
    return success({"total": total, "items": items})

@router.get("/hot")
async def get_hot_products(size: int = Query(10, ge=1, le=20)):
    products = await Product.filter(status=1).order_by("-sales").limit(size)
    items = [{
        "id": p.id,
        "name": p.name,
        "cover": p.cover,
        "base_price": float(p.base_price),
        "sales": p.sales
    } for p in products]
    return success(items)

@router.get("/{product_id}")
async def get_product_detail(product_id: int):
    product = await Product.get_or_none(id=product_id, status=1)
    if not product:
        return success(None, "商品不存在")
    
    skus = await ProductSku.filter(product_id=product_id)
    reviews = await Review.filter(product_id=product_id)
    review_count = len(reviews)
    avg_rating = sum(r.rating for r in reviews) / review_count if review_count else 0
    
    is_favorite = False
    # 足迹记录需要登录后处理
    
    return success({
        "id": product.id,
        "name": product.name,
        "cover": product.cover,
        "images": product.images,
        "description": product.description,
        "base_price": float(product.base_price),
        "sales": product.sales,
        "category_id": product.category_id,
        "is_favorite": is_favorite,
        "review_count": review_count,
        "avg_rating": round(avg_rating, 1),
        "skus": [{
            "id": s.id,
            "spec_info": s.spec_info,
            "price": float(s.price),
            "original_price": float(s.original_price) if s.original_price else None,
            "stock": s.stock,
            "image": s.image
        } for s in skus]
    })

@router.get("/{product_id}/reviews")
async def get_product_reviews(
    product_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50)
):
    query = Review.filter(product_id=product_id).order_by("-created_at")
    total = await query.count()
    reviews = await query.offset((page - 1) * size).limit(size).prefetch_related("user")
    
    items = [{
        "id": r.id,
        "user_id": r.user_id,
        "username": r.user.username,
        "avatar": r.user.avatar,
        "rating": r.rating,
        "content": r.content,
        "images": r.images,
        "created_at": r.created_at.isoformat()
    } for r in reviews]
    
    return success({"total": total, "items": items})
