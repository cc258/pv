from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
import uuid

from backend.app.core.deps import get_db, get_current_user
from backend.app.models.user import User
from backend.app.models.videos import Category, VideoCategory, Video

router = APIRouter(prefix="/categories", tags=["category"])


@router.get("")
async def get_categories(
    session: Session = Depends(get_db),
):
    """获取所有分类"""
    return session.execute(select(Category)).scalars().all()


@router.post("")
async def create_category(
    name: str,
    description: str = "",
    session: Session = Depends(get_db),
):
    """创建分类"""
    existing = session.execute(select(Category).where(Category.name == name)).scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="分类已存在")

    category = Category(name=name, description=description)
    session.add(category)
    session.commit()
    session.refresh(category)
    return {"id": category.id, "name": category.name, "description": category.description}


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    session: Session = Depends(get_db),
):
    """删除分类"""
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")

    session.delete(category)
    session.commit()
    return {"message": "删除成功"}


@router.get("/{category_id}/videos")
async def get_videos_by_category(
    category_id: int,
    session: Session = Depends(get_db),
):
    """获取某分类下的所有视频"""
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")

    videos = category.videos
    return videos


@router.post("/{category_id}/videos/{video_id}")
async def add_video_to_category(
    category_id: int,
    video_id: str,
    session: Session = Depends(get_db),
):
    """将视频添加到分类"""
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")

    video = session.get(Video, uuid.UUID(video_id))
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")

    existing = session.execute(
        select(VideoCategory).where(
            VideoCategory.video_id == video.id,
            VideoCategory.category_id == category_id,
        )
    ).scalars().first()

    if existing:
        return {"message": "视频已在该分类中"}

    video_category = VideoCategory(video_id=video.id, category_id=category_id)
    session.add(video_category)
    session.commit()
    return {"message": "添加成功"}


@router.delete("/{category_id}/videos/{video_id}")
async def remove_video_from_category(
    category_id: int,
    video_id: str,
    session: Session = Depends(get_db),
):
    """将视频从分类移除"""
    import uuid
    video_category = session.execute(
        select(VideoCategory).where(
            VideoCategory.video_id == uuid.UUID(video_id),
            VideoCategory.category_id == category_id,
        )
    ).scalars().first()

    if not video_category:
        raise HTTPException(status_code=404, detail="视频不在该分类中")

    session.delete(video_category)
    session.commit()
    return {"message": "移除成功"}
