from typing import List, Optional, Dict, Any
from supabase import Client
from app.core.supabase import get_supabase_client, Tables, PracticeStatus, UserRoles
import logging

logger = logging.getLogger(__name__)

class SupabasePracticeService:
    """Supabase 练习服务 - 处理练习会话和反馈"""
    
    def __init__(self):
        self.client = get_supabase_client()
    
    # ==================== 练习会话管理 ====================
    
    async def create_practice_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建练习会话"""
        try:
            # 设置默认状态
            session_data["status"] = PracticeStatus.IN_PROGRESS
            
            result = self.client.table(Tables.PRACTICE_SESSIONS).insert(session_data).execute()
            
            if result.data:
                logger.info(f"练习会话创建成功: 用户 {session_data.get('user_id')}, 资料 {session_data.get('material_id')}")
                return result.data[0]
            else:
                raise Exception("练习会话创建失败")
                
        except Exception as e:
            logger.error(f"创建练习会话失败: {e}")
            raise
    
    async def get_practice_sessions_by_user(self, user_id: int, status: str = None, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """获取用户的练习会话"""
        try:
            query = (self.client.table(Tables.PRACTICE_SESSIONS)
                    .select("*, training_materials(title, type)")
                    .eq("user_id", user_id))
            
            if status:
                query = query.eq("status", status)
            
            result = query.order("created_at", desc=True).range(offset, offset + limit - 1).execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"获取用户练习会话失败: {e}")
            return []
    
    async def get_practice_session_by_id(self, session_id: int, user_id: int = None) -> Optional[Dict[str, Any]]:
        """根据ID获取练习会话"""
        try:
            query = (self.client.table(Tables.PRACTICE_SESSIONS)
                    .select("*, training_materials(title, type), users(name, email)")
                    .eq("id", session_id))
            
            # 如果指定了用户ID，则只返回该用户的会话
            if user_id:
                query = query.eq("user_id", user_id)
            
            result = query.execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            logger.error(f"获取练习会话失败: {e}")
            return None
    
    async def update_practice_session(self, session_id: int, update_data: Dict[str, Any], user_id: int = None) -> bool:
        """更新练习会话"""
        try:
            query = self.client.table(Tables.PRACTICE_SESSIONS).update(update_data).eq("id", session_id)
            
            # 如果指定了用户ID，则只允许更新该用户的会话
            if user_id:
                query = query.eq("user_id", user_id)
            
            result = query.execute()
            
            if result.data:
                logger.info(f"练习会话 {session_id} 更新成功")
                return True
            return False
            
        except Exception as e:
            logger.error(f"更新练习会话失败: {e}")
            return False
    
    async def complete_practice_session(self, session_id: int, user_id: int, score: float = None) -> bool:
        """完成练习会话"""
        try:
            update_data = {
                "status": PracticeStatus.COMPLETED,
                "end_time": "now()"
            }
            
            if score is not None:
                update_data["score"] = score
            
            result = (self.client.table(Tables.PRACTICE_SESSIONS)
                     .update(update_data)
                     .eq("id", session_id)
                     .eq("user_id", user_id)
                     .execute())
            
            if result.data:
                logger.info(f"用户 {user_id} 完成练习会话 {session_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"完成练习会话失败: {e}")
            return False
    
    async def get_practice_statistics_by_user(self, user_id: int) -> Dict[str, Any]:
        """获取用户练习统计"""
        try:
            # 总练习次数
            total_sessions = self.client.table(Tables.PRACTICE_SESSIONS).select("id", count="exact").eq("user_id", user_id).execute()
            
            # 完成的练习次数
            completed_sessions = self.client.table(Tables.PRACTICE_SESSIONS).select("id", count="exact").eq("user_id", user_id).eq("status", PracticeStatus.COMPLETED).execute()
            
            # 平均分数
            scores = self.client.table(Tables.PRACTICE_SESSIONS).select("score").eq("user_id", user_id).eq("status", PracticeStatus.COMPLETED).execute()
            
            valid_scores = [item["score"] for item in (scores.data or []) if item.get("score") is not None]
            avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0
            
            return {
                "total_sessions": total_sessions.count or 0,
                "completed_sessions": completed_sessions.count or 0,
                "completion_rate": (completed_sessions.count / total_sessions.count * 100) if total_sessions.count else 0,
                "average_score": round(avg_score, 2)
            }
            
        except Exception as e:
            logger.error(f"获取用户练习统计失败: {e}")
            return {
                "total_sessions": 0,
                "completed_sessions": 0,
                "completion_rate": 0,
                "average_score": 0
            }
    
    async def get_all_practice_statistics(self, requester_role: str) -> Dict[str, Any]:
        """获取全部练习统计（管理员功能）"""
        try:
            if requester_role != UserRoles.MANAGER:
                raise ValueError("只有管理员可以查看全部练习统计")
            
            # 总练习次数
            total_sessions = self.client.table(Tables.PRACTICE_SESSIONS).select("id", count="exact").execute()
            
            # 完成的练习次数
            completed_sessions = self.client.table(Tables.PRACTICE_SESSIONS).select("id", count="exact").eq("status", PracticeStatus.COMPLETED).execute()
            
            # 参与练习的用户数
            active_users = self.client.table(Tables.PRACTICE_SESSIONS).select("user_id").execute()
            unique_users = len(set(item["user_id"] for item in (active_users.data or [])))
            
            # 平均分数
            scores = self.client.table(Tables.PRACTICE_SESSIONS).select("score").eq("status", PracticeStatus.COMPLETED).execute()
            valid_scores = [item["score"] for item in (scores.data or []) if item.get("score") is not None]
            avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0
            
            return {
                "total_sessions": total_sessions.count or 0,
                "completed_sessions": completed_sessions.count or 0,
                "completion_rate": (completed_sessions.count / total_sessions.count * 100) if total_sessions.count else 0,
                "active_users": unique_users,
                "average_score": round(avg_score, 2)
            }
            
        except Exception as e:
            logger.error(f"获取全部练习统计失败: {e}")
            return {
                "total_sessions": 0,
                "completed_sessions": 0,
                "completion_rate": 0,
                "active_users": 0,
                "average_score": 0
            }
    
    # ==================== 反馈管理 ====================
    
    async def create_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建反馈"""
        try:
            result = self.client.table(Tables.FEEDBACK).insert(feedback_data).execute()
            
            if result.data:
                logger.info(f"反馈创建成功: 会话 {feedback_data.get('session_id')}")
                return result.data[0]
            else:
                raise Exception("反馈创建失败")
                
        except Exception as e:
            logger.error(f"创建反馈失败: {e}")
            raise
    
    async def get_feedback_by_session(self, session_id: int) -> List[Dict[str, Any]]:
        """获取会话的反馈"""
        try:
            result = (self.client.table(Tables.FEEDBACK)
                     .select("*")
                     .eq("session_id", session_id)
                     .order("created_at")
                     .execute())
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"获取会话反馈失败: {e}")
            return []
    
    async def get_feedback_by_user(self, user_id: int, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """获取用户的反馈"""
        try:
            result = (self.client.table(Tables.FEEDBACK)
                     .select("*, practice_sessions(material_id, training_materials(title))")
                     .eq("practice_sessions.user_id", user_id)
                     .order("created_at", desc=True)
                     .range(offset, offset + limit - 1)
                     .execute())
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"获取用户反馈失败: {e}")
            return []
    
    async def update_feedback(self, feedback_id: int, update_data: Dict[str, Any]) -> bool:
        """更新反馈"""
        try:
            result = self.client.table(Tables.FEEDBACK).update(update_data).eq("id", feedback_id).execute()
            
            if result.data:
                logger.info(f"反馈 {feedback_id} 更新成功")
                return True
            return False
            
        except Exception as e:
            logger.error(f"更新反馈失败: {e}")
            return False
    
    async def delete_feedback(self, feedback_id: int, deleter_role: str) -> bool:
        """删除反馈（仅管理员）"""
        try:
            if deleter_role != UserRoles.MANAGER:
                raise ValueError("只有管理员可以删除反馈")
            
            result = self.client.table(Tables.FEEDBACK).delete().eq("id", feedback_id).execute()
            
            if result.data:
                logger.info(f"反馈 {feedback_id} 删除成功")
                return True
            return False
            
        except Exception as e:
            logger.error(f"删除反馈失败: {e}")
            return False
    
    async def get_all_feedback(self, requester_role: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """获取所有反馈（管理员功能）"""
        try:
            if requester_role != UserRoles.MANAGER:
                raise ValueError("只有管理员可以查看所有反馈")
            
            result = (self.client.table(Tables.FEEDBACK)
                     .select("*, practice_sessions(user_id, material_id, users(name, email), training_materials(title))")
                     .order("created_at", desc=True)
                     .range(offset, offset + limit - 1)
                     .execute())
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"获取所有反馈失败: {e}")
            return []