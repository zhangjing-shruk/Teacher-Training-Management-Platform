from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from pydantic import BaseModel
from datetime import datetime, timezone

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.learning_progress import LearningProgress
from app.models.training import TrainingMaterial

router = APIRouter()


class LearningProgressCreate(BaseModel):
    material_id: int


class LearningProgressUpdate(BaseModel):
    total_study_seconds: int
    is_completed: Optional[bool] = None


class LearningProgressResponse(BaseModel):
    id: int
    material_id: int
    total_study_seconds: int
    is_completed: bool
    progress_percentage: int
    start_time: Optional[datetime]
    completion_time: Optional[datetime]
    
    class Config:
        from_attributes = True


@router.post("/start", response_model=LearningProgressResponse)
async def start_learning(
    request: LearningProgressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """开始学习资料"""
    # 检查资料是否存在
    material = db.query(TrainingMaterial).filter(TrainingMaterial.id == request.material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="培训资料不存在")
    
    # 检查是否已有学习记录
    existing_progress = db.query(LearningProgress).filter(
        and_(
            LearningProgress.user_id == current_user.id,
            LearningProgress.material_id == request.material_id
        )
    ).first()
    
    if existing_progress:
        # 更新开始时间和最后活跃时间
        existing_progress.start_time = datetime.now(timezone.utc)
        existing_progress.last_active_time = datetime.now(timezone.utc)
        existing_progress.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(existing_progress)
        
        # 计算进度百分比
        progress_percentage = min(100, int((existing_progress.total_study_seconds / (15 * 60)) * 100))
        
        return LearningProgressResponse(
            id=existing_progress.id,
            material_id=existing_progress.material_id,
            total_study_seconds=existing_progress.total_study_seconds,
            is_completed=existing_progress.is_completed,
            progress_percentage=progress_percentage,
            start_time=existing_progress.start_time,
            completion_time=existing_progress.completion_time
        )
    
    # 创建新的学习记录
    progress = LearningProgress(
        user_id=current_user.id,
        material_id=request.material_id,
        start_time=datetime.now(timezone.utc),
        last_active_time=datetime.now(timezone.utc)
    )
    
    db.add(progress)
    db.commit()
    db.refresh(progress)
    
    return LearningProgressResponse(
        id=progress.id,
        material_id=progress.material_id,
        total_study_seconds=progress.total_study_seconds,
        is_completed=progress.is_completed,
        progress_percentage=0,
        start_time=progress.start_time,
        completion_time=progress.completion_time
    )


@router.put("/{progress_id}", response_model=LearningProgressResponse)
async def update_learning_progress(
    progress_id: int,
    request: LearningProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新学习进度"""
    progress = db.query(LearningProgress).filter(
        and_(
            LearningProgress.id == progress_id,
            LearningProgress.user_id == current_user.id
        )
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="学习记录不存在")
    
    # 更新学习时长
    progress.total_study_seconds = request.total_study_seconds
    progress.last_active_time = datetime.now(timezone.utc)
    progress.updated_at = datetime.now(timezone.utc)
    
    # 检查是否完成（15分钟 = 900秒）
    if request.total_study_seconds >= 15 * 60:
        progress.is_completed = True
        if not progress.completion_time:
            progress.completion_time = datetime.now(timezone.utc)
    elif request.is_completed is not None:
        progress.is_completed = request.is_completed
        if request.is_completed and not progress.completion_time:
            progress.completion_time = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(progress)
    
    # 计算进度百分比
    progress_percentage = min(100, int((progress.total_study_seconds / (15 * 60)) * 100))
    
    return LearningProgressResponse(
        id=progress.id,
        material_id=progress.material_id,
        total_study_seconds=progress.total_study_seconds,
        is_completed=progress.is_completed,
        progress_percentage=progress_percentage,
        start_time=progress.start_time,
        completion_time=progress.completion_time
    )


@router.get("/material/{material_id}", response_model=Optional[LearningProgressResponse])
async def get_material_progress(
    material_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取特定资料的学习进度"""
    progress = db.query(LearningProgress).filter(
        and_(
            LearningProgress.user_id == current_user.id,
            LearningProgress.material_id == material_id
        )
    ).first()
    
    if not progress:
        return None
    
    # 计算进度百分比
    progress_percentage = min(100, int((progress.total_study_seconds / (15 * 60)) * 100))
    
    return LearningProgressResponse(
        id=progress.id,
        material_id=progress.material_id,
        total_study_seconds=progress.total_study_seconds,
        is_completed=progress.is_completed,
        progress_percentage=progress_percentage,
        start_time=progress.start_time,
        completion_time=progress.completion_time
    )


@router.get("/", response_model=List[LearningProgressResponse])
async def get_all_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户所有学习进度"""
    progress_list = db.query(LearningProgress).filter(
        LearningProgress.user_id == current_user.id
    ).all()
    
    result = []
    for progress in progress_list:
        # 计算进度百分比
        progress_percentage = min(100, int((progress.total_study_seconds / (15 * 60)) * 100))
        
        result.append(LearningProgressResponse(
            id=progress.id,
            material_id=progress.material_id,
            total_study_seconds=progress.total_study_seconds,
            is_completed=progress.is_completed,
            progress_percentage=progress_percentage,
            start_time=progress.start_time,
            completion_time=progress.completion_time
        ))
    
    return result