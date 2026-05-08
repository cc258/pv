import uuid
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select, func, delete
from sqlalchemy.orm import selectinload

from backend.app.core.deps import get_db, get_current_user
from backend.app.models.videos import Video, VideoCategory
from backend.app.models.user import User

router = APIRouter(prefix="/video", tags=["video"])


@router.get("")
async def get_video_list(
        category_id: int = Query(None, description="分类ID"),
        name: str = Query(None),
        tags: str = Query(None),
        page: int = Query(default=1, ge=1, description="页码"),
        size: int = Query(default=10, ge=0, description="每页显示数目"),
        session: Session = Depends(get_db),
):
    query = select(Video).options(selectinload(Video.categories))
    count_query = select(func.count(Video.id))

    if name:
        query = query.where(Video.video_name.like(f"%{name.strip()}%"))
        count_query = count_query.where(Video.video_name.like(f"%{name.strip()}%"))
    if tags and tags.strip():
        query = query.where(Video.tags.like(f"%{tags.strip()}%"))
        count_query = count_query.where(Video.tags.like(f"%{tags.strip()}%"))
    if category_id:
        subquery = select(VideoCategory.video_id).where(VideoCategory.category_id == category_id).subquery()
        query = query.where(Video.id.in_(subquery))
        count_query = count_query.where(Video.id.in_(subquery))

    total = session.scalar(count_query)
    videos = session.exec(query.offset((page - 1) * size).limit(size)).all()

    result = []
    for v in videos:
        result.append({
            "id": str(v.id),
            "video_name": v.video_name,
            "link": v.link,
            "year": v.year,
            "cover": v.cover,
            "tags": v.tags,
            "comment": v.comment,
            "stars": v.stars,
            "created_at": v.created_at,
            "categories": [{"id": c.id, "name": c.name, "description": c.description} for c in v.categories]
        })

    return {"data": result, "total": total, "page": page, "size": size}


@router.get("/{video_id}")
async def get_video(
    video_id: uuid.UUID,
    session: Session = Depends(get_db),
):
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="video not found")
    
    return {
        "id": str(video.id),
        "video_name": video.video_name,
        "link": video.link,
        "year": video.year,
        "cover": video.cover,
        "tags": video.tags,
        "comment": video.comment,
        "stars": video.stars,
        "categories": [{"id": c.id, "name": c.name} for c in video.categories],
    }


@router.post("")
async def post_video(
    video_in: dict,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category_ids = video_in.pop("category_ids", [])
    video = Video.model_validate(video_in)
    session.add(video)
    session.commit()
    session.refresh(video)

    for cat_id in category_ids:
        session.add(VideoCategory(video_id=video.id, category_id=cat_id))
    session.commit()

    return {"id": str(video.id), "video_name": video.video_name}


@router.delete("/{video_id}")
async def del_video(
    video_id: uuid.UUID,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    session.exec(delete(VideoCategory).where(VideoCategory.video_id == video_id))
    session.delete(video)
    session.commit()
    return {"message": "deleted"}


@router.put("/{video_id}")
async def put_video(
    video_id: uuid.UUID,
    video_in: dict,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    category_ids = video_in.pop("category_ids", None)
    video.sqlmodel_update(video_in)

    if category_ids is not None:
        session.exec(delete(VideoCategory).where(VideoCategory.video_id == video_id))
        for cat_id in category_ids:
            session.add(VideoCategory(video_id=video.id, category_id=cat_id))

    session.add(video)
    session.commit()
    session.refresh(video)
    return {"id": str(video.id), "video_name": video.video_name}
