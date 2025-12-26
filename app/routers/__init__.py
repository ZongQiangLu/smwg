from fastapi import APIRouter
from app.routers import auth, products, categories, cart, orders, addresses, favorites, footprints, search, coupons, reviews, banners, admin

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(products.router, prefix="/products", tags=["商品"])
api_router.include_router(categories.router, prefix="/categories", tags=["分类"])
api_router.include_router(cart.router, prefix="/cart", tags=["购物车"])
api_router.include_router(orders.router, prefix="/orders", tags=["订单"])
api_router.include_router(addresses.router, prefix="/addresses", tags=["地址"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["收藏"])
api_router.include_router(footprints.router, prefix="/footprints", tags=["足迹"])
api_router.include_router(search.router, prefix="/search", tags=["搜索"])
api_router.include_router(coupons.router, prefix="/coupons", tags=["优惠券"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["评价"])
api_router.include_router(banners.router, prefix="/banners", tags=["轮播图"])
api_router.include_router(admin.router, prefix="/admin", tags=["管理后台"])
