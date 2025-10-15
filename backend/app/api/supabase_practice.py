from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.services.supabase_practice_service import SupabasePracticeService
from app.api.supabase_auth import get_current_user

router = APIRouter()

# 初始化服务
practice_service = SupabasePracticeService()

# Pydantic模型
class PracticeSessionResponse(BaseModel):
    id: int
    user_id: int
    material_id: int
    session_data: Optional[Dict[str, Any]]
    start_time: datetime
    end_time: Optional[datetime]
    score: Optional[float]
    status: str
    created_at: datetime
    updated_at: datetime
    training_materials: Optional[Dict[str, Any]] = None
    users: Optional[Dict[str, Any]] = None

class PracticeSessionCreate(BaseModel):
    material_id: int
    session_data: Optional[Dict[str, Any]] = None

class PracticeSessionUpdate(BaseModel):
    session_data: Optional[Dict[str, Any]] = None
    score: Optional[float] = None
    status: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    session_id: int
    feedback_type: str
    content: str
    score: Optional[float]
    created_at: datetime
    updated_at: datetime
    practice_sessions: Optional[Dict[str, Any]] = None

class FeedbackCreate(BaseModel):
    session_id: int
    feedback_type: str  # ai_generated, manual, peer_review
    content: str
    score: Optional[float] = None

class FeedbackUpdate(BaseModel):
    feedback_type: Optional[str] = None
    content: Optional[str] = None
    score: Optional[float] = None

class PracticeStatistics(BaseModel):
    total_sessions: int
    completed_sessions: int
    completion_rate: float
    average_score: float
    active_users: Optional[int] = None

# ==================== 练习会话管理 ====================

@router.post("/sessions", response_model=PracticeSessionResponse)
async def create_practice_session(
    session_data: PracticeSessionCreate,
    current_user: dict = Depends(get_current_user)
):
    """创建练习会话"""
    try:
        session_dict = {
            "user_id": current_user["id"],
            "material_id": session_data.material_id,
            "session_data": session_data.session_data,
            "start_time": "now()"
        }
        
        session = await practice_service.create_practice_session(session_dict)
        
        return PracticeSessionResponse(
            id=session["id"],
            user_id=session["user_id"],
            material_id=session["material_id"],
            session_data=session.get("session_data"),
            start_time=session["start_time"],
            end_time=session.get("end_time"),
            score=session.get("score"),
            status=session["status"],
            created_at=session["created_at"],
            updated_at=session["updated_at"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建练习会话失败: {str(e)}"
        )

@router.get("/sessions", response_model=List[PracticeSessionResponse])
async def get_my_practice_sessions(
    session_status: Optional[str] = Query(None, description="会话状态筛选"),
    limit: int = Query(50, ge=1, le=200, description="返回数量限制"),
    offset: int = Query(0, ge=0, description="偏移量"),
    current_user: dict = Depends(get_current_user)
):
    """获取我的练习会话"""
    try:
        sessions = await practice_service.get_practice_sessions_by_user(
            current_user["id"],
            status=session_status,
            limit=limit,
            offset=offset
        )
        
        return [
            PracticeSessionResponse(
                id=session["id"],
                user_id=session["user_id"],
                material_id=session["material_id"],
                session_data=session.get("session_data"),
                start_time=session["start_time"],
                end_time=session.get("end_time"),
                score=session.get("score"),
                status=session["status"],
                created_at=session["created_at"],
                updated_at=session["updated_at"],
                training_materials=session.get("training_materials")
            )
            for session in sessions
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取练习会话失败: {str(e)}"
        )

@router.get("/sessions/{session_id}", response_model=PracticeSessionResponse)
async def get_practice_session(
    session_id: int,
    current_user: dict = Depends(get_current_user)
):
    """获取单个练习会话"""
    try:
        # 如果是管理员，可以查看所有会话；否则只能查看自己的
        user_id = None if current_user["role"] == "manager" else current_user["id"]
        
        session = await practice_service.get_practice_session_by_id(session_id, user_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习会话不存在"
            )
        
        return PracticeSessionResponse(
            id=session["id"],
            user_id=session["user_id"],
            material_id=session["material_id"],
            session_data=session.get("session_data"),
            start_time=session["start_time"],
            end_time=session.get("end_time"),
            score=session.get("score"),
            status=session["status"],
            created_at=session["created_at"],
            updated_at=session["updated_at"],
            training_materials=session.get("training_materials"),
            users=session.get("users")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取练习会话失败: {str(e)}"
        )

@router.put("/sessions/{session_id}", response_model=PracticeSessionResponse)
async def update_practice_session(
    session_id: int,
    update_data: PracticeSessionUpdate,
    current_user: dict = Depends(get_current_user)
):
    """更新练习会话"""
    try:
        # 过滤掉None值
        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        
        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="没有提供更新数据"
            )
        
        # 如果是管理员，可以更新所有会话；否则只能更新自己的
        user_id = None if current_user["role"] == "manager" else current_user["id"]
        
        success = await practice_service.update_practice_session(
            session_id,
            update_dict,
            user_id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习会话不存在或无权限修改"
            )
        
        # 获取更新后的会话
        session = await practice_service.get_practice_session_by_id(session_id, user_id)
        
        return PracticeSessionResponse(
            id=session["id"],
            user_id=session["user_id"],
            material_id=session["material_id"],
            session_data=session.get("session_data"),
            start_time=session["start_time"],
            end_time=session.get("end_time"),
            score=session.get("score"),
            status=session["status"],
            created_at=session["created_at"],
            updated_at=session["updated_at"],
            training_materials=session.get("training_materials"),
            users=session.get("users")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新练习会话失败: {str(e)}"
        )

