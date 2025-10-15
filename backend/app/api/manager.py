from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os
import uuid
import shutil
from pathlib import Path

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User, UserRole
from app.models.training import TrainingMaterial, MaterialType, PracticeSession
from app.services.sync_service import SyncService
from app.models.sync import SyncLog, MaterialVersion

router = APIRouter()


# Pydantic模型
class ManagerStats(BaseModel):
    total_teachers: int
    completed_training: int
    in_progress_training: int
    pending_reviews: int


class TeacherInfo(BaseModel):
    id: int
    name: str
    email: str
    training_status: str
    training_progress: int
    created_at: str
    
    class Config:
        from_attributes = True


class ActivityInfo(BaseModel):
    id: int
    description: str
    time: str


class MaterialCreate(BaseModel):
    title: str
    description: str
    category: str = "教学文档"
    type: str
    status: str = "draft"


class MaterialResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    type: str
    status: str
    file_url: str
    file_size: str
    download_count: int
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


def verify_manager_role(current_user: User = Depends(get_current_user)):
    """验证管理员角色"""
    if current_user.role != UserRole.MANAGER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足：需要管理员角色"
        )
    return current_user


@router.get("/stats", response_model=ManagerStats)
async def get_manager_stats(
    current_user: User = Depends(verify_manager_role),
    db: Session = Depends(get_db)
):
    """获取管理员统计数据"""
    # TODO: 实现真实的统计查询
    # 目前返回模拟数据
    return ManagerStats(
        total_teachers=156,
        completed_training=89,
        in_progress_training=45,
        pending_reviews=12
    )


@router.get("/activities")
async def get_recent_activities(
    current_user: User = Depends(verify_manager_role),
    db: Session = Depends(get_db)
):
    """获取最近活动"""
    # TODO: 实现真实的活动查询
    # API占位符
    return {
        "activities": [
            {"id": 1, "description": "张老师完成了试讲练习", "time": "2小时前"},
            {"id": 2, "description": "李老师提交了讲座视频", "time": "4小时前"},
            {"id": 3, "description": "王老师开始了SOP学习", "time": "6小时前"}
        ]
    }


@router.get("/teachers", response_model=List[TeacherInfo])
async def get_teachers_list(
    current_user: User = Depends(verify_manager_role),
    db: Session = Depends(get_db)
):
    """获取教师列表"""
    # TODO: 实现教师列表查询
    teachers = db.query(User).filter(User.role == UserRole.TEACHER).all()
    
    return [
        TeacherInfo(
            id=teacher.id,
            name=teacher.name,
            email=teacher.email,
            training_status=teacher.training_status.value,
            training_progress=teacher.training_progress,
            created_at=teacher.created_at.isoformat() if teacher.created_at else ""
        )
        for teacher in teachers
    ]


@router.post("/teachers")
async def create_teacher(
    current_user: User = Depends(verify_manager_role),
    db: Session = Depends(get_db)
):
    """创建教师账户"""
    # TODO: 实现教师账户创建
    # API占位符
    return {"message": "教师账户创建功能开发中"}


@router.put("/teachers/{teacher_id}")
async def update_teacher(
    teacher_id: int,
    current_user: User = Depends(verify_manager_role),
    db: Session = Depends(get_db)
):
    """更新教师信息"""
    # TODO: 实现教师信息更新
    # API占位符
    return {"message": f"教师{teacher_id}信息更新功能开发中"}


@router.delete("/teachers/{teacher_id}")
async def delete_teacher(
    teacher_id: int,
    current_user: User = Depends(verify_manager_role),
    db: Session = Depends(get_db)
):
    """删除教师账户"""
    # TODO: 实现教师账户删除
    # API占位符
    return {"message": f"教师{teacher_id}账户删除功能开发中"}


@router.get("/lectures")
async def get_pending_lectures(
    current_user: User = Depends(verify_manager_role),
    db: Session = Depends(get_db)
):
    """获取待评审讲座"""
    # TODO: 实现待评审讲座查询
    # API占位符
    return {"message": "待评审讲座功能开发中", "lectures": []}


@router.post("/lectures/{lecture_id}/review")
async def review_lecture(
    lecture_id: int,
    current_user: User = Depends(verify_manager_role),
    db: Session = Depends(get_db)
):
    """提交讲座评审结果"""
    # TODO: 实现讲座评审
    # API占位符
    return {"message": f"讲座{lecture_id}评审功能开发中"}


@router.post("/ai/video-analysis")
async def analyze_video(
    current_user: User = Depends(verify_manager_role)
):
    """AI视频分析服务占位符"""
    # TODO: 集成AI视频分析服务
    return {"message": "AI视频分析功能开发中", "status": "placeholder"}


