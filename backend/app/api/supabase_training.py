from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.services.supabase_training_service import SupabaseTrainingService
from app.api.supabase_auth import get_current_user

router = APIRouter()

# 初始化服务
training_service = SupabaseTrainingService()

# Pydantic模型
class TrainingMaterialResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    type: str
    category: str
    content_url: Optional[str]
    thumbnail_url: Optional[str]
    duration_minutes: Optional[int]
    difficulty_level: str
    order_index: int
    status: str
    download_count: int
    created_at: datetime
    updated_at: datetime

class TrainingMaterialCreate(BaseModel):
    title: str
    description: Optional[str] = None
    type: str  # video, document, audio, interactive
    category: str
    content_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration_minutes: Optional[int] = None
    difficulty_level: str = "beginner"
    order_index: int = 0
    status: str = "active"

class TrainingMaterialUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    content_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration_minutes: Optional[int] = None
    difficulty_level: Optional[str] = None
    order_index: Optional[int] = None
    status: Optional[str] = None

class LearningProgressResponse(BaseModel):
    id: int
    user_id: int
    material_id: int
    start_time: Optional[datetime]
    last_active_time: Optional[datetime]
    total_study_seconds: int
    is_completed: bool
    completion_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    training_materials: Optional[TrainingMaterialResponse] = None

class LearningProgressUpdate(BaseModel):
    study_seconds: int

class MaterialStatistics(BaseModel):
    total_learners: int
    completed_learners: int
    completion_rate: float
    average_study_time_seconds: int

# ==================== 培训资料管理 ====================

@router.get("/materials", response_model=List[TrainingMaterialResponse])
async def get_training_materials(
    status: Optional[str] = Query(None, description="资料状态筛选"),
    category: Optional[str] = Query(None, description="资料分类筛选"),
    limit: int = Query(100, ge=1, le=500, description="返回数量限制"),
    offset: int = Query(0, ge=0, description="偏移量"),
    current_user: dict = Depends(get_current_user)
):
    """获取培训资料列表"""
    try:
        materials = await training_service.get_training_materials(
            status=status,
            category=category,
            limit=limit,
            offset=offset
        )
        
        return [
            TrainingMaterialResponse(
                id=material["id"],
                title=material["title"],
                description=material.get("description"),
                type=material["type"],
                category=material["category"],
                content_url=material.get("content_url"),
                thumbnail_url=material.get("thumbnail_url"),
                duration_minutes=material.get("duration_minutes"),
                difficulty_level=material["difficulty_level"],
                order_index=material["order_index"],
                status=material["status"],
                download_count=material.get("download_count", 0),
                created_at=material["created_at"],
                updated_at=material["updated_at"]
            )
            for material in materials
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取培训资料失败: {str(e)}"
        )

@router.get("/materials/{material_id}", response_model=TrainingMaterialResponse)
async def get_training_material(
    material_id: int,
    current_user: dict = Depends(get_current_user)
):
    """获取单个培训资料"""
    try:
        material = await training_service.get_training_material_by_id(material_id)
        if not material:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="培训资料不存在"
            )
        
        return TrainingMaterialResponse(
            id=material["id"],
            title=material["title"],
            description=material.get("description"),
            type=material["type"],
            category=material["category"],
            content_url=material.get("content_url"),
            thumbnail_url=material.get("thumbnail_url"),
            duration_minutes=material.get("duration_minutes"),
            difficulty_level=material["difficulty_level"],
            order_index=material["order_index"],
            status=material["status"],
            download_count=material.get("download_count", 0),
            created_at=material["created_at"],
            updated_at=material["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取培训资料失败: {str(e)}"
        )

@router.post("/materials", response_model=TrainingMaterialResponse)
async def create_training_material(
    material_data: TrainingMaterialCreate,
    current_user: dict = Depends(get_current_user)
):
    """创建培训资料（管理员功能）"""
    try:
        material = await training_service.create_training_material(
            material_data.dict(),
            current_user["role"]
        )
        
        return TrainingMaterialResponse(
            id=material["id"],
            title=material["title"],
            description=material.get("description"),
            type=material["type"],
            category=material["category"],
            content_url=material.get("content_url"),
            thumbnail_url=material.get("thumbnail_url"),
            duration_minutes=material.get("duration_minutes"),
            difficulty_level=material["difficulty_level"],
            order_index=material["order_index"],
            status=material["status"],
            download_count=material.get("download_count", 0),
            created_at=material["created_at"],
            updated_at=material["updated_at"]
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建培训资料失败: {str(e)}"
        )

@router.put("/materials/{material_id}", response_model=TrainingMaterialResponse)
async def update_training_material(
    material_id: int,
    update_data: TrainingMaterialUpdate,
    current_user: dict = Depends(get_current_user)
):
    """更新培训资料（管理员功能）"""
    try:
        # 过滤掉None值
        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        
        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="没有提供更新数据"
            )
        
        success = await training_service.update_training_material(
            material_id,
            update_dict,
            current_user["role"]
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="培训资料不存在"
            )
        
        # 获取更新后的资料
        material = await training_service.get_training_material_by_id(material_id)
        
        return TrainingMaterialResponse(
            id=material["id"],
            title=material["title"],
            description=material.get("description"),
            type=material["type"],
            category=material["category"],
            content_url=material.get("content_url"),
            thumbnail_url=material.get("thumbnail_url"),
            duration_minutes=material.get("duration_minutes"),
            difficulty_level=material["difficulty_level"],
            order_index=material["order_index"],
            status=material["status"],
            download_count=material.get("download_count", 0),
            created_at=material["created_at"],
            updated_at=material["updated_at"]
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新培训资料失败: {str(e)}"
        )

