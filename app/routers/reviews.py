from fastapi import APIRouter, Depends
from app.models import Review, OrderItem, Order, User
from app.schemas import ReviewCreate
from app.utils import success, error, get_current_user

router = APIRouter()

@router.post("")
async def create_review(data: ReviewCreate, user: User = Depends(get_current_user)):
    order_item = await OrderItem.get_or_none(id=data.order_item_id)
    if not order_item:
        return error("订单项不存在")
    
    order = await Order.get(id=order_item.order_id)
    if order.user_id != user.id:
        return error("无权评价")
    
    if order.status != 3:
        return error("订单状态不允许评价")
    
    if order_item.is_reviewed:
        return error("已评价过")
    
    sku = await order_item.sku
    
    await Review.create(
        user_id=user.id,
        product_id=sku.product_id,
        order_id=order.id,
        order_item_id=order_item.id,
        rating=data.rating,
        content=data.content,
        images=data.images
    )
    
    order_item.is_reviewed = True
    await order_item.save()
    
    # 检查是否所有订单项都已评价
    all_reviewed = not await OrderItem.filter(order_id=order.id, is_reviewed=False).exists()
    if all_reviewed:
        order.status = 4  # 已完成
        await order.save()
    
    return success()