@router.post("/ai/auto-review")
async def auto_review(
    current_user: User = Depends(verify_manager_role)
):
    """AI自动评审服务占位符"""
    # TODO: 集成AI自动评审服务
    return {"message": "AI自动评审功能开发中", "status": "placeholder"}


@router.get("/materials", response_model=List[MaterialResponse])
async def get_materials_list(
    current_user: User = Depends(verify_manager_role),
    db: Session = Depends(get_db)
):
    """获取培训资料列表"""
    materials = db.query(TrainingMaterial).order_by(TrainingMaterial.created_at.desc()).all()
    
    return [
        MaterialResponse(
            id=material.id,
            title=material.title,
            description=material.description,
            category=material.category or "教学文档",
            type=material.type.value,
            status=material.status,
            file_url=material.file_url or "",
            file_size=material.file_size or "0 Bytes",
            download_count=material.download_count,
            created_at=material.created_at.isoformat(),
            updated_at=material.updated_at.isoformat() if material.updated_at else material.created_at.isoformat()
        )
        for material in materials
    ]


@router.post("/materials", response_model=MaterialResponse)
async def upload_material(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form("教学文档"),
    type: str = Form(...),
    status: str = Form("draft"),
    file: UploadFile = File(...),
    current_user: User = Depends(verify_manager_role),
    db: Session = Depends(get_db)
):
    """上传新的培训资料"""
    try:
        # 验证文件类型
        allowed_types = {
            'application/pdf': '.pdf',
            'application/msword': '.doc',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
            'application/vnd.ms-powerpoint': '.ppt',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
            'video/mp4': '.mp4',
            'video/avi': '.avi',
            'video/quicktime': '.mov',
            'video/x-ms-wmv': '.wmv',
            'audio/mpeg': '.mp3',
            'audio/mp3': '.mp3',
            'text/plain': '.txt'  # 添加文本文件支持
        }
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件类型: {file.content_type}"
            )
        
        # 验证文件大小 (100MB)
        max_size = 100 * 1024 * 1024
        if file.size and file.size > max_size:
            raise HTTPException(
                status_code=400,
                detail="文件大小不能超过 100MB"
            )
        
        # 创建上传目录
        upload_dir = Path("uploads/materials")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成唯一文件名
        file_extension = allowed_types[file.content_type]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = upload_dir / unique_filename
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 计算文件大小
        file_size_bytes = os.path.getsize(file_path)
        file_size_str = format_file_size(file_size_bytes)
        
        # 创建数据库记录
        from datetime import datetime
        
        # 将字符串类型转换为 MaterialType 枚举
        material_type = None
        if type.lower() == "video":
            material_type = MaterialType.VIDEO
        elif type.lower() == "document":
            material_type = MaterialType.DOCUMENT
        elif type.lower() == "audio":
            material_type = MaterialType.AUDIO
        elif type.lower() == "interactive":
            material_type = MaterialType.INTERACTIVE
        else:
            material_type = MaterialType.DOCUMENT  # 默认为文档类型
        
        material = TrainingMaterial(
            title=title,
            description=description,
            category=category,
            type=material_type,
            status=status,
            file_url=f"/uploads/materials/{unique_filename}",
            file_path=str(file_path),  # 存储本地文件路径
            file_size=file_size_str,
            download_count=0
        )
        
        db.add(material)
        db.commit()
        db.refresh(material)
        
        return MaterialResponse(
            id=material.id,
            title=material.title,
            description=material.description,
            category=material.category,
            type=material.type.value,  # 转换枚举为字符串
            status=material.status,
            file_url=material.file_url,
            file_size=material.file_size,
            download_count=material.download_count,
            created_at=material.created_at.isoformat(),
            updated_at=material.updated_at.isoformat() if material.updated_at else material.created_at.isoformat()
        )
        
    except Exception as e:
        # 打印详细错误信息到日志
        import traceback
        print(f"文件上传错误: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        
        # 如果出错，删除已上传的文件
        if 'file_path' in locals() and file_path.exists():
            file_path.unlink()
        raise HTTPException(
            status_code=500,
            detail=f"文件上传失败: {str(e)}"
        )


@router.delete("/materials/{material_id}")
async def delete_material(
    material_id: int,
    current_user: User = Depends(verify_manager_role),
    db: Session = Depends(get_db)
):
    """删除培训资料"""
    material = db.query(TrainingMaterial).filter(TrainingMaterial.id == material_id).first()
    
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="资料不存在"
        )
    
    # 删除文件
    if material.file_url:
        file_path = Path("uploads") / "materials" / Path(material.file_url).name
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception as e:
                print(f"删除文件失败: {e}")
    
    # 删除数据库记录
    db.delete(material)
    db.commit()
    
    return {"message": "资料删除成功"}


