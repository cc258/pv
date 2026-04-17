import uuid
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select

from app.core.config import settings
from app.core.deps import sessionDEP
from app.models.videos import Video, VideoPublic, VideoCreate, VideoUpdate

router = APIRouter(prefix="/video", tags=["video"])

# 获取 Video列表
@router.get("")
async def get_video_list(
        session: sessionDEP,
        name: str = Query(None),
        tags: str = Query(None),
        categories: str = Query(None),
        page: int = Query(default=1, ge=1, description="页码"),
        size: int = Query(default=10, ge=0, description="每页显示数目")
):
    query = session.query(Video)
    if name:
        query = query.filter(Video.video_name.like(f"%{name.strip()}%"))
    if tags and tags.strip():
        query = query.filter(Video.tags.like(f"%{tags.strip()}%"))
    if categories and categories.strip():
        query = query.filter(Video.categories.like(f"%{categories.strip()}%"))

    total = query.count()

    video_list = query.offset((page - 1) * size).limit(size).all()

    return {"data": video_list, "total": total, "page": page, "size": size}


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
@router.delete("/{video_id}")
async def del_video(*, session: sessionDEP, video_id: uuid.UUID):
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    session.delete(video)
    session.commit()
    return "Item deleted successfully"


# 更新 Video
@router.put("/{video_id}", response_model=VideoPublic)
async def put_video(*, session: sessionDEP, video_id: uuid.UUID, video_in: VideoUpdate):
    print("前端传的数据：", video_id, video_in.model_dump())
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    video_dict = video_in.model_dump(exclude_unset=True)
    video.sqlmodel_update(video_dict)
    session.add(video)
    session.commit()
    return video