@router.post("/sessions/{session_id}/complete")
async def complete_practice_session(
    session_id: int,
    score: Optional[float] = Query(None, description="练习得分"),
    current_user: dict = Depends(get_current_user)
):
    """完成练习会话"""
    try:
        success = await practice_service.complete_practice_session(
            session_id,
            current_user["id"],
            score
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="练习会话不存在"
            )
        
        return {"message": "练习会话已完成"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"完成练习会话失败: {str(e)}"
        )

@router.get("/my-statistics", response_model=PracticeStatistics)
async def get_my_practice_statistics(current_user: dict = Depends(get_current_user)):
    """获取我的练习统计"""
    try:
        stats = await practice_service.get_practice_statistics_by_user(current_user["id"])
        
        return PracticeStatistics(
            total_sessions=stats["total_sessions"],
            completed_sessions=stats["completed_sessions"],
            completion_rate=stats["completion_rate"],
            average_score=stats["average_score"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取练习统计失败: {str(e)}"
        )

@router.get("/all-statistics", response_model=PracticeStatistics)
async def get_all_practice_statistics(current_user: dict = Depends(get_current_user)):
    """获取全部练习统计（管理员功能）"""
    try:
        stats = await practice_service.get_all_practice_statistics(current_user["role"])
        
        return PracticeStatistics(
            total_sessions=stats["total_sessions"],
            completed_sessions=stats["completed_sessions"],
            completion_rate=stats["completion_rate"],
            average_score=stats["average_score"],
            active_users=stats["active_users"]
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取练习统计失败: {str(e)}"
        )

# ==================== 反馈管理 ====================

@router.post("/feedback", response_model=FeedbackResponse)
async def create_feedback(
    feedback_data: FeedbackCreate,
    current_user: dict = Depends(get_current_user)
):
    """创建反馈"""
    try:
        feedback = await practice_service.create_feedback(feedback_data.dict())
        
        return FeedbackResponse(
            id=feedback["id"],
            session_id=feedback["session_id"],
            feedback_type=feedback["feedback_type"],
            content=feedback["content"],
            score=feedback.get("score"),
            created_at=feedback["created_at"],
            updated_at=feedback["updated_at"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建反馈失败: {str(e)}"
        )

@router.get("/sessions/{session_id}/feedback", response_model=List[FeedbackResponse])
async def get_session_feedback(
    session_id: int,
    current_user: dict = Depends(get_current_user)
):
    """获取会话的反馈"""
    try:
        feedback_list = await practice_service.get_feedback_by_session(session_id)
        
        return [
            FeedbackResponse(
                id=feedback["id"],
                session_id=feedback["session_id"],
                feedback_type=feedback["feedback_type"],
                content=feedback["content"],
                score=feedback.get("score"),
                created_at=feedback["created_at"],
                updated_at=feedback["updated_at"]
            )
            for feedback in feedback_list
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取会话反馈失败: {str(e)}"
        )

@router.get("/my-feedback", response_model=List[FeedbackResponse])
async def get_my_feedback(
    limit: int = Query(50, ge=1, le=200, description="返回数量限制"),
    offset: int = Query(0, ge=0, description="偏移量"),
    current_user: dict = Depends(get_current_user)
):
    """获取我的反馈"""
    try:
        feedback_list = await practice_service.get_feedback_by_user(
            current_user["id"],
            limit=limit,
            offset=offset
        )
        
        return [
            FeedbackResponse(
                id=feedback["id"],
                session_id=feedback["session_id"],
                feedback_type=feedback["feedback_type"],
                content=feedback["content"],
                score=feedback.get("score"),
                created_at=feedback["created_at"],
                updated_at=feedback["updated_at"],
                practice_sessions=feedback.get("practice_sessions")
            )
            for feedback in feedback_list
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户反馈失败: {str(e)}"
        )

@router.put("/feedback/{feedback_id}", response_model=FeedbackResponse)
async def update_feedback(
    feedback_id: int,
    update_data: FeedbackUpdate,
    current_user: dict = Depends(get_current_user)
):
    """更新反馈"""
    try:
        # 过滤掉None值
        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        
        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="没有提供更新数据"
            )
        
        success = await practice_service.update_feedback(feedback_id, update_dict)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="反馈不存在"
            )
        
        return {"message": "反馈更新成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新反馈失败: {str(e)}"
        )

@router.delete("/feedback/{feedback_id}")
async def delete_feedback(
    feedback_id: int,
    current_user: dict = Depends(get_current_user)
):
    """删除反馈（管理员功能）"""
    try:
        success = await practice_service.delete_feedback(feedback_id, current_user["role"])
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="反馈不存在"
            )
        
        return {"message": "反馈删除成功"}
        
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
            detail=f"删除反馈失败: {str(e)}"
        )

@router.get("/all-feedback", response_model=List[FeedbackResponse])
async def get_all_feedback(
    limit: int = Query(100, ge=1, le=500, description="返回数量限制"),
    offset: int = Query(0, ge=0, description="偏移量"),
    current_user: dict = Depends(get_current_user)
):
    """获取所有反馈（管理员功能）"""
    try:
        feedback_list = await practice_service.get_all_feedback(
            current_user["role"],
            limit=limit,
            offset=offset
        )
        
        return [
            FeedbackResponse(
                id=feedback["id"],
                session_id=feedback["session_id"],
                feedback_type=feedback["feedback_type"],
                content=feedback["content"],
                score=feedback.get("score"),
                created_at=feedback["created_at"],
                updated_at=feedback["updated_at"],
                practice_sessions=feedback.get("practice_sessions")
            )
            for feedback in feedback_list
        ]
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取所有反馈失败: {str(e)}"
        )