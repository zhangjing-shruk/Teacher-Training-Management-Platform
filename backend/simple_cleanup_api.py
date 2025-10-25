#!/usr/bin/env python3
"""
简化的清理API服务
独立运行，不依赖复杂的Supabase客户端
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
from dotenv import load_dotenv
import uvicorn

# 加载环境变量
load_dotenv()

app = FastAPI(
    title="AI教师培训平台 - 清理接口",
    description="临时清理接口服务",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase配置
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print("⚠️  警告: 缺少Supabase配置")

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI教师培训平台 - 清理接口服务",
        "status": "running",
        "endpoints": [
            "GET /api/cleanup/status - 查询状态",
            "POST /api/cleanup/all_users - 删除所有用户"
        ]
    }

@app.get("/api/cleanup/status")
async def cleanup_status():
    """查询清理接口状态和当前用户数量"""
    try:
        if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
            return {
                "status": "error",
                "message": "Supabase配置缺失",
                "user_count": -1
            }
        
        # 使用httpx直接调用Supabase REST API
        headers = {
            "apikey": SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            # 查询用户数量
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/users?select=id",
                headers=headers
            )
            
            if response.status_code == 200:
                users = response.json()
                user_count = len(users)
                
                return {
                    "status": "active",
                    "message": "清理接口运行正常",
                    "user_count": user_count,
                    "supabase_connected": True
                }
            else:
                return {
                    "status": "error",
                    "message": f"Supabase查询失败: {response.status_code}",
                    "user_count": -1,
                    "supabase_connected": False
                }
                
    except Exception as e:
        return {
            "status": "error",
            "message": f"状态查询失败: {str(e)}",
            "user_count": -1,
            "supabase_connected": False
        }

@app.post("/api/cleanup/all_users")
async def cleanup_all_users():
    """
    删除所有用户记录
    ⚠️ 警告：这是一个危险操作，会删除所有用户数据！
    """
    try:
        if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
            raise HTTPException(
                status_code=500,
                detail="Supabase配置缺失"
            )
        
        # 使用httpx直接调用Supabase REST API
        headers = {
            "apikey": SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            # 先查询当前用户数量
            count_response = await client.get(
                f"{SUPABASE_URL}/rest/v1/users?select=id",
                headers=headers
            )
            
            if count_response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=f"查询用户失败: {count_response.status_code}"
                )
            
            users = count_response.json()
            user_count = len(users)
            
            if user_count == 0:
                return {
                    "message": "用户表已经为空，无需清理",
                    "deleted_count": 0,
                    "status": "success"
                }
            
            # 删除所有用户记录 - 使用通用的过滤器
            delete_response = await client.delete(
                f"{SUPABASE_URL}/rest/v1/users?email=neq.null",
                headers=headers
            )
            
            print(f"删除响应状态码: {delete_response.status_code}")
            print(f"删除响应内容: {delete_response.text}")
            
            if delete_response.status_code in [200, 204]:
                return {
                    "message": "所有用户记录已成功删除",
                    "deleted_count": user_count,
                    "status": "success"
                }
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"删除操作失败: {delete_response.status_code} - {delete_response.text}"
                )
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"清理操作失败: {str(e)}"
        )

if __name__ == "__main__":
    print("🚀 启动简化清理API服务...")
    print("📍 服务地址: http://localhost:8001")
    print("📋 可用接口:")
    print("   GET  / - 服务信息")
    print("   GET  /api/cleanup/status - 查询状态")
    print("   POST /api/cleanup/all_users - 删除所有用户")
    
    uvicorn.run(
        "simple_cleanup_api:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )