# 🔧 注册问题修复指南

## 🚨 问题分析

您遇到的错误有两个原因：

1. **数据库 ID 类型不匹配**: Supabase Auth 使用 UUID，但我们的表使用 BIGSERIAL
2. **邮件验证问题**: Supabase 默认需要邮件验证，但配置不正确

## ✅ 解决方案

### 第一步：修复数据库表结构

**在 Supabase SQL Editor 中执行以下 SQL：**

```sql
-- 删除现有的外键约束
ALTER TABLE practice_sessions DROP CONSTRAINT IF EXISTS practice_sessions_user_id_fkey;
ALTER TABLE feedback DROP CONSTRAINT IF EXISTS feedback_session_id_fkey;
ALTER TABLE feedback DROP CONSTRAINT IF EXISTS feedback_user_id_fkey;
ALTER TABLE learning_progress DROP CONSTRAINT IF EXISTS learning_progress_user_id_fkey;
ALTER TABLE learning_progress DROP CONSTRAINT IF EXISTS learning_progress_material_id_fkey;

-- 删除现有表
DROP TABLE IF EXISTS learning_progress;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS practice_sessions;
DROP TABLE IF EXISTS training_materials;
DROP TABLE IF EXISTS users;

-- 重新创建用户表（使用 UUID）
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR UNIQUE NOT NULL,
    full_name VARCHAR NOT NULL,
    role user_role NOT NULL,
    is_active BOOLEAN DEFAULT true,
    training_status training_status DEFAULT 'not_started',
    training_progress INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 重新创建培训资料表
CREATE TABLE training_materials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR NOT NULL,
    description TEXT,
    content_url VARCHAR,
    material_type material_type NOT NULL,
    duration_minutes INTEGER,
    download_count INTEGER DEFAULT 0,
    created_by VARCHAR,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 重新创建练习会话表
CREATE TABLE practice_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) NOT NULL,
    title VARCHAR NOT NULL,
    description TEXT,
    status practice_status DEFAULT 'pending',
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 重新创建反馈表
CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES practice_sessions(id) NOT NULL,
    user_id UUID REFERENCES users(id) NOT NULL,
    content TEXT NOT NULL,
    rating INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 重新创建学习进度表
CREATE TABLE learning_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) NOT NULL,
    material_id UUID REFERENCES training_materials(id) NOT NULL,
    status training_status DEFAULT 'not_started',
    progress_percentage INTEGER DEFAULT 0,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, material_id)
);

-- 重新启用行级安全策略
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE training_materials ENABLE ROW LEVEL SECURITY;
ALTER TABLE practice_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_progress ENABLE ROW LEVEL SECURITY;

-- 重新创建安全策略
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Everyone can view training materials" ON training_materials
    FOR SELECT USING (true);

-- 插入测试数据
INSERT INTO training_materials (title, description, content_url, material_type, duration_minutes, created_by) VALUES 
('教学方法基础', '介绍基本的在线教学方法和技巧', 'https://example.com/material1', 'document', 30, 'admin'),
('课堂互动技巧', '如何在在线课堂中提高学生参与度', 'https://example.com/material2', 'video', 45, 'admin'),
('教学工具使用指南', '常用在线教学工具的使用方法', 'https://example.com/material3', 'document', 25, 'admin');
```

### 第二步：配置 Supabase 邮件验证

**在 Supabase 控制台中：**

1. 进入 **Authentication** → **Settings**
2. 找到 **Email Auth** 部分
3. **关闭** "Confirm email" 选项
4. 保存设置

### 第三步：测试注册

现在您可以：

1. 访问 http://localhost:5173/register
2. 填写注册信息：
   - 姓名：测试用户
   - 邮箱：test@example.com
   - 密码：123456
   - 角色：教师
3. 点击注册

应该能够成功注册并自动登录！

## 🎯 验证成功

如果看到以下情况，说明修复成功：

- ✅ 注册时没有错误信息
- ✅ 不需要邮件验证
- ✅ 自动跳转到对应角色的界面
- ✅ 能够正常使用系统功能

## 🚨 如果还有问题

请提供：
1. 具体的错误信息
2. 浏览器控制台的日志
3. Supabase 控制台的错误信息

我会立即帮您解决！

## 📝 注意事项

- 这个修复会清空现有的用户数据
- 如果您已经有重要数据，请先备份
- 修复后需要重新注册用户账户