@router.delete("/materials/{material_id}")
async def delete_training_material(
    material_id: int,
    current_user: dict = Depends(get_current_user)
):
    """删除培训资料（管理员功能）"""
    try:
        success = await training_service.delete_training_material(
            material_id,
            current_user["role"]
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="培训资料不存在"
            )
        
        return {"message": "培训资料删除成功"}
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除培训资料失败: {str(e)}"
        )

@router.post("/materials/{material_id}/download")
async def download_material(
    material_id: int,
    current_user: dict = Depends(get_current_user)
):
    """下载培训资料（增加下载次数）"""
    try:
        success = await training_service.increment_download_count(material_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="培训资料不存在"
            )
        
        return {"message": "下载记录成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"记录下载失败: {str(e)}"
        )

@router.get("/materials/{material_id}/statistics", response_model=MaterialStatistics)
async def get_material_statistics(
    material_id: int,
    current_user: dict = Depends(get_current_user)
):
    """获取资料学习统计（管理员功能）"""
    if current_user["role"] != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    try:
        stats = await training_service.get_material_learning_statistics(material_id)
        
        return MaterialStatistics(
            total_learners=stats["total_learners"],
            completed_learners=stats["completed_learners"],
            completion_rate=stats["completion_rate"],
            average_study_time_seconds=stats["average_study_time_seconds"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取统计数据失败: {str(e)}"
        )

# ==================== 学习进度管理 ====================

@router.post("/materials/{material_id}/start-learning", response_model=LearningProgressResponse)
async def start_learning(
    material_id: int,
    current_user: dict = Depends(get_current_user)
):
    """开始学习资料"""
    try:
        progress = await training_service.start_learning(current_user["id"], material_id)
        
        return LearningProgressResponse(
            id=progress["id"],
            user_id=progress["user_id"],
            material_id=progress["material_id"],
            start_time=progress.get("start_time"),
            last_active_time=progress.get("last_active_time"),
            total_study_seconds=progress["total_study_seconds"],
            is_completed=progress["is_completed"],
            completion_time=progress.get("completion_time"),
            created_at=progress["created_at"],
            updated_at=progress["updated_at"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"开始学习失败: {str(e)}"
        )

@router.put("/materials/{material_id}/update-progress")
async def update_learning_progress(
    material_id: int,
    progress_data: LearningProgressUpdate,
    current_user: dict = Depends(get_current_user)
):
    """更新学习进度"""
    try:
        success = await training_service.update_learning_progress(
            current_user["id"],
            material_id,
            progress_data.study_seconds
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="学习记录不存在"
            )
        
        return {"message": "学习进度更新成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新学习进度失败: {str(e)}"
        )

@router.post("/materials/{material_id}/complete")
async def complete_learning(
    material_id: int,
    current_user: dict = Depends(get_current_user)
):
    """完成学习"""
    try:
        success = await training_service.complete_learning(current_user["id"], material_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="学习记录不存在"
            )
        
        return {"message": "学习完成"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"完成学习失败: {str(e)}"
        )

@router.get("/my-progress", response_model=List[LearningProgressResponse])
async def get_my_learning_progress(current_user: dict = Depends(get_current_user)):
    """获取我的学习进度"""
    try:
        progress_list = await training_service.get_user_learning_progress(current_user["id"])
        
        return [
            LearningProgressResponse(
                id=progress["id"],
                user_id=progress["user_id"],
                material_id=progress["material_id"],
                start_time=progress.get("start_time"),
                last_active_time=progress.get("last_active_time"),
                total_study_seconds=progress["total_study_seconds"],
                is_completed=progress["is_completed"],
                completion_time=progress.get("completion_time"),
                created_at=progress["created_at"],
                updated_at=progress["updated_at"],
                training_materials=TrainingMaterialResponse(
                    **progress["training_materials"]
                ) if progress.get("training_materials") else None
            )
            for progress in progress_list
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取学习进度失败: {str(e)}"
        )