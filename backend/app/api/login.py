import uuid
from datetime import timedelta
from fastapi import Depends, APIRouter, Request, Query, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Annotated, List

from backend.app.core.deps import sessionDEP
from backend.app.models.login import LoginRequest, Token
from backend.app.core.security import create_access_token
from backend.app.core.config import settings
from backend.app import crud


router = APIRouter(prefix="/login", tags=["login"])

@router.post("")
def login(session: sessionDEP, form_data: LoginRequest,) -> Token:
    user = crud.authenticate(
        session=session, username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
