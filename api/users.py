import uuid
from fastapi import Depends, APIRouter, Request, Query, APIRouter, Security
from sqlalchemy.orm import Session

from db.database import get_db
from models.models import UserModel
from schemas.schemas import UserSchema

from core.config import settings
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

# 获取所有用户
@router.get("", response_model=List[UserSchema])
def get_user(db: Session = Depends(get_db)):
    users = db.query(UserModel)
    return users

# 获取指定用户
@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    return user


