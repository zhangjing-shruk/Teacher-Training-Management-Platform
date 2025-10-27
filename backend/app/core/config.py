from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field
import os


class Settings(BaseSettings):
    # 应用基础配置
    APP_NAME: str = "AI教师培训平台"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 环境检测
    ENVIRONMENT: str = Field(default="development", description="运行环境: development, production")
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 生产环境域名配置
    PRODUCTION_FRONTEND_URL: str = Field(default="", description="生产环境前端域名")
    VERCEL_DOMAIN: str = Field(default="", description="Vercel部署域名")
    
    @property
    def CORS_ORIGINS(self) -> List[str]:
        """根据环境动态配置CORS origins"""
        # 开发环境允许的源
        development_origins = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:8001",
            "http://127.0.0.1:8001",
        ]
        
        # 生产环境允许的源
        production_origins = []
        
        # 添加配置的生产域名
        if self.PRODUCTION_FRONTEND_URL:
            production_origins.append(self.PRODUCTION_FRONTEND_URL)
        
        # 添加 Vercel 域名（如果与 PRODUCTION_FRONTEND_URL 不同）
        if self.VERCEL_DOMAIN:
            vercel_url = f"https://{self.VERCEL_DOMAIN}"
            if vercel_url not in production_origins:
                production_origins.append(vercel_url)
        
        # 检测是否在Vercel环境
        is_vercel = os.getenv("VERCEL") == "1"
        is_production = self.ENVIRONMENT == "production" or is_vercel
        
        if is_production:
            # 生产环境：只允许配置的域名 + 本地开发（用于调试）
            return production_origins + [
                "http://localhost:5173",  # 允许本地前端访问Vercel后端
                "http://127.0.0.1:5173"
            ]
        else:
            # 开发环境：允许所有开发域名
            return development_origins
    
    # 可信主机配置 (不包含协议)
    ALLOWED_HOSTS: List[str] = [
        "localhost:5173", 
        "127.0.0.1:5173",
        "localhost:8000",
        "127.0.0.1:8000",
        "localhost:8001",
        "127.0.0.1:8001",
        "localhost",
        "127.0.0.1"
    ]
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Supabase 配置
    SUPABASE_URL: str = Field(default="", description="Supabase项目URL")
    SUPABASE_ANON_KEY: str = Field(default="", description="Supabase匿名密钥")
    SUPABASE_SERVICE_ROLE_KEY: str = Field(default="", description="Supabase服务角色密钥")
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI服务配置占位符
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API密钥")
    AZURE_SPEECH_KEY: str = Field(default="", description="Azure语音服务密钥")
    AZURE_SPEECH_REGION: str = Field(default="", description="Azure语音服务区域")
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        case_sensitive = True
        
        @classmethod
        def env_file(cls):
            """根据环境动态选择配置文件"""
            env = os.getenv("ENVIRONMENT", "development")
            is_vercel = os.getenv("VERCEL") == "1"
            
            if env == "production" or is_vercel:
                return ".env.production"
            else:
                return ".env"


# 创建设置实例，根据环境加载对应的配置文件
def create_settings():
    """创建设置实例"""
    env = os.getenv("ENVIRONMENT", "development")
    is_vercel = os.getenv("VERCEL") == "1"
    
    if env == "production" or is_vercel:
        env_file = ".env.production"
    else:
        env_file = ".env"
    
    # 检查文件是否存在
    if os.path.exists(env_file):
        return Settings(_env_file=env_file)
    else:
        # 如果指定的环境文件不存在，使用默认配置
        return Settings()

settings = create_settings()