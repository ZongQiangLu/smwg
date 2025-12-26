from fastapi import APIRouter, Depends, Query
from datetime import datetime
import uuid
from app.models import Order, OrderItem, OrderLogistics, Cart, ProductSku, Product, Address, UserCoupon, User
from app.schemas import OrderCreate
from app.utils import success, error, get_current_user

router = APIRouter()

@router.get("")
async def get_orders(
    status: int = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    user: User = Depends(get_current_user)
):
    query = Order.filter(user_id=user.id)
    if status is not None:
        query = query.filter(status=status)
    
    total = await query.count()
    orders = await query.order_by("-created_at").offset((page - 1) * size).limit(size)
    
    items = []
    for o in orders:
        order_items = await OrderItem.filter(order_id=o.id)
        items.append({
            "id": o.id,
            "order_no": o.order_no,
            "total_amount": float(o.total_amount),
            "pay_amount": float(o.pay_amount),
            "status": o.status,
            "created_at": o.created_at.isoformat(),
            "item_count": len(order_items),
            "first_item_image": order_items[0].product_image if order_items else None
        })
    
    return success({"total": total, "items": items})

@router.post("")
async def create_order(data: OrderCreate, user: User = Depends(get_current_user)):
    address = await Address.get_or_none(id=data.address_id, user_id=user.id)
    if not address:
        return error("收货地址不存在")
    
    total_amount = 0
    order_items = []
    
    for item in data.items:
        sku = await ProductSku.get_or_none(id=item.sku_id)
        if not sku or sku.stock < item.quantity:
            return error(f"商品库存不足")
        
        product = await Product.get(id=sku.product_id)
        total_amount += float(sku.price) * item.quantity
        order_items.append({
            "sku": sku,
            "product": product,
            "quantity": item.quantity,
            "price": sku.price
        })
    
    # 优惠券处理
    discount = 0
    user_coupon = None
    if data.coupon_id:
        user_coupon = await UserCoupon.get_or_none(id=data.coupon_id, user_id=user.id, status=0)
        if user_coupon:
            coupon = await user_coupon.coupon
            if total_amount >= float(coupon.min_amount):
                if coupon.type == 1:  # 满减
                    discount = float(coupon.value)
                else:  # 折扣
                    discount = total_amount * (1 - float(coupon.value))
    
    pay_amount = max(0, total_amount - discount)
    
    # 创建订单
    order = await Order.create(
        order_no=str(uuid.uuid4()).replace("-", "")[:20],
        user_id=user.id,
        total_amount=total_amount,
        pay_amount=pay_amount,
        coupon_id=user_coupon.id if user_coupon else None,
        address_snapshot={
            "name": address.name,
            "phone": address.phone,
            "address": f"{address.province}{address.city}{address.district}{address.detail}"
        },
        remark=data.remark
    )
    
    # 创建订单项并扣减库存
    for item in order_items:
        await OrderItem.create(
            order_id=order.id,
            sku_id=item["sku"].id,
            product_name=item["product"].name,
            product_image=item["sku"].image or item["product"].cover,
            spec_info=item["sku"].spec_info,
            quantity=item["quantity"],
            price=item["price"]
        )
        item["sku"].stock -= item["quantity"]
        await item["sku"].save()
    
    # 更新优惠券状态
    if user_coupon:
        user_coupon.status = 1
        user_coupon.used_time = datetime.now()
        await user_coupon.save()
    
    # 清空购物车中已下单的商品
    sku_ids = [item.sku_id for item in data.items]
    await Cart.filter(user_id=user.id, sku_id__in=sku_ids).delete()
    
    return success({"id": order.id, "order_no": order.order_no})

@router.get("/{order_id}")
async def get_order_detail(order_id: int, user: User = Depends(get_current_user)):
    order = await Order.get_or_none(id=order_id, user_id=user.id)
    if not order:
        return error("订单不存在")
    
    items = await OrderItem.filter(order_id=order.id)
    logistics = await OrderLogistics.get_or_none(order_id=order.id)
    
    return success({
        "id": order.id,
        "order_no": order.order_no,
        "total_amount": float(order.total_amount),
        "pay_amount": float(order.pay_amount),
        "status": order.status,
        "address_snapshot": order.address_snapshot,
        "remark": order.remark,
        "created_at": order.created_at.isoformat(),
        "items": [{
            "id": i.id,
            "product_name": i.product_name,
            "product_image": i.product_image,
            "spec_info": i.spec_info,
            "quantity": i.quantity,
            "price": float(i.price),
            "is_reviewed": i.is_reviewed
        } for i in items],
        "logistics": {
            "company": logistics.company,
            "tracking_no": logistics.tracking_no,
            "status": logistics.status,
            "traces": logistics.traces
        } if logistics else None
    })

@router.put("/{order_id}/cancel")
async def cancel_order(order_id: int, user: User = Depends(get_current_user)):
    order = await Order.get_or_none(id=order_id, user_id=user.id)
    if not order:
        return error("订单不存在")
    if order.status != 0:
        return error("只能取消待付款订单")
    
    order.status = 5
    await order.save()
    
    # 恢复库存
    items = await OrderItem.filter(order_id=order.id)
    for item in items:
        sku = await ProductSku.get(id=item.sku_id)
        sku.stock += item.quantity
        await sku.save()
    
    return success()

@router.put("/{order_id}/pay")
async def pay_order(order_id: int, user: User = Depends(get_current_user)):
    order = await Order.get_or_none(id=order_id, user_id=user.id)
    if not order:
        return error("订单不存在")
    if order.status != 0:
        return error("只能支付待付款订单")
    
    order.status = 1  # 待发货
    order.pay_time = datetime.now()
    await order.save()
    
    return success()

@router.put("/{order_id}/confirm")
async def confirm_order(order_id: int, user: User = Depends(get_current_user)):
    order = await Order.get_or_none(id=order_id, user_id=user.id)
    if not order:
        return error("订单不存在")
    if order.status != 2:
        return error("只能确认待收货订单")
    
    order.status = 3  # 待评价
    await order.save()
    
    # 更新销量
    items = await OrderItem.filter(order_id=order.id)
    for item in items:
        sku = await ProductSku.get(id=item.sku_id)
        product = await Product.get(id=sku.product_id)
        product.sales += item.quantity
        await product.save()
    
    return success()

@router.get("/{order_id}/logistics")
async def get_logistics(order_id: int, user: User = Depends(get_current_user)):
    order = await Order.get_or_none(id=order_id, user_id=user.id)
    if not order:
        return error("订单不存在")
    
    logistics = await OrderLogistics.get_or_none(order_id=order.id)
    if not logistics:
        return success(None, "暂无物流信息")
    
    return success({
        "company": logistics.company,
        "tracking_no": logistics.tracking_no,
        "status": logistics.status,
        "traces": logistics.traces
    })
