from fastapi import APIRouter, Depends, HTTPException, Header
from app.models import Product, ProductSku, Category, Order, User, Coupon, Banner
from app.utils import success, error
from app.config import settings
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
from jose import jwt, JWTError

router = APIRouter()

# 管理员账号配置（实际项目应存数据库）
ADMIN_USERS = {
    "admin": "admin123",  # 用户名: 密码
}

# ========== 管理员登录 ==========
class AdminLogin(BaseModel):
    username: str
    password: str

@router.post("/login")
async def admin_login(data: AdminLogin):
    if data.username not in ADMIN_USERS or ADMIN_USERS[data.username] != data.password:
        return error("用户名或密码错误")
    
    # 生成 Token
    expire = datetime.utcnow() + timedelta(hours=24)
    token = jwt.encode(
        {"sub": f"admin:{data.username}", "exp": expire},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return success({"token": token, "username": data.username})

# 验证管理员 Token
async def verify_admin(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="未登录")
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub", "")
        if not sub.startswith("admin:"):
            raise HTTPException(status_code=401, detail="无权限")
        return sub.split(":")[1]
    except JWTError:
        raise HTTPException(status_code=401, detail="Token 无效")

# ========== 统计 ==========
@router.get("/stats/products")
async def stats_products(admin: str = Depends(verify_admin)):
    count = await Product.all().count()
    return success({"count": count})

@router.get("/stats/orders")
async def stats_orders(admin: str = Depends(verify_admin)):
    count = await Order.all().count()
    orders = await Order.filter(status=3).all()
    total = sum(float(o.total_amount) for o in orders)
    return success({"count": count, "total_amount": total})

@router.get("/stats/users")
async def stats_users(admin: str = Depends(verify_admin)):
    count = await User.all().count()
    return success({"count": count})

# ========== 商品管理 ==========
class ProductCreate(BaseModel):
    name: str
    category_id: int
    cover: str
    images: List[str] = []
    description: str = ""
    base_price: float
    status: int = 1

@router.get("/products")
async def list_products(admin: str = Depends(verify_admin)):
    products = await Product.all().order_by("-id")
    items = [{
        "id": p.id, "name": p.name, "cover": p.cover, "images": p.images,
        "description": p.description, "base_price": float(p.base_price),
        "sales": p.sales, "status": p.status, "category_id": p.category_id
    } for p in products]
    return success(items)

@router.post("/products")
async def create_product(data: ProductCreate, admin: str = Depends(verify_admin)):
    product = await Product.create(**data.model_dump())
    # 创建默认SKU
    await ProductSku.create(
        product_id=product.id,
        spec_info={"规格": "默认"},
        price=data.base_price,
        original_price=data.base_price,
        stock=100
    )
    return success({"id": product.id})

@router.put("/products/{product_id}")
async def update_product(product_id: int, data: ProductCreate, admin: str = Depends(verify_admin)):
    await Product.filter(id=product_id).update(**data.model_dump())
    return success()

@router.delete("/products/{product_id}")
async def delete_product(product_id: int, admin: str = Depends(verify_admin)):
    await ProductSku.filter(product_id=product_id).delete()
    await Product.filter(id=product_id).delete()
    return success()

# ========== 分类管理 ==========
class CategoryCreate(BaseModel):
    name: str
    icon: str = ""
    sort_order: int = 0

@router.post("/categories")
async def create_category(data: CategoryCreate, admin: str = Depends(verify_admin)):
    category = await Category.create(**data.model_dump())
    return success({"id": category.id})

@router.put("/categories/{category_id}")
async def update_category(category_id: int, data: CategoryCreate, admin: str = Depends(verify_admin)):
    await Category.filter(id=category_id).update(**data.model_dump())
    return success()

@router.delete("/categories/{category_id}")
async def delete_category(category_id: int, admin: str = Depends(verify_admin)):
    await Category.filter(id=category_id).delete()
    return success()

# ========== 订单管理 ==========
@router.get("/orders")
async def list_orders(status: Optional[int] = None, page: int = 1, size: int = 20, admin: str = Depends(verify_admin)):
    query = Order.all()
    if status is not None:
        query = query.filter(status=status)
    
    total = await query.count()
    orders = await query.order_by("-id").offset((page-1)*size).limit(size).prefetch_related("user")
    
    items = []
    for o in orders:
        items.append({
            "id": o.id, "order_no": o.order_no, "total_amount": float(o.total_amount),
            "status": o.status, "created_at": str(o.created_at),
            "user": {"username": o.user.username} if o.user else None
        })
    
    return success({"items": items, "total": total})

@router.put("/orders/{order_id}/ship")
async def ship_order(order_id: int, admin: str = Depends(verify_admin)):
    order = await Order.get_or_none(id=order_id)
    if not order:
        return error("订单不存在")
    if order.status != 1:
        return error("订单状态不正确")
    order.status = 2
    await order.save()
    return success()

# ========== 用户管理 ==========
@router.get("/users")
async def list_users(admin: str = Depends(verify_admin)):
    users = await User.all().order_by("-id")
    items = [{
        "id": u.id, "username": u.username, "phone": u.phone,
        "created_at": str(u.created_at)
    } for u in users]
    return success(items)

# ========== 优惠券管理 ==========
class CouponCreate(BaseModel):
    name: str
    type: int  # 1满减 2折扣
    value: float
    min_amount: float = 0
    total: int
    start_time: datetime
    end_time: datetime

@router.get("/coupons")
async def list_coupons(admin: str = Depends(verify_admin)):
    coupons = await Coupon.all().order_by("-id")
    items = [{
        "id": c.id, "name": c.name, "type": c.type, "value": float(c.value),
        "min_amount": float(c.min_amount), "total": c.total, "remain": c.remain,
        "start_time": str(c.start_time), "end_time": str(c.end_time)
    } for c in coupons]
    return success(items)

@router.post("/coupons")
async def create_coupon(data: CouponCreate, admin: str = Depends(verify_admin)):
    coupon = await Coupon.create(**data.model_dump(), remain=data.total)
    return success({"id": coupon.id})

@router.delete("/coupons/{coupon_id}")
async def delete_coupon(coupon_id: int, admin: str = Depends(verify_admin)):
    await Coupon.filter(id=coupon_id).delete()
    return success()

# ========== 轮播图管理 ==========
class BannerCreate(BaseModel):
    image: str
    link: str = ""
    sort_order: int = 0

@router.post("/banners")
async def create_banner(data: BannerCreate, admin: str = Depends(verify_admin)):
    banner = await Banner.create(**data.model_dump())
    return success({"id": banner.id})

@router.put("/banners/{banner_id}")
async def update_banner(banner_id: int, data: BannerCreate, admin: str = Depends(verify_admin)):
    await Banner.filter(id=banner_id).update(**data.model_dump())
    return success()

@router.delete("/banners/{banner_id}")
async def delete_banner(banner_id: int, admin: str = Depends(verify_admin)):
    await Banner.filter(id=banner_id).delete()
    return success()
