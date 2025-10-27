# 后端部署指南

## 部署选项

本项目后端支持多种部署方式：

### 1. Railway 部署（推荐）

1. 访问 [Railway](https://railway.app)
2. 连接你的 GitHub 仓库
3. 选择 `backend` 目录作为根目录
4. Railway 会自动检测到 `railway.json` 配置文件
5. 设置环境变量：
   - `ENVIRONMENT=production`
   - `PRODUCTION_FRONTEND_URL=https://teacher-training-management-platfor.vercel.app`
   - `VERCEL_DOMAIN=teacher-training-management-platfor.vercel.app`
   - `SECRET_KEY=your-secret-key`
   - `SUPABASE_URL=your-supabase-url`
   - `SUPABASE_ANON_KEY=your-supabase-anon-key`
   - `SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key`

### 2. Render 部署

1. 访问 [Render](https://render.com)
2. 连接你的 GitHub 仓库
3. 选择 Web Service
4. 设置根目录为 `backend`
5. Render 会自动检测到 `render.yaml` 配置文件
6. 设置相同的环境变量

### 3. Docker 部署

使用提供的 Dockerfile：

```bash
cd backend
docker build -t ai-teacher-backend .
docker run -p 8000:8000 --env-file .env.production ai-teacher-backend
```

## 部署后配置

1. 获取部署后的 API URL（例如：`https://your-app.railway.app`）
2. 更新前端环境变量 `VITE_API_BASE_URL`
3. 在 Vercel 中设置生产环境变量
4. 重新部署前端

## 验证部署

访问 `https://your-backend-url/docs` 查看 API 文档，确认部署成功。