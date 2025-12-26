from fastapi import APIRouter, Depends, Query
from datetime import datetime
from app.models import Coupon, UserCoupon, User
from app.utils import success, error, get_current_user

router = APIRouter()

@router.get("/available")
async def get_available_coupons(user: User = Depends(get_current_user)):
    now = datetime.now()
    coupons = await Coupon.filter(
        start_time__lte=now,
        end_time__gte=now,
        remain__gt=0
    )
    
    # 过滤已领取的
    user_coupon_ids = await UserCoupon.filter(user_id=user.id).values_list("coupon_id", flat=True)
    
    items = [{
        "id": c.id,
        "name": c.name,
        "type": c.type,
        "value": float(c.value),
        "min_amount": float(c.min_amount),
        "start_time": c.start_time.isoformat(),
        "end_time": c.end_time.isoformat(),
        "remain": c.remain,
        "claimed": c.id in user_coupon_ids
    } for c in coupons]
    
    return success(items)

@router.get("/mine")
async def get_my_coupons(
    status: int = Query(None),
    user: User = Depends(get_current_user)
):
    query = UserCoupon.filter(user_id=user.id)
    if status is not None:
        query = query.filter(status=status)
    
    user_coupons = await query.prefetch_related("coupon")
    
    items = [{
        "id": uc.id,
        "coupon_id": uc.coupon.id,
        "name": uc.coupon.name,
        "type": uc.coupon.type,
        "value": float(uc.coupon.value),
        "min_amount": float(uc.coupon.min_amount),
        "end_time": uc.coupon.end_time.isoformat(),
        "status": uc.status
    } for uc in user_coupons]
    
    return success(items)

@router.post("/{coupon_id}/claim")
async def claim_coupon(coupon_id: int, user: User = Depends(get_current_user)):
    coupon = await Coupon.get_or_none(id=coupon_id)
    if not coupon:
        return error("优惠券不存在")
    
    now = datetime.now()
    if now < coupon.start_time or now > coupon.end_time:
        return error("优惠券不在有效期内")
    
    if coupon.remain <= 0:
        return error("优惠券已领完")
    
    exists = await UserCoupon.filter(user_id=user.id, coupon_id=coupon_id).exists()
    if exists:
        return error("已领取过该优惠券")
    
    await UserCoupon.create(user_id=user.id, coupon_id=coupon_id)
    coupon.remain -= 1
    await coupon.save()
    
    return success()

@router.get("/usable")
async def get_usable_coupons(
    amount: float = Query(..., gt=0),
    user: User = Depends(get_current_user)
):
    now = datetime.now()
    user_coupons = await UserCoupon.filter(
        user_id=user.id,
        status=0
    ).prefetch_related("coupon")
    
    items = []
    for uc in user_coupons:
        coupon = uc.coupon
        if coupon.end_time >= now and float(coupon.min_amount) <= amount:
            items.append({
                "id": uc.id,
                "coupon_id": coupon.id,
                "name": coupon.name,
                "type": coupon.type,
                "value": float(coupon.value),
                "min_amount": float(coupon.min_amount),
                "end_time": coupon.end_time.isoformat()
            })
    
    return success(items)
