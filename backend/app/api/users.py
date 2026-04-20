from fastapi import Depends, APIRouter, HTTPException
from typing import Dict, List

from backend.app.core.deps import sessionDEP, get_current_user
from backend.app.models.user import User

router = APIRouter(prefix="/user", tags=["user"])

# 新增用户


# 菜单权限
@router.get("/info")
async def get_user_info(current_user: User = Depends(get_current_user)):
    roles = [role.name for role in current_user.roles]
    
    permissions: Dict[str, List[str]] = {}

    if 'admin' in roles:
        for route in [
            'menu.dashboard.workplace',
            'menu.dashboard.monitor',
            'menu.visualization.dataAnalysis',
            'menu.visualization.multiDimensionDataAnalysis',
            'menu.list.searchTable',
            'menu.list.videoDetails',
            'menu.list.cardList',
            'menu.form.group',
            'menu.form.step',
            'menu.profile.basic',
            'menu.result.success',
            'menu.result.error',
            'menu.exception.403',
            'menu.exception.404',
            'menu.exception.500',
            'menu.user.info',
            'menu.user.setting',
            'menu.user.permission',
        ]:
            permissions[route] = ['*']
    else:
        for route in [
            'menu.dashboard.workplace',
            'menu.list.searchTable',
            'menu.list.videoDetails',
            'menu.list.cardList',
            'menu.profile.basic',
            'menu.result.success',
            'menu.result.error',
            'menu.exception.403',
            'menu.exception.404',
            'menu.exception.500',
            'menu.user.info',
            'menu.user.setting',
        ]:
            permissions[route] = ['read']
    
    return {
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'roles': roles,
        'permissions': permissions,
    }