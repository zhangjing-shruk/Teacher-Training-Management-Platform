from typing import List, Optional, Dict, Any
from supabase import Client
from app.core.supabase import get_supabase_client, get_supabase_admin_client, Tables, UserRoles
from app.core.security import get_password_hash, verify_password
import logging

logger = logging.getLogger(__name__)

class SupabaseUserService:
    """Supabase 用户服务 - 处理多用户系统的用户管理"""
    
    def __init__(self):
        self.client = get_supabase_client()
        self.admin_client = get_supabase_admin_client()
    
    async def create_user(self, email: str, name: str, password: str, role: str) -> Dict[str, Any]:
        """创建新用户"""
        try:
            # 验证角色
            if role not in [UserRoles.TEACHER, UserRoles.MANAGER]:
                raise ValueError(f"无效的用户角色: {role}")
            
            # 检查邮箱是否已存在
            existing_user = self.client.table(Tables.USERS).select("id").eq("email", email).execute()
            if existing_user.data:
                raise ValueError("邮箱已存在")
            
            # 创建用户
            hashed_password = get_password_hash(password)
            user_data = {
                "email": email,
                "name": name,
                "hashed_password": hashed_password,
                "role": role,
                "is_active": True,
                "training_status": "not_started",
                "training_progress": 0
            }
            
            result = self.client.table(Tables.USERS).insert(user_data).execute()
            
            if result.data:
                user = result.data[0]
                # 移除敏感信息
                user.pop("hashed_password", None)
                logger.info(f"用户创建成功: {email}, 角色: {role}")
                return user
            else:
                raise Exception("用户创建失败")
                
        except Exception as e:
            logger.error(f"创建用户失败: {e}")
            raise
    
    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """用户认证"""
        try:
            # 查询用户
            result = self.client.table(Tables.USERS).select("*").eq("email", email).eq("is_active", True).execute()
            
            if not result.data:
                return None
            
            user = result.data[0]
            
            # 验证密码
            if not verify_password(password, user["hashed_password"]):
                return None
            
            # 移除敏感信息
            user.pop("hashed_password", None)
            logger.info(f"用户认证成功: {email}")
            return user
            
        except Exception as e:
            logger.error(f"用户认证失败: {e}")
            return None
    
    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取用户"""
        try:
            result = self.client.table(Tables.USERS).select("*").eq("id", user_id).eq("is_active", True).execute()
            
            if result.data:
                user = result.data[0]
                user.pop("hashed_password", None)
                return user
            return None
            
        except Exception as e:
            logger.error(f"获取用户失败: {e}")
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """根据邮箱获取用户"""
        try:
            result = self.client.table(Tables.USERS).select("*").eq("email", email).eq("is_active", True).execute()
            
            if result.data:
                user = result.data[0]
                user.pop("hashed_password", None)
                return user
            return None
            
        except Exception as e:
            logger.error(f"获取用户失败: {e}")
            return None
    
    async def get_users_by_role(self, role: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """根据角色获取用户列表"""
        try:
            if role not in [UserRoles.TEACHER, UserRoles.MANAGER]:
                raise ValueError(f"无效的用户角色: {role}")
            
            result = (self.client.table(Tables.USERS)
                     .select("id,email,name,role,is_active,training_status,training_progress,created_at,updated_at")
                     .eq("role", role)
                     .eq("is_active", True)
                     .range(offset, offset + limit - 1)
                     .execute())
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"获取用户列表失败: {e}")
            return []
    
    async def update_user_training_progress(self, user_id: int, progress: int, status: str = None) -> bool:
        """更新用户培训进度"""
        try:
            update_data = {"training_progress": progress}
            if status:
                update_data["training_status"] = status
            
            result = self.client.table(Tables.USERS).update(update_data).eq("id", user_id).execute()
            
            if result.data:
                logger.info(f"用户 {user_id} 培训进度更新成功: {progress}%")
                return True
            return False
            
        except Exception as e:
            logger.error(f"更新用户培训进度失败: {e}")
            return False
    
    async def update_user_profile(self, user_id: int, name: str = None, email: str = None) -> bool:
        """更新用户资料"""
        try:
            update_data = {}
            if name:
                update_data["name"] = name
            if email:
                # 检查新邮箱是否已存在
                existing = self.client.table(Tables.USERS).select("id").eq("email", email).neq("id", user_id).execute()
                if existing.data:
                    raise ValueError("邮箱已存在")
                update_data["email"] = email
            
            if not update_data:
                return True
            
            result = self.client.table(Tables.USERS).update(update_data).eq("id", user_id).execute()
            
            if result.data:
                logger.info(f"用户 {user_id} 资料更新成功")
                return True
            return False
            
        except Exception as e:
            logger.error(f"更新用户资料失败: {e}")
            return False
    
    async def deactivate_user(self, user_id: int) -> bool:
        """停用用户"""
        try:
            result = self.client.table(Tables.USERS).update({"is_active": False}).eq("id", user_id).execute()
            
            if result.data:
                logger.info(f"用户 {user_id} 已停用")
                return True
            return False
            
        except Exception as e:
            logger.error(f"停用用户失败: {e}")
            return False
    
    async def get_user_statistics(self) -> Dict[str, Any]:
        """获取用户统计信息（管理员功能）"""
        try:
            # 总用户数
            total_users = self.client.table(Tables.USERS).select("id", count="exact").eq("is_active", True).execute()
            
            # 教师数量
            teachers = self.client.table(Tables.USERS).select("id", count="exact").eq("role", UserRoles.TEACHER).eq("is_active", True).execute()
            
            # 管理员数量
            managers = self.client.table(Tables.USERS).select("id", count="exact").eq("role", UserRoles.MANAGER).eq("is_active", True).execute()
            
            # 培训完成情况
            completed_training = self.client.table(Tables.USERS).select("id", count="exact").eq("training_status", "completed").eq("is_active", True).execute()
            
            return {
                "total_users": total_users.count or 0,
                "teachers": teachers.count or 0,
                "managers": managers.count or 0,
                "completed_training": completed_training.count or 0
            }
            
        except Exception as e:
            logger.error(f"获取用户统计失败: {e}")
            return {
                "total_users": 0,
                "teachers": 0,
                "managers": 0,
                "completed_training": 0
            }