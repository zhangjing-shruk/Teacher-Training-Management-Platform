from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User, UserRole
from app.models.training import TrainingMaterial, PracticeSession, Feedback

router = APIRouter()


# Pydantic模型
class TrainingMaterialResponse(BaseModel):
    id: int
    title: str
    description: str
    type: str
    category: str = None
    duration_minutes: int
    file_url: str = None
    file_path: str = None
    file_size: str = None
    download_count: int = 0
    
    class Config:
        from_attributes = True


class PracticeSessionResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    overall_score: float = None
    created_at: str
    
    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    materials_completed: int
    practice_sessions: int
    current_status: str
    progress_percentage: int


def verify_teacher_role(current_user: User = Depends(get_current_user)):
    """验证教师角色"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足：需要教师角色"
        )
    return current_user


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(verify_teacher_role),
    db: Session = Depends(get_db)
):
    """获取教师仪表板统计数据"""
    # TODO: 实现真实的统计逻辑
    # 这里返回模拟数据
    return DashboardStats(
        materials_completed=8,
        practice_sessions=3,
        current_status=current_user.training_status.value,
        progress_percentage=current_user.training_progress
    )


@router.get("/materials", response_model=List[TrainingMaterialResponse])
async def get_training_materials(
    current_user: User = Depends(verify_teacher_role),
    db: Session = Depends(get_db)
):
    """获取培训资料列表"""
    # 查询所有已发布的培训资料
    materials = db.query(TrainingMaterial).filter(
        TrainingMaterial.status == "published"
    ).order_by(TrainingMaterial.order_index, TrainingMaterial.created_at).all()
    
    return [
        TrainingMaterialResponse(
            id=material.id,
            title=material.title,
            description=material.description,
            type=material.type.value,
            category=material.category,
            duration_minutes=material.duration_minutes or 0,
            file_url=material.file_url,
            file_path=material.file_path,
            file_size=material.file_size,
            download_count=material.download_count or 0
        )
        for material in materials
    ]


@router.get("/practice-sessions", response_model=List[PracticeSessionResponse])
async def get_practice_sessions(
    current_user: User = Depends(verify_teacher_role),
    db: Session = Depends(get_db)
):
    """获取试讲练习记录"""
    # TODO: 实现真实的数据查询
    sessions = db.query(PracticeSession).filter(
        PracticeSession.user_id == current_user.id
    ).all()
    
    return [
        PracticeSessionResponse(
            id=session.id,
            title=session.title,
            description=session.description,
            status=session.status.value,
            overall_score=session.overall_score,
            created_at=session.created_at.isoformat() if session.created_at else ""
        )
        for session in sessions
    ]


@router.post("/practice/start")
async def start_practice_session(
    current_user: User = Depends(verify_teacher_role),
    db: Session = Depends(get_db)
):
    """开始试讲练习"""
    # TODO: 实现试讲练习开始逻辑
    # API占位符
    return {"message": "试讲练习已开始", "session_id": "placeholder"}


@router.post("/ai/speech-analysis")
async def analyze_speech(
    current_user: User = Depends(verify_teacher_role)
):
    """AI语音分析服务占位符"""
    # TODO: 集成AI语音分析服务
    return {"message": "AI语音分析功能开发中", "status": "placeholder"}


@router.post("/ai/feedback")
async def generate_ai_feedback(
    current_user: User = Depends(verify_teacher_role)
):
    """AI反馈生成服务占位符"""
    # TODO: 集成AI反馈生成服务
    return {"message": "AI反馈生成功能开发中", "status": "placeholder"}


@router.get("/sop")
async def get_sop_documents(
    current_user: User = Depends(verify_teacher_role)
):
    """获取SOP流程文档"""
    # TODO: 实现SOP文档获取
    # API占位符
    return {"message": "SOP文档功能开发中", "documents": []}


@router.get("/feedback/reports")
async def get_feedback_reports(
    current_user: User = Depends(verify_teacher_role),
    db: Session = Depends(get_db)
):
    """获取反馈报告列表"""
    # TODO: 实现反馈报告查询
    # API占位符
    return {"message": "反馈报告功能开发中", "reports": []}