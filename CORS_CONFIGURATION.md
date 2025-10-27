# CORS 配置说明

## 概述

本项目已经配置了智能的 CORS（跨域资源共享）中间件，能够根据运行环境自动调整允许的域名，确保开发和生产环境的安全性。

## 配置特性

### 🔧 智能环境检测
- **开发环境**: 允许本地开发域名（localhost:5173 等）
- **生产环境**: 只允许配置的生产域名 + 本地调试域名
- **Vercel 自动检测**: 通过 `VERCEL=1` 环境变量自动识别 Vercel 部署环境

### 🌐 支持的 HTTP 方法
- GET
- POST  
- PUT
- DELETE
- OPTIONS（预检请求）

### 📋 允许的 HTTP 头部
- Accept
- Accept-Language
- Content-Language
- Content-Type
- Authorization
- X-Requested-With
- X-CSRF-Token

## 环境配置

### 开发环境 (.env)
```bash
ENVIRONMENT=development
# 开发环境会自动允许以下域名：
# - http://localhost:5173
# - http://127.0.0.1:5173
# - http://localhost:3000
# - http://127.0.0.1:3000
# - http://localhost:8001
# - http://127.0.0.1:8001
```

### 生产环境 (.env.production)
```bash
ENVIRONMENT=production
PRODUCTION_FRONTEND_URL=https://your-frontend-domain.com
VERCEL_DOMAIN=your-app.vercel.app
```

## 部署到 Vercel

### 1. 设置环境变量
在 Vercel 项目设置中添加以下环境变量：

```bash
ENVIRONMENT=production
PRODUCTION_FRONTEND_URL=https://your-frontend-domain.com
VERCEL_DOMAIN=your-app.vercel.app
```

### 2. 自动检测
当部署到 Vercel 时，系统会自动：
- 检测到 `VERCEL=1` 环境变量
- 切换到生产模式
- 只允许配置的域名访问

## 安全特性

### 🔒 生产环境安全
- 只允许明确配置的域名
- 保留本地调试能力（localhost:5173）
- 防止未授权的跨域访问

### 🛠️ 开发环境便利
- 允许所有常用的本地开发端口
- 支持热重载和开发工具
- 无需频繁修改配置

## 测试 CORS 配置

### 方法 1: 使用测试页面
打开 `backend/test_cors.html` 文件在浏览器中测试各种 HTTP 方法。

### 方法 2: 浏览器开发者工具
1. 打开前端应用 (http://localhost:5173)
2. 打开浏览器开发者工具
3. 查看 Network 标签页
4. 确认没有 CORS 错误

### 方法 3: curl 命令测试
```bash
# 测试预检请求
curl -X OPTIONS http://localhost:8000/health \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: Content-Type,Authorization"

# 测试实际请求
curl -X GET http://localhost:8000/health \
  -H "Origin: http://localhost:5173" \
  -H "Content-Type: application/json"
```

## 常见问题

### Q: 为什么生产环境还允许 localhost:5173？
A: 这是为了方便开发者在本地调试生产环境的后端 API。如果不需要，可以在配置中移除。

### Q: 如何添加新的允许域名？
A: 在相应的环境变量文件中设置 `PRODUCTION_FRONTEND_URL` 或 `VERCEL_DOMAIN`。

### Q: CORS 错误仍然存在怎么办？
A: 
1. 检查环境变量是否正确设置
2. 确认后端服务器已重启
3. 清除浏览器缓存
4. 使用测试页面验证配置

## 配置文件位置

- 主配置: `backend/app/core/config.py`
- CORS 中间件: `backend/app/main.py`
- 环境变量示例: `backend/.env.example`
- 生产环境配置: `backend/.env.production`
- 测试页面: `backend/test_cors.html`

## 更新日志

- ✅ 添加智能环境检测
- ✅ 配置生产/开发环境分离
- ✅ 支持 Vercel 自动检测
- ✅ 明确指定允许的 HTTP 方法和头部
- ✅ 添加测试工具和文档