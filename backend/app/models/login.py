from datetime import datetime, UTC
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: str
    password: str

class RegRequest(BaseModel):
    username: str
    password: str
