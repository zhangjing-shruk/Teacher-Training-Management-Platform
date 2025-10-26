from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User, UserRole
from app.models.training import (
    TrainingMaterial, PracticeSession, Feedback, 
    PracticeMode, CourseTopic, EvaluationFocus
)

router = APIRouter()

# Response Models
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


class PracticeModeResponse(BaseModel):
    id: int
    name: str
    description: str
    duration_minutes: int
    difficulty_level: str
    
    class Config:
        from_attributes = True


class CourseTopicResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True


class EvaluationFocusResponse(BaseModel):
    id: int
    name: str
    description: str
    category: str
    weight: float
    criteria: str = None
    
    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    materials_completed: int
    practice_sessions: int
    current_status: str
    progress_percentage: int


def verify_teacher_role(current_user: User = Depends(get_current_user)):
    """验证用户是否为教师角色"""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有教师用户可以访问此功能"
        )
    return current_user


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(verify_teacher_role),
    db: Session = Depends(get_db)
):
    """获取教师仪表板统计数据"""
    # 获取已完成的培训材料数量
    materials_completed = db.query(TrainingMaterial).count()
    
    # 获取练习会话数量
    practice_sessions = db.query(PracticeSession).filter(
        PracticeSession.user_id == current_user.id
    ).count()
    
    return DashboardStats(
        materials_completed=materials_completed,
        practice_sessions=practice_sessions,
        current_status="正常",
        progress_percentage=75
    )


@router.get("/materials", response_model=List[TrainingMaterialResponse])
async def get_training_materials(
    current_user: User = Depends(verify_teacher_role),
    db: Session = Depends(get_db)
):
    """获取培训材料列表"""
    materials = db.query(TrainingMaterial).filter(
        TrainingMaterial.status == "published"
    ).order_by(TrainingMaterial.order_index).all()
    
    # 转换为响应格式
    result = []
    for material in materials:
        result.append(TrainingMaterialResponse(
            id=material.id,
            title=material.title,
            description=material.description or "",
            type=material.type.value if material.type else "document",
            category=material.category,
            duration_minutes=material.duration_minutes or 0,
            file_url=material.file_url,
            file_path=material.file_path,
            file_size=material.file_size,
            download_count=material.download_count
        ))
    
    return result


@router.get("/practice-sessions", response_model=List[PracticeSessionResponse])
async def get_practice_sessions(
    current_user: User = Depends(verify_teacher_role),
    db: Session = Depends(get_db)
):
    """获取练习会话列表"""
    sessions = db.query(PracticeSession).filter(
        PracticeSession.user_id == current_user.id
    ).order_by(PracticeSession.created_at.desc()).all()
    
    # 转换为响应格式
    result = []
    for session in sessions:
        result.append(PracticeSessionResponse(
            id=session.id,
            title=session.title,
            description=session.description or "",
            status=session.status.value if session.status else "pending",
            overall_score=session.overall_score,
            created_at=session.created_at.isoformat() if session.created_at else ""
        ))
    
    return result


@router.get("/practice-modes", response_model=List[PracticeModeResponse])
async def get_practice_modes(
    current_user: User = Depends(verify_teacher_role),
    db: Session = Depends(get_db)
):
    """获取练习模式列表"""
    modes = db.query(PracticeMode).filter(
        PracticeMode.is_active == True
    ).order_by(PracticeMode.order_index).all()
    
    return [PracticeModeResponse(
        id=mode.id,
        name=mode.name,
        description=mode.description or "",
        duration_minutes=mode.duration_minutes,
        difficulty_level=mode.difficulty_level
    ) for mode in modes]


@router.get("/course-topics", response_model=List[CourseTopicResponse])
async def get_course_topics(
    current_user: User = Depends(verify_teacher_role),
    db: Session = Depends(get_db)
):
    """获取课程主题列表"""
    topics = db.query(CourseTopic).all()
    
    return [CourseTopicResponse(
        id=topic.id,
        name=topic.name
    ) for topic in topics]


@router.get("/evaluation-focus", response_model=List[EvaluationFocusResponse])
async def get_evaluation_focus(
    current_user: User = Depends(verify_teacher_role),
    db: Session = Depends(get_db)
):
    """获取评估重点列表"""
    focus_items = db.query(EvaluationFocus).filter(
        EvaluationFocus.is_active == True
    ).order_by(EvaluationFocus.order_index).all()
    
    return [EvaluationFocusResponse(
        id=item.id,
        name=item.name,
        description=item.description or "",
        category=item.category or "",
        weight=item.weight,
        criteria=item.criteria
    ) for item in focus_items]


