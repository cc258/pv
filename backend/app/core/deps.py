import os
import jwt
from sqlmodel import Session, SQLModel, create_engine, select
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.core.config import settings
from app.core.security import ALGORITHM
from app.models.user import User

# 获取 app 目录的绝对路径
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(app_dir, "database.db")
sqlite_url = f"sqlite:///{db_path}"

engine = create_engine(sqlite_url, echo=True)

def get_db():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_db():
    SQLModel.metadata.drop_all(engine)

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1}/login/access-token")

sessionDEP = Annotated[Session, Depends(get_db)]
TokenDEP = Annotated[str, Depends(reusable_oauth2)]

async def get_current_user(token: TokenDEP, session: sessionDEP) -> User:
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
    
    user = session.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.status == 1:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

