import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from apis.app.core.deps import sessionDEP
from apis.app.models.models import Message
from apis.app.models.videos import Video, VideoPublic, VideoCreate, VideoUpdate

router = APIRouter(prefix="/video", tags=["video"])


# 获取 Video列表
@router.get("", response_model=list[VideoPublic])
async def get_video_list(session: sessionDEP, skip: int = 0, pagesize: int = 10):
    video_list = session.exec(select(Video).offset(skip).limit(pagesize)).all()
    return video_list

# 获取单个 Video
@router.get("/{video_id}", response_model=VideoPublic)
async def get_video(video_id: uuid.UUID, session: sessionDEP):
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="video not found")
    return video


# 创建 Video
@router.post("", response_model=VideoPublic)
async def post_video(*, session: sessionDEP, video_in: VideoCreate):
    video = Video.model_validate(video_in)
    session.add(video)
    session.commit()
    session.refresh(video)
    return video

# 删除 Video
@router.delete("/{video_id}", response_model=Message)
async def del_video(*, session: sessionDEP, video_id: uuid.UUID):
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    session.delete(video)
    session.commit()
    return Message(message="Item deleted successfully")


# 更新 Video
@router.put("/{video_id}", response_model=VideoPublic)
async def put_video(*, session: sessionDEP, video_id: uuid.UUID, video_in: VideoUpdate):
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    video_dict = video_in.model_dump(exclude_unset=True)
    print(video_dict)
    video.sqlmodel_update(video_dict)
    session.add(video)
    session.commit()
    return video
