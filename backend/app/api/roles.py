from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

from backend.app.core.deps import get_db, get_current_user
from backend.app.models.user import User, Role, Permission, RolePermission

router = APIRouter(prefix="/roles", tags=["role"])

@router.get("/permissions")
async def get_roles_permissions(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """获取所有角色和权限数据"""
    roles = session.execute(select(Role)).scalars().all()
    permissions = session.execute(select(Permission)).scalars().all()

    result = []
    for role in roles:
        role_data = {
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "permissions": [
                {"id": p.id, "code": p.code, "description": p.description}
                for p in role.permissions
            ],
        }
        result.append(role_data)

    return {
        "roles": result,
        "permissions": [
            {"id": p.id, "code": p.code, "description": p.description}
            for p in permissions
        ],
    }


@router.post("/{role_id}/permissions/{permission_id}")
async def toggle_role_permission(
    role_id: int,
    permission_id: int,
    action: str = Query(..., description="add or remove"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """添加或移除角色权限"""
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    permission = session.get(Permission, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="权限不存在")

    if action == "add":
        existing = session.execute(
            select(RolePermission).where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id,
            )
        ).scalars().first()
        if not existing:
            role_permission = RolePermission(
                role_id=role_id,
                permission_id=permission_id,
            )
            session.add(role_permission)
            session.commit()

    elif action == "remove":
        role_permission = session.execute(
            select(RolePermission).where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id,
            )
        ).scalars().first()
        if role_permission:
            session.delete(role_permission)
            session.commit()

    return {"message": "操作成功"}
