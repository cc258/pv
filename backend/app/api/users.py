import uuid
from fastapi import Depends, APIRouter, Request, Query, APIRouter, Security, HTTPException
from sqlmodel import Session, select

from backend.app.core.deps import sessionDEP
from backend.app.models.models import User, UserBase, UserCreate, UserUpdate, UserInfo, UserInfoAll, Roles, RoleBase, RoleCreate, RoleUpdate, RoleInfo, RoleInfoAll

from backend.app.core.config import settings
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


# add user
@router.post("", response_model=UserInfo)
def create_user(*, session: sessionDEP, user: UserCreate):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# 获取所有用户
@router.get("", response_model=list[UserInfo])
def get_user_list(*, session: sessionDEP, offset: int = 0, limit: int = 100):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

# 获取指定用户
@router.get("/{user_id}", response_model=UserInfoAll)
def get_user(*, session: sessionDEP, user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



