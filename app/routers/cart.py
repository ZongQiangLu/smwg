from fastapi import APIRouter, Depends
from app.models import Cart, ProductSku, Product, User
from app.schemas import CartAdd, CartUpdate
from app.utils import success, error, get_current_user

router = APIRouter()

@router.get("")
async def get_cart(user: User = Depends(get_current_user)):
    carts = await Cart.filter(user_id=user.id).prefetch_related("sku", "sku__product")
    items = []
    for c in carts:
        sku = c.sku
        product = await Product.get(id=sku.product_id)
        items.append({
            "id": c.id,
            "sku_id": sku.id,
            "product_id": product.id,
            "product_name": product.name,
            "product_image": sku.image or product.cover,
            "spec_info": sku.spec_info,
            "price": float(sku.price),
            "stock": sku.stock,
            "quantity": c.quantity,
            "selected": c.selected
        })
    return success(items)

@router.post("")
async def add_to_cart(data: CartAdd, user: User = Depends(get_current_user)):
    sku = await ProductSku.get_or_none(id=data.sku_id)
    if not sku:
        return error("商品规格不存在")
    
    cart = await Cart.get_or_none(user_id=user.id, sku_id=data.sku_id)
    if cart:
        cart.quantity += data.quantity
        await cart.save()
    else:
        cart = await Cart.create(user_id=user.id, sku_id=data.sku_id, quantity=data.quantity)
    
    return success({"id": cart.id})

@router.put("/{cart_id}")
async def update_cart(cart_id: int, data: CartUpdate, user: User = Depends(get_current_user)):
    cart = await Cart.get_or_none(id=cart_id, user_id=user.id)
    if not cart:
        return error("购物车项不存在")
    
    if data.quantity is not None:
        cart.quantity = data.quantity
    if data.selected is not None:
        cart.selected = data.selected
    await cart.save()
    return success()

@router.put("/select-all")
async def select_all(selected: bool, user: User = Depends(get_current_user)):
    await Cart.filter(user_id=user.id).update(selected=selected)
    return success()

@router.delete("/{cart_id}")
async def delete_cart(cart_id: int, user: User = Depends(get_current_user)):
    await Cart.filter(id=cart_id, user_id=user.id).delete()
    return success()
