from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional, Any
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from app.core.config import settings

password_hash = PasswordHash((BcryptHasher(),))

ALGORITHM = "HS256"

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> tuple[bool, str | None]:
    return password_hash.verify_and_update(plain_password, hashed_password)

def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt