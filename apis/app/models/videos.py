import uuid
from datetime import datetime, timezone
from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel

class VideoBase(SQLModel):
    video_name: str = Field(default=None, nullable=False)
    link: str = Field(default=None)
    year: int = Field(default=None)
    cover: str = Field(default=None)

    tags: str = Field(default=None)
    categories: str = Field(default=None, description="分类")
    stars: int = Field(default=1, gt=0, le=5, description="评分（1-5分）")
    comment: str = Field(default=None)


class VideoCreate(VideoBase):
    pass

class Video(VideoBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class VideoPublic(VideoBase):
    id: uuid.UUID

class VideoUpdate(VideoBase):
    pass

