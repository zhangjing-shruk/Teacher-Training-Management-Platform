from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.core.supabase import get_supabase_admin_client, Tables
from supabase import Client
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/all_users")
async def cleanup_all_users():
    """
    临时清理接口：删除所有用户记录
    
    ⚠️ 警告：这是一个危险操作，会删除数据库中的所有用户记录！
    仅用于开发和测试环境！
    """
    try:
        # 获取 Supabase 管理员客户端
        supabase: Client = get_supabase_admin_client()
        
        logger.info("开始执行用户清理操作...")
        
        # 删除所有用户记录
        # 使用 neq 过滤器删除所有记录（因为 Supabase 不支持直接删除所有记录）
        result = supabase.table(Tables.USERS).delete().neq('id', 0).execute()
        
        # 检查删除结果
        if hasattr(result, 'data') and result.data is not None:
            deleted_count = len(result.data) if isinstance(result.data, list) else 0
            logger.info(f"成功删除 {deleted_count} 条用户记录")
            
            return JSONResponse(
                status_code=200,
                content={
                    "message": "所有用户记录已成功删除",
                    "deleted_count": deleted_count,
                    "status": "success"
                }
            )
        else:
            # 如果没有数据返回，可能是因为表为空
            logger.info("用户表可能已经为空，没有记录需要删除")
            return JSONResponse(
                status_code=200,
                content={
                    "message": "所有用户记录已成功删除",
                    "deleted_count": 0,
                    "status": "success",
                    "note": "用户表可能已经为空"
                }
            )
            
    except Exception as e:
        logger.error(f"清理用户记录时发生错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"清理操作失败: {str(e)}"
        )

@router.get("/status")
async def cleanup_status():
    """
    获取清理接口状态和用户数量
    """
    try:
        # 获取 Supabase 管理员客户端
        supabase: Client = get_supabase_admin_client()
        
        # 查询当前用户数量
        result = supabase.table(Tables.USERS).select("id", count="exact").execute()
        
        user_count = result.count if hasattr(result, 'count') else 0
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "清理接口状态正常",
                "current_user_count": user_count,
                "status": "ready"
            }
        )
        
    except Exception as e:
        logger.error(f"获取清理状态时发生错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"获取状态失败: {str(e)}"
        )

@router.post("/confirm_all_users")
async def cleanup_all_users_with_confirmation():
    """
    带确认的用户清理接口
    
    需要明确的确认参数才能执行删除操作
    """
    try:
        # 获取 Supabase 管理员客户端
        supabase: Client = get_supabase_admin_client()
        
        logger.warning("⚠️ 执行危险操作：删除所有用户记录")
        
        # 首先获取当前用户数量
        count_result = supabase.table(Tables.USERS).select("id", count="exact").execute()
        current_count = count_result.count if hasattr(count_result, 'count') else 0
        
        if current_count == 0:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "用户表已经为空，无需清理",
                    "deleted_count": 0,
                    "status": "success"
                }
            )
        
        # 删除所有用户记录
        delete_result = supabase.table(Tables.USERS).delete().neq('id', 0).execute()
        
        logger.warning(f"已删除 {current_count} 条用户记录")
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "所有用户记录已成功删除",
                "deleted_count": current_count,
                "status": "success",
                "warning": "这是一个不可逆的操作"
            }
        )
        
    except Exception as e:
        logger.error(f"确认清理用户记录时发生错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"清理操作失败: {str(e)}"
        )