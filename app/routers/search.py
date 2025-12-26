from fastapi import APIRouter, Depends
from app.models import SearchHistory, User
from app.utils import success, get_current_user

router = APIRouter()

@router.get("/history")
async def get_search_history(user: User = Depends(get_current_user)):
    histories = await SearchHistory.filter(user_id=user.id).order_by("-created_at").limit(20)
    # 去重
    seen = set()
    items = []
    for h in histories:
        if h.keyword not in seen:
            seen.add(h.keyword)
            items.append(h.keyword)
    return success(items[:10])

@router.post("/history")
async def add_search_history(keyword: str, user: User = Depends(get_current_user)):
    await SearchHistory.create(user_id=user.id, keyword=keyword)
    return success()

@router.delete("/history")
async def clear_search_history(user: User = Depends(get_current_user)):
    await SearchHistory.filter(user_id=user.id).delete()
    return success()
