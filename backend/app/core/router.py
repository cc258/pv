from fastapi import APIRouter
from backend.app.api import login, users, video

router = APIRouter()

router.include_router(login.router, tags=["login"])
router.include_router(users.router, tags=["user"])
router.include_router(video.router, tags=["video"])

# router.include_router(role.router, prefix="/admin", tags=["role"])
# router.include_router(access.router, prefix="/admin", tags=["access"])
# router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
