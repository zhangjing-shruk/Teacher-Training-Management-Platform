# AI 教师培训平台

一个集成了人工智能的 Web 应用，为在线英语教育的新任教师提供标准化的试讲练习平台。

## 项目结构

```
AI教师培训平台-trae/
├── frontend/          # Vue.js 3 前端应用
├── backend/           # FastAPI 后端应用
├── docs/             # 项目文档
└── README.md         # 项目说明
```

## 技术栈

### 前端
- Vue.js 3 + TypeScript
- Vue Router (路由管理)
- Pinia (状态管理)
- Vite (构建工具)

### 后端
- FastAPI (Python Web框架)
- SQLAlchemy (ORM)
- PostgreSQL/SQLite (数据库)
- Alembic (数据库迁移)

### AI服务 (第三方API)
- Google Cloud Speech-to-Text (语音识别)
- Azure Cognitive Services (情感分析)
- 自定义内容分析逻辑

## 快速开始

### 前端开发
```bash
cd frontend
npm install
npm run dev
```

### 后端开发
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 环境变量配置

创建 `.env` 文件并配置以下变量：

```env
# 数据库
DATABASE_URL=postgresql://user:password@localhost/dbname

# AI服务API密钥 (生产环境配置)
GOOGLE_API_KEY=your_google_api_key
AZURE_API_KEY=your_azure_api_key
AZURE_API_REGION=your_azure_region

# JWT密钥
SECRET_KEY=your_secret_key
```

## 部署

- 前端：Vercel
- 后端：Vercel Serverless Functions
- 数据库：Supabase PostgreSQL