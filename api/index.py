from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import sys
import os

# 添加后端目录到 Python 路径
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# 导入 FastAPI 应用
from app.main import app

# 使用 Mangum 适配器将 FastAPI 应用转换为 ASGI 兼容的处理器
handler = Mangum(app)