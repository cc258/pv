import uuid
from datetime import datetime, UTC
from pydantic import EmailStr, ConfigDict
from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List


class VideoCategory(SQLModel, table=True):
    """视频-分类关联表"""
    __tablename__ = "video_category"

    video_id: uuid.UUID = Field(
        foreign_key="video.id",
        primary_key=True
    )
    category_id: int = Field(
        foreign_key="category.id",
        primary_key=True
    )


class Category(SQLModel, table=True):
    """视频分类"""
    __tablename__ = "category"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: str = Field(default="")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    videos: List["Video"] = Relationship(
        back_populates="categories",
        link_model=VideoCategory
    )


class VideoBase(SQLModel):
    video_name: str
    link: Optional[str] = None
    year: Optional[int] = None
    cover: Optional[str] = None
    tags: Optional[str] = None
    comment: Optional[str] = None
    stars: int = 1

    class Config:
        extra = "allow"


class VideoCreate(VideoBase):
    category_ids: Optional[List[int]] = []


class Video(VideoBase, table=True):
    __tablename__ = "video"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    categories: List["Category"] = Relationship(
        back_populates="videos",
        link_model=VideoCategory
    )


class VideoPublic(VideoBase):
    id: uuid.UUID
    categories: List[dict] = []


class VideoUpdate(VideoBase):
    category_ids: Optional[List[int]] = None
