from fastapi import APIRouter
from apis.api import users, video

router = APIRouter()

router.include_router(users.router, tags=["users"])
router.include_router(video.router, tags=["video"])
# router.include_router(role.router, prefix="/admin", tags=["role"])
# router.include_router(access.router, prefix="/admin", tags=["access"])
# router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
