from supabase import create_client, Client
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Supabase 客户端实例
supabase: Client = None

def get_supabase_client() -> Client:
    """获取 Supabase 客户端实例"""
    global supabase
    
    if supabase is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
            raise ValueError("Supabase URL 和 ANON KEY 必须在环境变量中配置")
        
        try:
            supabase = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_ANON_KEY
            )
            logger.info("Supabase 客户端初始化成功")
        except Exception as e:
            logger.error(f"Supabase 客户端初始化失败: {e}")
            raise
    
    return supabase

def get_supabase_admin_client() -> Client:
    """获取 Supabase 管理员客户端实例（使用 service role key）"""
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
        raise ValueError("Supabase URL 和 SERVICE ROLE KEY 必须在环境变量中配置")
    
    try:
        admin_client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY
        )
        logger.info("Supabase 管理员客户端初始化成功")
        return admin_client
    except Exception as e:
        logger.error(f"Supabase 管理员客户端初始化失败: {e}")
        raise

# 数据库表名常量
class Tables:
    USERS = "users"
    TRAINING_MATERIALS = "training_materials"
    PRACTICE_SESSIONS = "practice_sessions"
    FEEDBACK = "feedback"
    LEARNING_PROGRESS = "learning_progress"

# 用户角色常量
class UserRoles:
    TEACHER = "teacher"
    MANAGER = "manager"

# 培训状态常量
class TrainingStatus:
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# 资料类型常量
class MaterialTypes:
    VIDEO = "video"
    DOCUMENT = "document"
    AUDIO = "audio"
    INTERACTIVE = "interactive"

# 练习状态常量
class PracticeStatus:
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REVIEWED = "reviewed"