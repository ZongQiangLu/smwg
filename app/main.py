from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.config import settings
from app.database import init_db, close_db
from app.routers import api_router
import os

async def init_sample_data():
    """初始化示例数据"""
    from datetime import datetime, timedelta
    from app.models import Category, Product, ProductSku, Banner, Coupon
    
    # 检查是否已有数据
    if await Category.exists():
        return
    
    print("初始化示例数据...")
    
    # 创建分类
    categories = [
        {"name": "手机", "icon": "/static/cat_phone.png", "sort_order": 1},
        {"name": "电脑", "icon": "/static/cat_computer.png", "sort_order": 2},
        {"name": "平板", "icon": "/static/cat_tablet.png", "sort_order": 3},
        {"name": "耳机", "icon": "/static/cat_headphone.png", "sort_order": 4},
        {"name": "手表", "icon": "/static/cat_watch.png", "sort_order": 5},
        {"name": "配件", "icon": "/static/cat_accessory.png", "sort_order": 6},
    ]
    for c in categories:
        await Category.create(**c)
    
    # 创建商品
    products_data = [
        {"category_id": 1, "name": "iPhone 15 Pro Max", "cover": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop", "images": ["https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop"], "description": "Apple iPhone 15 Pro Max，A17 Pro芯片", "base_price": 9999, "sales": 1234, "skus": [{"spec_info": {"颜色": "原色钛金属", "内存": "256GB"}, "price": 9999, "original_price": 10999, "stock": 100}]},
        {"category_id": 1, "name": "华为 Mate 60 Pro", "cover": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop", "images": ["https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop"], "description": "华为Mate60 Pro，麒麟芯片", "base_price": 6999, "sales": 2345, "skus": [{"spec_info": {"颜色": "雅丹黑", "内存": "256GB"}, "price": 6999, "original_price": 7499, "stock": 200}]},
        {"category_id": 1, "name": "小米14 Ultra", "cover": "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=400&h=400&fit=crop", "images": ["https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=400&h=400&fit=crop"], "description": "徕卡光学镜头，骁龙8 Gen3", "base_price": 6499, "sales": 2345, "skus": [{"spec_info": {"颜色": "黑色", "内存": "256GB"}, "price": 6499, "original_price": 6999, "stock": 150}]},
        {"category_id": 2, "name": "MacBook Pro 14", "cover": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop", "images": ["https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop"], "description": "Apple MacBook Pro 14英寸，M3 Pro芯片", "base_price": 14999, "sales": 567, "skus": [{"spec_info": {"颜色": "深空黑", "配置": "18GB+512GB"}, "price": 14999, "original_price": 16999, "stock": 30}]},
        {"category_id": 2, "name": "联想小新Pro16", "cover": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop", "images": ["https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop"], "description": "酷睿i5-13500H，16GB内存", "base_price": 5999, "sales": 987, "skus": [{"spec_info": {"配置": "i5/16GB/512GB"}, "price": 5999, "original_price": 6499, "stock": 60}]},
        {"category_id": 3, "name": "iPad Pro 12.9", "cover": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop", "images": ["https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop"], "description": "Apple iPad Pro 12.9英寸，M2芯片", "base_price": 8999, "sales": 890, "skus": [{"spec_info": {"颜色": "深空灰", "存储": "256GB"}, "price": 8999, "original_price": 9499, "stock": 60}]},
        {"category_id": 3, "name": "小米平板6 Pro", "cover": "https://images.unsplash.com/photo-1568656012937-8982e65df4b4?w=400&h=400&fit=crop", "images": ["https://images.unsplash.com/photo-1568656012937-8982e65df4b4?w=400&h=400&fit=crop"], "description": "骁龙8+，144Hz高刷", "base_price": 2499, "sales": 2134, "skus": [{"spec_info": {"颜色": "黑色", "存储": "128GB"}, "price": 2499, "original_price": 2799, "stock": 200}]},
        {"category_id": 4, "name": "AirPods Pro 2", "cover": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop", "images": ["https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop"], "description": "Apple AirPods Pro 第二代，主动降噪", "base_price": 1899, "sales": 3456, "skus": [{"spec_info": {"版本": "USB-C充电盒"}, "price": 1899, "original_price": 1999, "stock": 500}]},
        {"category_id": 4, "name": "索尼WH-1000XM5", "cover": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=400&fit=crop", "images": ["https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=400&fit=crop"], "description": "顶级降噪，30小时续航", "base_price": 2499, "sales": 3456, "skus": [{"spec_info": {"颜色": "黑色"}, "price": 2499, "original_price": 2899, "stock": 200}]},
        {"category_id": 5, "name": "Apple Watch Ultra 2", "cover": "https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400&h=400&fit=crop", "images": ["https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400&h=400&fit=crop"], "description": "Apple Watch Ultra 2，钛金属表壳", "base_price": 6499, "sales": 234, "skus": [{"spec_info": {"表带": "高山回环表带"}, "price": 6499, "original_price": 6999, "stock": 100}]},
        {"category_id": 5, "name": "小米手表S3", "cover": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop", "images": ["https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop"], "description": "eSIM独立通话，运动健康", "base_price": 999, "sales": 4567, "skus": [{"spec_info": {"颜色": "黑色"}, "price": 999, "original_price": 1199, "stock": 300}]},
        {"category_id": 6, "name": "倍思100W氮化镓充电器", "cover": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=400&fit=crop", "images": ["https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=400&fit=crop"], "description": "4口快充，小巧便携", "base_price": 199, "sales": 8765, "skus": [{"spec_info": {"功率": "100W"}, "price": 199, "original_price": 249, "stock": 500}]},
        {"category_id": 6, "name": "罗技MX Master 3S", "cover": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop", "images": ["https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop"], "description": "静音点击，8000DPI", "base_price": 799, "sales": 3456, "skus": [{"spec_info": {"颜色": "石墨黑"}, "price": 799, "original_price": 899, "stock": 200}]},
    ]
    
    for p_data in products_data:
        skus = p_data.pop("skus")
        product = await Product.create(**p_data)
        for sku in skus:
            await ProductSku.create(product_id=product.id, **sku)
    
    # 创建轮播图
    banners = [
        {"image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=750&h=300&fit=crop", "link": "/pages/product/detail?id=1", "sort_order": 1},
        {"image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=750&h=300&fit=crop", "link": "/pages/product/detail?id=4", "sort_order": 2},
    ]
    for b in banners:
        await Banner.create(**b)
    
    # 创建优惠券
    now = datetime.now()
    coupons = [
        {"name": "新人专享券", "type": 1, "value": 50, "min_amount": 200, "start_time": now, "end_time": now + timedelta(days=30), "total": 1000, "remain": 1000},
        {"name": "满500减100", "type": 1, "value": 100, "min_amount": 500, "start_time": now, "end_time": now + timedelta(days=15), "total": 500, "remain": 500},
    ]
    for c in coupons:
        await Coupon.create(**c)
    
    print("示例数据初始化完成!")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_sample_data()
    yield
    await close_db()

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# 挂载管理后台静态文件
admin_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "admin")
if os.path.exists(admin_path):
    app.mount("/admin", StaticFiles(directory=admin_path, html=True), name="admin")

@app.get("/")
async def root():
    return {"message": "数码网购平台 API"}