def format_file_size(bytes_size: int) -> str:
    """格式化文件大小"""
    if bytes_size == 0:
        return "0 Bytes"
    
    k = 1024
    sizes = ["Bytes", "KB", "MB", "GB"]
    i = 0
    
    while bytes_size >= k and i < len(sizes) - 1:
        bytes_size /= k
        i += 1
    
    return f"{bytes_size:.2f} {sizes[i]}"


@router.get("/analytics/overview")
async def get_analytics_overview(
    current_user: User = Depends(verify_manager_role),
    db: Session = Depends(get_db)
):
    """获取数据分析概览"""
    # TODO: 实现数据分析
    # API占位符
    return {"message": "数据分析功能开发中", "data": {}}


# 同步相关API
class SyncRequest(BaseModel):
    material_ids: List[int] = None  # 如果为空则同步所有资料
    target_teacher_ids: List[int] = None  # 如果为空则同步给所有教师


class SyncLogResponse(BaseModel):
    id: int
    operation: str
    status: str
    description: str
    material_id: Optional[int] = None
    batch_id: Optional[str] = None
    error_message: Optional[str] = None
    created_at: str
    
    class Config:
        from_attributes = True


@router.post("/sync/materials")
async def sync_materials_to_teachers(
    sync_request: SyncRequest,
    current_user: User = Depends(verify_manager_role),
    db: Session = Depends(get_db)
):
    """将培训资料同步给教师"""
    sync_service = SyncService(db)
    
    try:
        if sync_request.material_ids:
            # 同步指定资料
            results = []
            for material_id in sync_request.material_ids:
                success = sync_service.sync_material_to_teachers(
                    material_id, 
                    current_user, 
                    sync_request.target_teacher_ids
                )
                results.append({
                    "material_id": material_id,
                    "success": success
                })
            
            return {
                "success": True,
                "message": f"同步完成，共处理 {len(sync_request.material_ids)} 个资料",
                "results": results
            }
        else:
            # 同步所有资料
            result = sync_service.sync_all_materials_to_teachers(
                current_user, 
                sync_request.target_teacher_ids
            )
            return result
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"同步失败: {str(e)}"
        )


@router.get("/sync/logs", response_model=List[SyncLogResponse])
async def get_sync_logs(
    material_id: int = None,
    limit: int = 50,
    current_user: User = Depends(verify_manager_role),
    db: Session = Depends(get_db)
):
    """获取同步操作日志"""
    sync_service = SyncService(db)
    logs = sync_service.get_sync_logs(
        user_id=current_user.id,
        material_id=material_id,
        limit=limit
    )
    
    return [
        SyncLogResponse(
            id=log.id,
            operation=log.operation.value,
            status=log.status.value,
            description=log.description,
            material_id=log.material_id,
            batch_id=log.batch_id,
            error_message=log.error_message,
            created_at=log.created_at.isoformat()
        )
        for log in logs
    ]


@router.get("/materials/{material_id}/versions")
async def get_material_versions(
    material_id: int,
    current_user: User = Depends(verify_manager_role),
    db: Session = Depends(get_db)
):
    """获取培训资料版本历史"""
    sync_service = SyncService(db)
    versions = sync_service.get_material_versions(material_id)
    
    return [
        {
            "id": version.id,
            "version": version.version,
            "title": version.title,
            "description": version.description,
            "change_description": version.change_description,
            "is_current": version.is_current,
            "created_at": version.created_at.isoformat(),
            "created_by": version.created_by
        }
        for version in versions
    ]


@router.post("/sync/clear-virtual-materials")
async def clear_virtual_materials(
    current_user: User = Depends(verify_manager_role),
    db: Session = Depends(get_db)
):
    """清理教师账户中的虚拟学习资料"""
    sync_service = SyncService(db)
    
    # 获取所有教师
    teachers = db.query(User).filter(User.role == UserRole.TEACHER).all()
    
    results = []
    for teacher in teachers:
        result = sync_service.delete_virtual_materials_for_teacher(
            teacher.id, 
            current_user
        )
        results.append({
            "teacher_id": teacher.id,
            "teacher_name": teacher.name,
            "result": result
        })
    
    return {
        "success": True,
        "message": f"已清理 {len(teachers)} 位教师的虚拟资料",
        "results": results
    }