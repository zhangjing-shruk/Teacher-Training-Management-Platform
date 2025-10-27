# Vercel API 部署指南

## 概述

本项目现在支持将 FastAPI 后端部署为 Vercel Serverless Functions，与前端一起部署在同一个 Vercel 项目中。

## 项目结构

```
├── api/                    # Vercel API Functions
│   ├── index.py           # 主 API 入口（完整 FastAPI 应用）
│   └── hello.py           # 简单测试 API
├── backend/               # FastAPI 应用源码
├── frontend/              # Vue.js 前端
├── vercel.json           # Vercel 配置
└── requirements.txt      # Python 依赖
```

## 部署步骤

### 1. 推送代码到 GitHub

确保所有更改已提交并推送到 GitHub 仓库。

### 2. 在 Vercel 中部署

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 "New Project"
3. 选择你的 GitHub 仓库
4. Vercel 会自动检测到 `vercel.json` 配置

### 3. 设置环境变量

在 Vercel 项目设置中添加以下环境变量：

```
ENVIRONMENT=production
PRODUCTION_FRONTEND_URL=https://your-project.vercel.app
VERCEL_DOMAIN=your-project.vercel.app
SECRET_KEY=your-secret-key
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
```

### 4. 部署验证

部署完成后，访问以下端点验证：

- 前端：`https://your-project.vercel.app`
- API 测试：`https://your-project.vercel.app/api/hello`
- API 文档：`https://your-project.vercel.app/api/docs`

## API 端点

- `/api/hello` - 简单测试端点
- `/api/*` - 完整 FastAPI 应用的所有路由

## 注意事项

1. **冷启动**：Serverless Functions 可能有冷启动延迟
2. **超时限制**：Vercel 免费版有 10 秒执行时间限制
3. **内存限制**：注意 Serverless Functions 的内存使用
4. **数据库连接**：使用连接池优化数据库连接

## 故障排除

### API 无法访问
- 检查 `vercel.json` 中的 rewrites 配置
- 确认 `requirements.txt` 包含所有必要依赖
- 查看 Vercel 部署日志

### CORS 错误
- 确认 API 中的 CORS 配置包含正确的域名
- 检查前端环境变量 `VITE_API_BASE_URL`

### 依赖错误
- 确保 `mangum` 包已添加到 `requirements.txt`
- 检查 Python 版本兼容性（使用 Python 3.9）