import uuid
import httpx
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select

from backend.app.core.config import settings
from backend.app.core.deps import sessionDEP
from backend.app.models.models import Message
from backend.app.models.videos import Video, VideoPublic, VideoCreate, VideoUpdate

router = APIRouter(prefix="/video", tags=["video"])

# 构建请求头
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_TOKEN}"
}


# 第三方数据
@router.get("/popular")
async def get_video_popular():
    """获取热门电影"""
    # 不能使用，需要VPN
    try:
        # httpx 的异步客户端
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{settings.TMDB_BASE}/movie/popular",
                params={
                    "api_key": settings.TMDB_KEY,
                    "language": "zh-CN"
                },
                timeout=30.0
            )

            if resp.status_code != 200:
                raise HTTPException(
                    status_code=resp.status_code,
                    detail=f"TMDB API error: {resp.text}"
                )

            data = resp.json()
            return data.get("results", [])[:10]

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="TMDB API timeout")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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
    print("--------------", page, size)
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
    print("前端传的数据：", video_id, video_in.model_dump())
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    video_dict = video_in.model_dump(exclude_unset=True)
    video.sqlmodel_update(video_dict)
    session.add(video)
    session.commit()
    return video
