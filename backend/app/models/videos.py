import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field

from sqlalchemy import String, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.deps import Base


# ============== Pydantic Schemas ==============

class VideoBase(BaseModel):
    video_name: str = Field(..., max_length=255)
    link: Optional[str] = Field(None, max_length=1000)
    year: Optional[int] = None
    cover: Optional[str] = Field(None, max_length=1000)
    tags: Optional[str] = Field(None, max_length=500)
    comment: Optional[str] = Field(None, max_length=2000)
    stars: int = 1

    model_config = ConfigDict(extra="allow")


class VideoCreate(VideoBase):
    category_ids: Optional[List[int]] = []


class VideoUpdate(BaseModel):
    """部分更新：所有字段都可选，未传则不更新原 ORM 值"""
    video_name: Optional[str] = Field(None, max_length=255)
    link: Optional[str] = Field(None, max_length=1000)
    year: Optional[int] = None
    cover: Optional[str] = Field(None, max_length=1000)
    tags: Optional[str] = Field(None, max_length=500)
    comment: Optional[str] = Field(None, max_length=2000)
    stars: Optional[int] = None
    category_ids: Optional[List[int]] = None


class VideoPublic(VideoBase):
    id: uuid.UUID
    categories: List[dict] = []


# ============== ORM Models ==============

class VideoCategory(Base):
    """视频-分类关联表"""
    __tablename__ = "video_category"

    video_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("video.id"),
        primary_key=True,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"),
        primary_key=True,
    )


class Category(Base):
    """视频分类"""
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255), default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    videos: Mapped[List["Video"]] = relationship(
        secondary="video_category",
        back_populates="categories",
    )


class Video(Base):
    __tablename__ = "video"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    video_name: Mapped[str] = mapped_column(String(255), index=True)
    link: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    cover: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    stars: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    categories: Mapped[List["Category"]] = relationship(
        secondary="video_category",
        back_populates="videos",
    )
