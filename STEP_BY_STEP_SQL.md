# 🚀 Supabase 数据库创建步骤

## 📋 操作说明
1. 登录您的 Supabase 项目控制台
2. 点击左侧菜单的 "SQL Editor"
3. 按照下面的步骤，一步一步复制粘贴 SQL 代码并执行

---

## 第一步：创建枚举类型
**复制下面的代码，粘贴到 SQL Editor 中，点击 "RUN" 执行：**

```sql
-- 创建枚举类型
CREATE TYPE user_role AS ENUM ('teacher', 'manager');
CREATE TYPE training_status AS ENUM ('not_started', 'in_progress', 'completed');
CREATE TYPE material_type AS ENUM ('video', 'document', 'audio', 'interactive');
CREATE TYPE practice_status AS ENUM ('pending', 'in_progress', 'completed', 'reviewed');
```

---

## 第二步：创建用户表
**复制下面的代码，粘贴执行：**

```sql
-- 创建用户表
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    full_name VARCHAR NOT NULL,
    role user_role NOT NULL,
    is_active BOOLEAN DEFAULT true,
    training_status training_status DEFAULT 'not_started',
    training_progress INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 第三步：创建培训资料表
**复制下面的代码，粘贴执行：**

```sql
-- 创建培训资料表
CREATE TABLE training_materials (
    id BIGSERIAL PRIMARY KEY,
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
```

---

## 第四步：创建练习会话表
**复制下面的代码，粘贴执行：**

```sql
-- 创建练习会话表
CREATE TABLE practice_sessions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) NOT NULL,
    title VARCHAR NOT NULL,
    description TEXT,
    status practice_status DEFAULT 'pending',
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 第五步：创建反馈表
**复制下面的代码，粘贴执行：**

```sql
-- 创建反馈表
CREATE TABLE feedback (
    id BIGSERIAL PRIMARY KEY,
    session_id BIGINT REFERENCES practice_sessions(id) NOT NULL,
    user_id BIGINT REFERENCES users(id) NOT NULL,
    content TEXT NOT NULL,
    rating INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 第六步：创建学习进度表
**复制下面的代码，粘贴执行：**

```sql
-- 创建学习进度表
CREATE TABLE learning_progress (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) NOT NULL,
    material_id BIGINT REFERENCES training_materials(id) NOT NULL,
    status training_status DEFAULT 'not_started',
    progress_percentage INTEGER DEFAULT 0,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, material_id)
);
```

---

## 第七步：创建索引（提高性能）
**复制下面的代码，粘贴执行：**

```sql
-- 创建索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_practice_sessions_user_id ON practice_sessions(user_id);
CREATE INDEX idx_learning_progress_user_id ON learning_progress(user_id);
CREATE INDEX idx_feedback_session_id ON feedback(session_id);
```

---

## 第八步：启用行级安全策略
**复制下面的代码，粘贴执行：**

```sql
-- 启用行级安全策略
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE training_materials ENABLE ROW LEVEL SECURITY;
ALTER TABLE practice_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_progress ENABLE ROW LEVEL SECURITY;
```

---

## 第九步：创建基本安全策略
**复制下面的代码，粘贴执行：**

```sql
-- 用户可以查看自己的信息
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

-- 所有人可以查看培训资料
CREATE POLICY "Everyone can view training materials" ON training_materials
    FOR SELECT USING (true);

-- 用户可以管理自己的练习会话
CREATE POLICY "Users can manage own sessions" ON practice_sessions
    FOR ALL USING (auth.uid()::text = user_id::text);

-- 用户可以管理自己的学习进度
CREATE POLICY "Users can manage own progress" ON learning_progress
    FOR ALL USING (auth.uid()::text = user_id::text);

-- 用户可以管理自己的反馈
CREATE POLICY "Users can manage own feedback" ON feedback
    FOR ALL USING (auth.uid()::text = user_id::text);
```

---

## 第十步：插入测试数据（可选）
**复制下面的代码，粘贴执行：**

```sql
-- 插入测试培训资料
INSERT INTO training_materials (title, description, content_url, material_type, duration_minutes, created_by) VALUES 
('教学方法基础', '介绍基本的在线教学方法和技巧', 'https://example.com/material1', 'document', 30, 'admin'),
('课堂互动技巧', '如何在在线课堂中提高学生参与度', 'https://example.com/material2', 'video', 45, 'admin'),
('教学工具使用指南', '常用在线教学工具的使用方法', 'https://example.com/material3', 'document', 25, 'admin');
```

---

## ✅ 完成！

如果所有步骤都执行成功，您的数据库就创建好了！

### 🔍 验证数据库
您可以在 Supabase 控制台的 "Table Editor" 中查看创建的表：
- users（用户表）
- training_materials（培训资料表）
- practice_sessions（练习会话表）
- feedback（反馈表）
- learning_progress（学习进度表）

### 🚨 如果遇到错误
- 检查是否按顺序执行了所有步骤
- 确保每一步都显示 "Success" 
- 如果某一步失败，可以重新执行该步骤

### 📞 需要帮助？
如果遇到任何问题，请告诉我具体的错误信息，我会帮您解决！