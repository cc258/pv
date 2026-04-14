import jwt
from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from backend.app.core.config import settings


sqlite_file_name = "apis/database.db"
sqlite_url = settings.DATABASE

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

