"""初始化测试数据"""
import asyncio
from datetime import datetime, timedelta
from tortoise import Tortoise
from app.database import TORTOISE_ORM
from app.models import Category, Product, ProductSku, Banner, Coupon

async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    
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
        exists = await Category.filter(name=c["name"]).exists()
        if not exists:
            await Category.create(**c)
    print("分类创建完成")
    
    # 创建商品 - 使用 tt.sql 数据 + update_product_images.sql 图片
    products_data = [
        # 手机 (category_id=1)
        {
            "category_id": 1, "name": "iPhone 15 Pro Max", 
            "cover": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=400&h=400&fit=crop"],
            "description": "Apple iPhone 15 Pro Max，A17 Pro芯片，钛金属设计", "base_price": 9999, "sales": 1234,
            "skus": [
                {"spec_info": {"颜色": "原色钛金属", "内存": "256GB"}, "price": 9999, "original_price": 10999, "stock": 100},
                {"spec_info": {"颜色": "原色钛金属", "内存": "512GB"}, "price": 11999, "original_price": 12999, "stock": 50},
                {"spec_info": {"颜色": "蓝色钛金属", "内存": "256GB"}, "price": 9999, "original_price": 10999, "stock": 80},
            ]
        },
        {
            "category_id": 1, "name": "华为 Mate 60 Pro", 
            "cover": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1592750475338-39e1006fb7b7?w=400&h=400&fit=crop"],
            "description": "华为Mate60 Pro，麒麟芯片回归，卫星通话", "base_price": 6999, "sales": 2345,
            "skus": [
                {"spec_info": {"颜色": "雅丹黑", "内存": "256GB"}, "price": 6999, "original_price": 7499, "stock": 200},
                {"spec_info": {"颜色": "白沙银", "内存": "512GB"}, "price": 7999, "original_price": 8499, "stock": 150},
            ]
        },
        {
            "category_id": 1, "name": "小米14 Ultra", 
            "cover": "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1592750475338-39e1006fb7b7?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1560469901-75f8f9a32690?w=400&h=400&fit=crop"],
            "description": "徕卡光学镜头，骁龙8 Gen3", "base_price": 6499, "sales": 2345,
            "skus": [
                {"spec_info": {"颜色": "黑色", "内存": "256GB"}, "price": 6499, "original_price": 6999, "stock": 150},
                {"spec_info": {"颜色": "白色", "内存": "512GB"}, "price": 7499, "original_price": 7999, "stock": 100},
            ]
        },
        {
            "category_id": 1, "name": "OPPO Find X7 Ultra", 
            "cover": "https://images.unsplash.com/photo-1592750475338-39e1006fb7b7?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1592750475338-39e1006fb7b7?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1560469901-75f8f9a32690?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1597762138661-70dcd1ba832f?w=400&h=400&fit=crop"],
            "description": "哈苏影像，双潜望长焦", "base_price": 5999, "sales": 1876,
            "skus": [
                {"spec_info": {"颜色": "海阔天空", "内存": "256GB"}, "price": 5999, "original_price": 6499, "stock": 120},
                {"spec_info": {"颜色": "大漠银月", "内存": "512GB"}, "price": 6999, "original_price": 7499, "stock": 80},
            ]
        },
        {
            "category_id": 1, "name": "vivo X100 Pro", 
            "cover": "https://images.unsplash.com/photo-1560469901-75f8f9a32690?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1560469901-75f8f9a32690?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1597762138661-70dcd1ba832f?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop"],
            "description": "蔡司影像，天玑9300", "base_price": 5299, "sales": 1543,
            "skus": [
                {"spec_info": {"颜色": "白月光", "内存": "256GB"}, "price": 5299, "original_price": 5799, "stock": 180},
                {"spec_info": {"颜色": "落日橙", "内存": "512GB"}, "price": 5999, "original_price": 6499, "stock": 100},
            ]
        },
        # 电脑 (category_id=2)
        {
            "category_id": 2, "name": "MacBook Pro 14", 
            "cover": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1587614382346-4ec70e388b28?w=400&h=400&fit=crop"],
            "description": "Apple MacBook Pro 14英寸，M3 Pro芯片", "base_price": 14999, "sales": 567,
            "skus": [
                {"spec_info": {"颜色": "深空黑", "内存": "18GB+512GB"}, "price": 14999, "original_price": 16999, "stock": 30},
                {"spec_info": {"颜色": "银色", "内存": "36GB+1TB"}, "price": 22999, "original_price": 24999, "stock": 20},
            ]
        },
        {
            "category_id": 2, "name": "联想小新Pro16", 
            "cover": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1587614382346-4ec70e388b28?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1552831388-6a0b3575b32a?w=400&h=400&fit=crop"],
            "description": "酷睿i5-13500H，16GB内存", "base_price": 5999, "sales": 987,
            "skus": [
                {"spec_info": {"配置": "i5-13500H/16GB/512GB"}, "price": 5999, "original_price": 6499, "stock": 60},
                {"spec_info": {"配置": "i7-13700H/32GB/1TB"}, "price": 7999, "original_price": 8499, "stock": 40},
            ]
        },
        {
            "category_id": 2, "name": "华硕天选4", 
            "cover": "https://images.unsplash.com/photo-1587614382346-4ec70e388b28?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1587614382346-4ec70e388b28?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1552831388-6a0b3575b32a?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1532339142463-fd0a8979791a?w=400&h=400&fit=crop"],
            "description": "RTX4060，144Hz电竞屏", "base_price": 6999, "sales": 765,
            "skus": [
                {"spec_info": {"配置": "R7-7840H/RTX4060/16GB"}, "price": 6999, "original_price": 7499, "stock": 50},
                {"spec_info": {"配置": "R9-7945HX/RTX4070/32GB"}, "price": 9999, "original_price": 10999, "stock": 25},
            ]
        },
        # 平板 (category_id=3)
        {
            "category_id": 3, "name": "iPad Pro 12.9", 
            "cover": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1568656012937-8982e65df4b4?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1532339142463-fd0a8979791a?w=400&h=400&fit=crop"],
            "description": "Apple iPad Pro 12.9英寸，M2芯片", "base_price": 8999, "sales": 890,
            "skus": [
                {"spec_info": {"颜色": "深空灰", "存储": "256GB"}, "price": 8999, "original_price": 9499, "stock": 60},
                {"spec_info": {"颜色": "银色", "存储": "512GB"}, "price": 10999, "original_price": 11499, "stock": 40},
            ]
        },
        {
            "category_id": 3, "name": "小米平板6 Pro", 
            "cover": "https://images.unsplash.com/photo-1568656012937-8982e65df4b4?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1568656012937-8982e65df4b4?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1532339142463-fd0a8979791a?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop"],
            "description": "骁龙8+，144Hz高刷", "base_price": 2499, "sales": 2134,
            "skus": [
                {"spec_info": {"颜色": "黑色", "存储": "128GB"}, "price": 2499, "original_price": 2799, "stock": 200},
                {"spec_info": {"颜色": "金色", "存储": "256GB"}, "price": 2999, "original_price": 3299, "stock": 150},
            ]
        },
        {
            "category_id": 3, "name": "荣耀平板V8 Pro", 
            "cover": "https://images.unsplash.com/photo-1532339142463-fd0a8979791a?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1532339142463-fd0a8979791a?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1568656012937-8982e65df4b4?w=400&h=400&fit=crop"],
            "description": "天玑8100，12.1英寸大屏", "base_price": 2999, "sales": 1567,
            "skus": [
                {"spec_info": {"颜色": "曜石黑", "存储": "128GB"}, "price": 2999, "original_price": 3299, "stock": 100},
                {"spec_info": {"颜色": "燃橙色", "存储": "256GB"}, "price": 3499, "original_price": 3799, "stock": 80},
            ]
        },
        # 耳机 (category_id=4)
        {
            "category_id": 4, "name": "AirPods Pro 2", 
            "cover": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1572569028738-411a1971d29d?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=400&fit=crop"],
            "description": "Apple AirPods Pro 第二代，主动降噪", "base_price": 1899, "sales": 3456,
            "skus": [
                {"spec_info": {"版本": "USB-C充电盒"}, "price": 1899, "original_price": 1999, "stock": 500},
            ]
        },
        {
            "category_id": 4, "name": "索尼WH-1000XM5", 
            "cover": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1572569028738-411a1971d29d?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop"],
            "description": "顶级降噪，30小时续航", "base_price": 2499, "sales": 3456,
            "skus": [
                {"spec_info": {"颜色": "黑色"}, "price": 2499, "original_price": 2899, "stock": 200},
                {"spec_info": {"颜色": "银色"}, "price": 2499, "original_price": 2899, "stock": 150},
            ]
        },
        {
            "category_id": 4, "name": "Bose QC45", 
            "cover": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1572569028738-411a1971d29d?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=400&fit=crop"],
            "description": "舒适佩戴，出色降噪", "base_price": 2299, "sales": 2789,
            "skus": [
                {"spec_info": {"颜色": "黑色"}, "price": 2299, "original_price": 2599, "stock": 180},
                {"spec_info": {"颜色": "白色"}, "price": 2299, "original_price": 2599, "stock": 120},
            ]
        },
        # 手表 (category_id=5)
        {
            "category_id": 5, "name": "Apple Watch Ultra 2", 
            "cover": "https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=400&h=400&fit=crop"],
            "description": "Apple Watch Ultra 2，钛金属表壳", "base_price": 6499, "sales": 234,
            "skus": [
                {"spec_info": {"表带": "高山回环表带"}, "price": 6499, "original_price": 6999, "stock": 100},
                {"spec_info": {"表带": "野径回环表带"}, "price": 6499, "original_price": 6999, "stock": 80},
            ]
        },
        {
            "category_id": 5, "name": "小米手表S3", 
            "cover": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400&h=400&fit=crop"],
            "description": "eSIM独立通话，运动健康", "base_price": 999, "sales": 4567,
            "skus": [
                {"spec_info": {"颜色": "黑色"}, "price": 999, "original_price": 1199, "stock": 300},
                {"spec_info": {"颜色": "银色"}, "price": 999, "original_price": 1199, "stock": 250},
            ]
        },
        {
            "category_id": 5, "name": "OPPO Watch 4 Pro", 
            "cover": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop"],
            "description": "双擎混动，超长续航", "base_price": 2199, "sales": 1234,
            "skus": [
                {"spec_info": {"颜色": "铂黑"}, "price": 2199, "original_price": 2499, "stock": 150},
                {"spec_info": {"颜色": "羽金"}, "price": 2199, "original_price": 2499, "stock": 100},
            ]
        },
        # 配件 (category_id=6)
        {
            "category_id": 6, "name": "倍思100W氮化镓充电器", 
            "cover": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1568656012937-8982e65df4b4?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1587614382346-4ec70e388b28?w=400&h=400&fit=crop"],
            "description": "4口快充，小巧便携", "base_price": 199, "sales": 8765,
            "skus": [
                {"spec_info": {"功率": "100W"}, "price": 199, "original_price": 249, "stock": 500},
                {"spec_info": {"功率": "65W"}, "price": 149, "original_price": 179, "stock": 600},
            ]
        },
        {
            "category_id": 6, "name": "罗技MX Master 3S", 
            "cover": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop"],
            "description": "静音点击，8000DPI", "base_price": 799, "sales": 3456,
            "skus": [
                {"spec_info": {"颜色": "石墨黑"}, "price": 799, "original_price": 899, "stock": 200},
                {"spec_info": {"颜色": "珍珠白"}, "price": 799, "original_price": 899, "stock": 150},
            ]
        },
        {
            "category_id": 6, "name": "绿联Type-C扩展坞", 
            "cover": "https://images.unsplash.com/photo-1568656012937-8982e65df4b4?w=400&h=400&fit=crop",
            "images": ["https://images.unsplash.com/photo-1568656012937-8982e65df4b4?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1532339142463-fd0a8979791a?w=400&h=400&fit=crop", "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop"],
            "description": "10合1，4K HDMI", "base_price": 299, "sales": 5678,
            "skus": [
                {"spec_info": {"接口": "10合1"}, "price": 299, "original_price": 349, "stock": 400},
                {"spec_info": {"接口": "6合1"}, "price": 199, "original_price": 229, "stock": 500},
            ]
        },
    ]
    
    for p_data in products_data:
        skus_data = p_data.pop("skus")
        name = p_data["name"]
        exists = await Product.filter(name=name).exists()
        if not exists:
            product = await Product.create(**p_data)
            for sku in skus_data:
                await ProductSku.create(product_id=product.id, **sku)
    print("商品创建完成")
    
    # 创建轮播图
    banners = [
        {"image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=750&h=300&fit=crop", "link": "/pages/product/detail?id=1", "sort_order": 1},
        {"image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=750&h=300&fit=crop", "link": "/pages/product/detail?id=6", "sort_order": 2},
        {"image": "https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=750&h=300&fit=crop", "link": "/pages/product/detail?id=15", "sort_order": 3},
    ]
    for b in banners:
        exists = await Banner.filter(image=b["image"]).exists()
        if not exists:
            await Banner.create(**b)
    print("轮播图创建完成")
    
    # 创建优惠券
    now = datetime.now()
    coupons = [
        {"name": "新人专享券", "type": 1, "value": 50, "min_amount": 200, "start_time": now, "end_time": now + timedelta(days=30), "total": 1000, "remain": 1000},
        {"name": "满500减100", "type": 1, "value": 100, "min_amount": 500, "start_time": now, "end_time": now + timedelta(days=15), "total": 500, "remain": 500},
        {"name": "满1000减200", "type": 1, "value": 200, "min_amount": 1000, "start_time": now, "end_time": now + timedelta(days=10), "total": 300, "remain": 300},
        {"name": "9折券", "type": 2, "value": 0.9, "min_amount": 100, "start_time": now, "end_time": now + timedelta(days=7), "total": 200, "remain": 200},
    ]
    for c in coupons:
        exists = await Coupon.filter(name=c["name"]).exists()
        if not exists:
            await Coupon.create(**c)
    print("优惠券创建完成")
    
    await Tortoise.close_connections()
    print("初始化完成!")

if __name__ == "__main__":
    asyncio.run(init())
