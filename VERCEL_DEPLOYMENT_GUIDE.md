# Vercel 部署配置指南

## 概述

AI 教师培训平台是一个多用户系统，支持教师和管理员两种角色。本指南将帮助您在 Vercel 上正确部署前端应用。

## 必需的环境变量

在 Vercel 项目设置中，您需要配置以下环境变量：

### 1. Supabase 配置（必需）

```
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
```

**获取方式：**
1. 登录 [Supabase Dashboard](https://app.supabase.com/)
2. 选择您的项目
3. 进入 Settings > API
4. 复制 Project URL 和 anon public key

### 2. API 配置（可选）

```
VITE_API_BASE_URL=https://your-backend-api-domain.com
```

**说明：**
- 如果您有独立的后端 API 服务，请设置此变量
- 如果只使用 Supabase 作为后端，可以不设置此变量

### 3. 应用配置（可选）

```
VITE_APP_NAME=AI教师培训平台
VITE_APP_VERSION=1.0.0
```

## Vercel 环境变量设置步骤

### 方法一：通过 Vercel Dashboard

1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 选择您的项目
3. 进入 Settings > Environment Variables
4. 点击 "Add New" 添加环境变量
5. 输入变量名和值
6. 选择适用的环境（Production, Preview, Development）
7. 点击 "Save"

### 方法二：通过 Vercel CLI

```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录
vercel login

# 设置环境变量
vercel env add VITE_SUPABASE_URL
vercel env add VITE_SUPABASE_ANON_KEY
vercel env add VITE_API_BASE_URL
```

## 部署后验证

部署完成后，请验证以下功能：

1. **访问主页**：确保页面正常加载
2. **注册功能**：测试用户注册流程
3. **登录功能**：测试教师和管理员登录
4. **角色权限**：确保不同角色看到不同的界面

## 常见问题解决

### 问题 1: "Backend API is not configured" 错误

**原因：** 环境变量未正确设置

**解决方案：**
1. 检查 Vercel 项目的环境变量设置
2. 确保 `VITE_SUPABASE_URL` 和 `VITE_SUPABASE_ANON_KEY` 已正确配置
3. 重新部署项目

### 问题 2: 登录后页面空白

**原因：** Supabase 数据库权限配置问题

**解决方案：**
1. 检查 Supabase 数据库的 RLS (Row Level Security) 策略
2. 确保用户表和相关表的权限配置正确

### 问题 3: 注册功能不工作

**原因：** Supabase 认证设置问题

**解决方案：**
1. 检查 Supabase 项目的 Authentication 设置
2. 确保启用了 Email 认证
3. 配置邮件模板和 SMTP 设置

## 多用户系统说明

本系统支持两种用户角色：

### 教师角色
- 查看培训材料
- 提交试讲视频
- 查看反馈报告
- 练习功能

### 管理员角色
- 管理教师账户
- 审核试讲视频
- 提供反馈评价
- 查看系统分析

## 技术架构

- **前端：** Vue.js + TypeScript + Tailwind CSS
- **后端：** Supabase (主要) + FastAPI (可选)
- **部署：** Vercel (前端) + Supabase (后端)
- **认证：** Supabase Auth

## 支持

如果遇到问题，请：

1. 检查浏览器控制台的错误信息
2. 查看 Vercel 部署日志
3. 验证 Supabase 项目配置
4. 参考本指南的常见问题解决方案

---

**注意：** 请确保不要在公开的代码仓库中提交包含敏感信息的 `.env` 文件。所有敏感配置都应该通过 Vercel 的环境变量功能进行设置。