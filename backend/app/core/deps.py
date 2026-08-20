import os
import jwt
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, DeclarativeBase

from backend.app.core.config import settings
from backend.app.core.security import ALGORITHM

# 本地开发：backend/app/database.db（相对于项目根目录）
# Docker容器内：/app/backend/app/database.db
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(app_dir, "database.db")

sqlite_url = f"sqlite:///{db_path}"

engine = create_engine(
    sqlite_url,
    echo=True,
    connect_args={"check_same_thread": False},  # SQLite 多线程支持
)


class Base(DeclarativeBase):
    pass


def get_db():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1}/login/access-token")

sessionDEP = Annotated[Session, Depends(get_db)]
TokenDEP = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(token: TokenDEP, session: sessionDEP):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    from backend.app.models.user import User
    user = session.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.status == 1:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
