from fastapi import APIRouter
from backend.app.api import login, users, video, roles

router = APIRouter()

router.include_router(login.router, tags=["login"])
router.include_router(users.router, tags=["user"])
router.include_router(video.router, tags=["video"])
router.include_router(roles.router, tags=["role"])