@router.get("/practice-history", response_model=List[PracticeSessionResponse])
async def get_practice_history(
    current_user: User = Depends(verify_teacher_role),
    db: Session = Depends(get_db)
):
    """获取练习历史数据"""
    # 获取用户的所有练习会话，按时间倒序
    sessions = db.query(PracticeSession).filter(
        PracticeSession.user_id == current_user.id
    ).order_by(PracticeSession.created_at.desc()).limit(50).all()
    
    return [PracticeSessionResponse(
        id=session.id,
        title=session.title,
        description=session.description or "",
        status=session.status.value if session.status else "pending",
        overall_score=session.overall_score,
        created_at=session.created_at.isoformat() if session.created_at else ""
    ) for session in sessions]


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
    audio_data: bytes = None,
    transcript: str = None,
    duration: float = None,
    current_user: User = Depends(verify_teacher_role)
):
    """AI语音分析服务"""
    try:
        from app.services.ai_service import SpeechAnalysisService
        
        speech_service = SpeechAnalysisService()
        
        # 如果没有提供音频数据，使用模拟数据
        if not audio_data:
            audio_data = b"mock_audio_data"
        
        # 如果没有提供转录文本，使用默认文本
        if not transcript:
            transcript = "这是一段示例教学内容，用于演示语音分析功能。"
        
        # 如果没有提供时长，使用默认值
        if not duration:
            duration = 60.0
        
        # 执行语音分析
        analysis_result = await speech_service.analyze_pronunciation(
            audio_data=audio_data,
            transcript=transcript,
            duration=duration
        )
        
        return {
            "status": "success",
            "analysis": analysis_result,
            "message": "语音分析完成"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"语音分析失败: {str(e)}",
            "analysis": None
        }


@router.post("/ai/content-analysis")
async def analyze_content(
    transcript: str = None,
    topic: str = None,
    current_user: User = Depends(verify_teacher_role)
):
    """AI内容分析服务"""
    try:
        from app.services.ai_service import ContentAnalysisService
        
        content_service = ContentAnalysisService()
        
        # 如果没有提供转录文本，使用默认文本
        if not transcript:
            transcript = "今天我们来学习数学中的函数概念。函数是数学中的重要概念，它描述了两个变量之间的对应关系。"
        
        # 执行内容分析
        analysis_result = await content_service.analyze_teaching_content(
            transcript=transcript,
            topic=topic
        )
        
        return {
            "status": "success",
            "analysis": analysis_result,
            "message": "内容分析完成"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"内容分析失败: {str(e)}",
            "analysis": None
        }


@router.post("/ai/video-analysis")
async def analyze_video(
    video_data: bytes = None,
    duration: float = None,
    current_user: User = Depends(verify_teacher_role)
):
    """AI视频分析服务"""
    try:
        from app.services.ai_service import VideoAnalysisService
        
        video_service = VideoAnalysisService()
        
        # 如果没有提供视频数据，使用模拟数据
        if not video_data:
            video_data = b"mock_video_data"
        
        # 如果没有提供时长，使用默认值
        if not duration:
            duration = 60.0
        
        # 执行视频分析
        analysis_result = await video_service.analyze_body_language(
            video_data=video_data,
            duration=duration
        )
        
        return {
            "status": "success",
            "analysis": analysis_result,
            "message": "视频分析完成"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"视频分析失败: {str(e)}",
            "analysis": None
        }


@router.post("/ai/comprehensive-analysis")
async def comprehensive_analysis(
    audio_data: bytes = None,
    video_data: bytes = None,
    transcript: str = None,
    topic: str = None,
    duration: float = None,
    current_user: User = Depends(verify_teacher_role)
):
    """AI综合分析服务"""
    try:
        from app.services.ai_service import SpeechAnalysisService, ContentAnalysisService, VideoAnalysisService
        
        # 初始化服务
        speech_service = SpeechAnalysisService()
        content_service = ContentAnalysisService()
        video_service = VideoAnalysisService()
        
        # 设置默认值
        if not audio_data:
            audio_data = b"mock_audio_data"
        if not video_data:
            video_data = b"mock_video_data"
        if not transcript:
            transcript = "这是一段示例教学内容，包含了完整的课程讲解和互动环节。"
        if not duration:
            duration = 120.0
        
        # 执行各项分析
        speech_analysis = await speech_service.analyze_pronunciation(
            audio_data=audio_data,
            transcript=transcript,
            duration=duration
        )
        
        content_analysis = await content_service.analyze_teaching_content(
            transcript=transcript,
            topic=topic
        )
        
        video_analysis = await video_service.analyze_body_language(
            video_data=video_data,
            duration=duration
        )
        
        # 生成综合反馈
        analysis_results = {
            "speech_analysis": speech_analysis,
            "content_analysis": content_analysis,
            "video_analysis": video_analysis
        }
        
        comprehensive_feedback = await content_service.generate_feedback(analysis_results)
        
        return {
            "status": "success",
            "speech_analysis": speech_analysis,
            "content_analysis": content_analysis,
            "video_analysis": video_analysis,
            "comprehensive_feedback": comprehensive_feedback,
            "message": "综合分析完成"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"综合分析失败: {str(e)}",
            "analysis": None
        }


@router.post("/ai/feedback")
async def generate_ai_feedback(
    analysis_results: dict = None,
    current_user: User = Depends(verify_teacher_role)
):
    """AI反馈生成服务"""
    try:
        from app.services.ai_service import ContentAnalysisService
        
        content_service = ContentAnalysisService()
        
        # 如果没有提供分析结果，使用模拟数据
        if not analysis_results:
            analysis_results = {
                "speech_analysis": {"overall_pronunciation_score": 82.5},
                "content_analysis": {"overall_content_score": 78.3},
                "video_analysis": {"overall_body_language_score": 85.1}
            }
        
        # 生成反馈
        feedback = await content_service.generate_feedback(analysis_results)
        
        return {
            "status": "success",
            "feedback": feedback,
            "message": "反馈生成完成"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"反馈生成失败: {str(e)}",
            "feedback": None
        }


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