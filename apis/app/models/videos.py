import uuid
from datetime import datetime, timezone
from pydantic import EmailStr, ConfigDict
from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel
from typing import Optional

class VideoBase(SQLModel):
    video_name: str
    link: Optional[str] = None
    year: Optional[int] = None
    cover: Optional[str] = None
    tags: Optional[str] = None
    categories: Optional[str] = None
    comment: Optional[str] = None
    stars: int = 1

    class Config:
        extra = "allow"


class VideoCreate(VideoBase):
    pass

class Video(VideoBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class VideoPublic(VideoBase):
    id: uuid.UUID

class VideoUpdate(VideoBase):
    pass

