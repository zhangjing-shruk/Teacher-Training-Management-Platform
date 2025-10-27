from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://teacher-training-management-platfor.vercel.app",
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI教师培训平台 API 正在运行", "status": "success"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Teacher Training Platform API"}

# Vercel 处理器
from mangum import Mangum
handler = Mangum(app)