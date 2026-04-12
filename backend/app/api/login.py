import uuid
from fastapi import Depends, APIRouter, Request, Query, APIRouter, Security, HTTPException
from sqlmodel import Session, select
from typing import List

from backend.app.core.deps import sessionDEP
from backend.app.models.models import Message, User, UserBase, UserCreate, UserUpdate, UserInfo, UserInfoAll, Roles, RoleBase, RoleCreate, RoleUpdate, RoleInfo, RoleInfoAll

from backend.app.core.config import settings


router = APIRouter(prefix="/login", tags=["login"])

@router.post("")
def login():
    return {"message": "success", "status": "ok"}
