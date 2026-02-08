from datetime import datetime, UTC
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

class UserBase(SQLModel):

    user_type: str = Field(max_length=64)
    status: int = Field(default=0, description="0: 未启用，1:正常，2:禁止")

    username: str = Field(default=None, nullable=False, max_length=20)
    password: str = Field(default=None, nullable=False)
    gender: int = Field(default=0, description="0: 未知，1:男，2:女")
    # age: int = Field(default=0)

    email: EmailStr = Field(default=None, max_length=255)
    # created_timestamp: datetime = Field(default_factory=lambda : datetime.now(UTC))
    # updated_timestamp: datetime = Field(default_factory=lambda : datetime.now(UTC))



class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    # role_id: list[int] = Relationship(back_populates="roles")

class UserCreate(UserBase):
    pass

class UserInfo(UserBase):
    id: int

class UserUpdate(UserBase):
    # role_id: int
    pass

class UserInfoAll(UserBase):
    # role_id: int
    pass

class RoleBase(SQLModel):
    name: str = Field(max_length=20)
    permissions: str = Field(max_length=20)
    description: str = Field(max_length=255)

class Roles(RoleBase, table=True):
    id: int = Field(default=None, primary_key=True)

class RoleCreate(RoleBase):
    pass

class RoleInfo(RoleBase):
    id: int

class RoleUpdate(RoleBase):
    pass

class RoleInfoAll(RoleBase):
    pass