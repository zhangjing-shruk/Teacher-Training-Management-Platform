from typing import List, Optional, Dict, Any
from supabase import Client
from app.core.supabase import get_supabase_client, Tables, MaterialTypes, UserRoles
import logging

logger = logging.getLogger(__name__)

class SupabaseTrainingService:
    """Supabase 培训服务 - 处理培训资料和学习进度"""
    
    def __init__(self):
        self.client = get_supabase_client()
    
    # ==================== 培训资料管理 ====================
    
    async def create_training_material(self, material_data: Dict[str, Any], creator_role: str) -> Dict[str, Any]:
        """创建培训资料（仅管理员）"""
        try:
            if creator_role != UserRoles.MANAGER:
                raise ValueError("只有管理员可以创建培训资料")
            
            # 验证资料类型
            if material_data.get("type") not in [MaterialTypes.VIDEO, MaterialTypes.DOCUMENT, MaterialTypes.AUDIO, MaterialTypes.INTERACTIVE]:
                raise ValueError("无效的资料类型")
            
            result = self.client.table(Tables.TRAINING_MATERIALS).insert(material_data).execute()
            
            if result.data:
                logger.info(f"培训资料创建成功: {material_data.get('title')}")
                return result.data[0]
            else:
                raise Exception("培训资料创建失败")
                
        except Exception as e:
            logger.error(f"创建培训资料失败: {e}")
            raise
    
    async def get_training_materials(self, status: str = None, category: str = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """获取培训资料列表"""
        try:
            query = self.client.table(Tables.TRAINING_MATERIALS).select("*")
            
            if status:
                query = query.eq("status", status)
            if category:
                query = query.eq("category", category)
            
            result = query.order("order_index").range(offset, offset + limit - 1).execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"获取培训资料失败: {e}")
            return []
    
    async def get_training_material_by_id(self, material_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取培训资料"""
        try:
            result = self.client.table(Tables.TRAINING_MATERIALS).select("*").eq("id", material_id).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            logger.error(f"获取培训资料失败: {e}")
            return None
    
    async def update_training_material(self, material_id: int, update_data: Dict[str, Any], updater_role: str) -> bool:
        """更新培训资料（仅管理员）"""
        try:
            if updater_role != UserRoles.MANAGER:
                raise ValueError("只有管理员可以更新培训资料")
            
            result = self.client.table(Tables.TRAINING_MATERIALS).update(update_data).eq("id", material_id).execute()
            
            if result.data:
                logger.info(f"培训资料 {material_id} 更新成功")
                return True
            return False
            
        except Exception as e:
            logger.error(f"更新培训资料失败: {e}")
            return False
    
    async def delete_training_material(self, material_id: int, deleter_role: str) -> bool:
        """删除培训资料（仅管理员）"""
        try:
            if deleter_role != UserRoles.MANAGER:
                raise ValueError("只有管理员可以删除培训资料")
            
            result = self.client.table(Tables.TRAINING_MATERIALS).delete().eq("id", material_id).execute()
            
            if result.data:
                logger.info(f"培训资料 {material_id} 删除成功")
                return True
            return False
            
        except Exception as e:
            logger.error(f"删除培训资料失败: {e}")
            return False
    
    async def increment_download_count(self, material_id: int) -> bool:
        """增加下载次数"""
        try:
            # 先获取当前下载次数
            current = self.client.table(Tables.TRAINING_MATERIALS).select("download_count").eq("id", material_id).execute()
            
            if current.data:
                new_count = (current.data[0].get("download_count") or 0) + 1
                result = self.client.table(Tables.TRAINING_MATERIALS).update({"download_count": new_count}).eq("id", material_id).execute()
                
                if result.data:
                    return True
            return False
            
        except Exception as e:
            logger.error(f"更新下载次数失败: {e}")
            return False
    
    # ==================== 学习进度管理 ====================
    
    async def start_learning(self, user_id: int, material_id: int) -> Dict[str, Any]:
        """开始学习资料"""
        try:
            # 检查是否已有学习记录
            existing = self.client.table(Tables.LEARNING_PROGRESS).select("*").eq("user_id", user_id).eq("material_id", material_id).execute()
            
            if existing.data:
                # 更新开始时间和最后活跃时间
                progress_data = {
                    "start_time": "now()",
                    "last_active_time": "now()"
                }
                result = self.client.table(Tables.LEARNING_PROGRESS).update(progress_data).eq("user_id", user_id).eq("material_id", material_id).execute()
                return result.data[0] if result.data else existing.data[0]
            else:
                # 创建新的学习记录
                progress_data = {
                    "user_id": user_id,
                    "material_id": material_id,
                    "start_time": "now()",
                    "last_active_time": "now()",
                    "total_study_seconds": 0,
                    "is_completed": False
                }
                result = self.client.table(Tables.LEARNING_PROGRESS).insert(progress_data).execute()
                
                if result.data:
                    logger.info(f"用户 {user_id} 开始学习资料 {material_id}")
                    return result.data[0]
                else:
                    raise Exception("创建学习记录失败")
                    
        except Exception as e:
            logger.error(f"开始学习失败: {e}")
            raise
    
    async def update_learning_progress(self, user_id: int, material_id: int, study_seconds: int) -> bool:
        """更新学习进度"""
        try:
            # 获取当前学习记录
            current = self.client.table(Tables.LEARNING_PROGRESS).select("total_study_seconds").eq("user_id", user_id).eq("material_id", material_id).execute()
            
            if current.data:
                new_total = (current.data[0].get("total_study_seconds") or 0) + study_seconds
                update_data = {
                    "total_study_seconds": new_total,
                    "last_active_time": "now()"
                }
                
                result = self.client.table(Tables.LEARNING_PROGRESS).update(update_data).eq("user_id", user_id).eq("material_id", material_id).execute()
                
                if result.data:
                    logger.info(f"用户 {user_id} 学习进度更新: +{study_seconds}秒")
                    return True
            return False
            
        except Exception as e:
            logger.error(f"更新学习进度失败: {e}")
            return False
    
    async def complete_learning(self, user_id: int, material_id: int) -> bool:
        """完成学习"""
        try:
            update_data = {
                "is_completed": True,
                "completion_time": "now()",
                "last_active_time": "now()"
            }
            
            result = self.client.table(Tables.LEARNING_PROGRESS).update(update_data).eq("user_id", user_id).eq("material_id", material_id).execute()
            
            if result.data:
                logger.info(f"用户 {user_id} 完成学习资料 {material_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"完成学习失败: {e}")
            return False
    
    async def get_user_learning_progress(self, user_id: int) -> List[Dict[str, Any]]:
        """获取用户学习进度"""
        try:
            result = (self.client.table(Tables.LEARNING_PROGRESS)
                     .select("*, training_materials(*)")
                     .eq("user_id", user_id)
                     .execute())
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"获取用户学习进度失败: {e}")
            return []
    
    async def get_material_learning_statistics(self, material_id: int) -> Dict[str, Any]:
        """获取资料学习统计（管理员功能）"""
        try:
            # 总学习人数
            total_learners = self.client.table(Tables.LEARNING_PROGRESS).select("id", count="exact").eq("material_id", material_id).execute()
            
            # 完成学习人数
            completed_learners = self.client.table(Tables.LEARNING_PROGRESS).select("id", count="exact").eq("material_id", material_id).eq("is_completed", True).execute()
            
            # 平均学习时长
            avg_time = self.client.table(Tables.LEARNING_PROGRESS).select("total_study_seconds").eq("material_id", material_id).execute()
            
            total_seconds = sum(item.get("total_study_seconds", 0) for item in (avg_time.data or []))
            avg_seconds = total_seconds / len(avg_time.data) if avg_time.data else 0
            
            return {
                "total_learners": total_learners.count or 0,
                "completed_learners": completed_learners.count or 0,
                "completion_rate": (completed_learners.count / total_learners.count * 100) if total_learners.count else 0,
                "average_study_time_seconds": int(avg_seconds)
            }
            
        except Exception as e:
            logger.error(f"获取资料学习统计失败: {e}")
            return {
                "total_learners": 0,
                "completed_learners": 0,
                "completion_rate": 0,
                "average_study_time_seconds": 0
            }