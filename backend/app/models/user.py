from datetime import datetime, UTC
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict, Field

from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.deps import Base


# ============== Pydantic Schemas ==============

class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=128)
    gender: int = 0
    status: int = 1
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=1, max_length=50)
    gender: Optional[int] = None
    status: Optional[int] = None
    password: Optional[str] = Field(None, min_length=1, max_length=128)


class UserResponse(BaseModel):
    id: int
    username: str
    gender: int
    status: int
    email: Optional[EmailStr] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============== ORM Models ==============

class UserRole(Base):
    __tablename__ = "user_role"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("role.id", ondelete="CASCADE"),
        primary_key=True,
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class RolePermission(Base):
    __tablename__ = "role_permission"

    role_id: Mapped[int] = mapped_column(
        ForeignKey("role.id", ondelete="CASCADE"),
        primary_key=True,
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permission.id", ondelete="CASCADE"),
        primary_key=True,
    )


class Permission(Base):
    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255), default="")

    roles: Mapped[List["Role"]] = relationship(
        secondary="role_permission",
        back_populates="permissions",
    )


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(String(255), default="")

    users: Mapped[List["User"]] = relationship(
        secondary="user_role",
        back_populates="roles",
    )
    permissions: Mapped[List["Permission"]] = relationship(
        secondary="role_permission",
        back_populates="roles",
    )


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    gender: Mapped[int] = mapped_column(Integer, default=0, doc="0: 未知，1:男，2:女")
    status: Mapped[int] = mapped_column(Integer, default=1, doc="0: 未启用，1:正常，2:禁止")
    email: Mapped[Optional[str]] = mapped_column(String(254), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    roles: Mapped[List["Role"]] = relationship(
        secondary="user_role",
        back_populates="users",
    )
