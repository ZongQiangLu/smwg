from fastapi import APIRouter, Depends
from app.models import Address, User
from app.schemas import AddressCreate
from app.utils import success, error, get_current_user

router = APIRouter()

@router.get("")
async def get_addresses(user: User = Depends(get_current_user)):
    addresses = await Address.filter(user_id=user.id).order_by("-is_default", "-id")
    items = [{
        "id": a.id,
        "name": a.name,
        "phone": a.phone,
        "province": a.province,
        "city": a.city,
        "district": a.district,
        "detail": a.detail,
        "is_default": a.is_default
    } for a in addresses]
    return success(items)

@router.post("")
async def create_address(data: AddressCreate, user: User = Depends(get_current_user)):
    if data.is_default:
        await Address.filter(user_id=user.id).update(is_default=False)
    
    address = await Address.create(user_id=user.id, **data.model_dump())
    return success({"id": address.id})

@router.put("/{address_id}")
async def update_address(address_id: int, data: AddressCreate, user: User = Depends(get_current_user)):
    address = await Address.get_or_none(id=address_id, user_id=user.id)
    if not address:
        return error("地址不存在")
    
    if data.is_default:
        await Address.filter(user_id=user.id).update(is_default=False)
    
    await Address.filter(id=address_id).update(**data.model_dump())
    return success()

@router.delete("/{address_id}")
async def delete_address(address_id: int, user: User = Depends(get_current_user)):
    await Address.filter(id=address_id, user_id=user.id).delete()
    return success()

@router.put("/{address_id}/default")
async def set_default(address_id: int, user: User = Depends(get_current_user)):
    address = await Address.get_or_none(id=address_id, user_id=user.id)
    if not address:
        return error("地址不存在")
    
    await Address.filter(user_id=user.id).update(is_default=False)
    address.is_default = True
    await address.save()
    return success()
