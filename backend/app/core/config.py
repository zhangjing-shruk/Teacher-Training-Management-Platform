from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # 应用基础配置
    APP_NAME: str = "AI教师培训平台"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 跨域配置 (CORS origins)
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
        "http://localhost",
        "http://127.0.0.1"
    ]
    
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
        env_file = ".env"
        case_sensitive = True


settings = Settings()