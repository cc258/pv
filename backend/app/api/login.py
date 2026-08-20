import uuid
from datetime import timedelta
from fastapi import Depends, APIRouter, Request, Query, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated, List

from backend.app.core.deps import sessionDEP
from backend.app.models.login import LoginRequest, RegRequest, Token
from backend.app.core.security import create_access_token, get_password_hash
from backend.app.core.config import settings
from backend.app import crud
from backend.app.models.user import User, UserCreate


router = APIRouter(prefix="/login", tags=["login"])


@router.post("/reg", response_model=None)
def register(session: sessionDEP, user_create: UserCreate,):
    # Pydantic UserCreate → ORM User：排除 password（它会变成 hashed_password）
    create_data = user_create.model_dump(exclude={"password"})
    db_user = User(**create_data, hashed_password=get_password_hash(user_create.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {
        "id": db_user.id,
        "username": db_user.username,
        "gender": db_user.gender,
        "status": db_user.status,
        "email": db_user.email,
        "created_at": db_user.created_at,
        "updated_at": db_user.updated_at,
    }


# 登录，重新发一个Token
@router.post("")
def login(session: sessionDEP, form_data: LoginRequest,) -> Token:
    user = crud.authenticate(
        session=session, username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    elif not user.status == 1:
        raise HTTPException(status_code=401, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
