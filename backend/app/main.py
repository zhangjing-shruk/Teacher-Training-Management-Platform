from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api.auth import router as auth_router
from app.api.teacher import router as teacher_router
from app.api.manager import router as manager_router
from app.api.learning_progress import router as learning_progress_router
# Supabase API 路由
from app.api.supabase_auth import router as supabase_auth_router
from app.api.supabase_training import router as supabase_training_router
from app.api.supabase_practice import router as supabase_practice_router
# 临时清理接口
from app.api.cleanup import router as cleanup_router
from app.core.config import settings

app = FastAPI(
    title="AI教师培训平台 API",
    description="AI驱动的英语教师培训平台后端API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "X-CSRF-Token",
    ],
    expose_headers=["*"],
)

# 可信主机中间件 (开发环境中暂时禁用)
# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=settings.ALLOWED_HOSTS
# )

# 静态文件服务
uploads_dir = "uploads"
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# 路由注册
app.include_router(auth_router, prefix="/api/auth", tags=["认证"])
app.include_router(teacher_router, prefix="/api/teacher", tags=["教师端"])
app.include_router(manager_router, prefix="/api/manager", tags=["管理端"])
app.include_router(learning_progress_router, prefix="/api/learning-progress", tags=["学习进度"])

# Supabase API 路由
app.include_router(supabase_auth_router, prefix="/api/supabase-auth", tags=["Supabase认证"])
app.include_router(supabase_training_router, prefix="/api/supabase-training", tags=["Supabase培训"])
app.include_router(supabase_practice_router, prefix="/api/supabase-practice", tags=["Supabase练习"])

# 临时清理接口 (⚠️ 仅用于开发和测试环境)
app.include_router(cleanup_router, prefix="/api/cleanup", tags=["临时清理接口"])

@app.get("/")
async def root():
    return {"message": "AI教师培训平台 API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)