from datetime import datetime, UTC
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class UserBase(SQLModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(default=None, nullable=False)
    gender: int = Field(default=0, description="0: 未知，1:男，2:女")
    status: int = Field(default=0, description="0: 未启用，1:正常，2:禁止")
    email: EmailStr = Field(default=None, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=100)


class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    gender: Optional[int] = None
    status: Optional[int] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 中间表
class UserRole(SQLModel, table=True):
    user_id: int = Field(
        foreign_key="user.id",
        primary_key=True,
        ondelete="CASCADE"
    )
    role_id: int = Field(
        foreign_key="role.id",
        primary_key=True,
        ondelete="CASCADE"
    )
    assigned_at: datetime = Field(default_factory=datetime.utcnow)


class RolePermission(SQLModel, table=True):
    role_id: int = Field(
        foreign_key="role.id",
        primary_key=True,
        ondelete="CASCADE"
    )
    permission_id: int = Field(
        foreign_key="permission.id",
        primary_key=True,
        ondelete="CASCADE"
    )


class Permission(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True)
    description: str = Field(default="")

    roles: List["Role"] = Relationship(
        back_populates="permissions",
        link_model=RolePermission
    )


class Role(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: str = Field(default="")

    users: List["User"] = Relationship(
        back_populates="roles",
        link_model=UserRole
    )
    permissions: List["Permission"] = Relationship(
        back_populates="roles",
        link_model=RolePermission
    )


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    roles: List["Role"] = Relationship(back_populates="users", link_model=UserRole)
