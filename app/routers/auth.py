from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.models import User
from app.schemas import UserCreate, UserLogin, UserOut
from app.utils import hash_password, verify_password, create_access_token, get_current_user, success, error
from fastapi import Depends

router = APIRouter()

@router.post("/register")
async def register(data: UserCreate):
    if await User.filter(username=data.username).exists():
        return error("用户名已存在")
    user = await User.create(
        username=data.username,
        password_hash=hash_password(data.password),
        phone=data.phone
    )
    return success({"id": user.id, "username": user.username})

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(username=form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        return error("用户名或密码错误")
    token = create_access_token({"sub": str(user.id)})
    return success({"access_token": token, "token_type": "bearer"})

@router.get("/profile")
async def get_profile(user: User = Depends(get_current_user)):
    return success({
        "id": user.id,
        "username": user.username,
        "phone": user.phone,
        "avatar": user.avatar,
        "created_at": user.created_at.isoformat()
    })
