-- ========================================
-- AI教师培训平台 - 完整数据库创建脚本
-- 一次性执行版本 - 直接复制粘贴到 Supabase SQL Editor
-- ========================================

-- 1. 创建枚举类型
CREATE TYPE user_role AS ENUM ('teacher', 'manager');
CREATE TYPE training_status AS ENUM ('not_started', 'in_progress', 'completed');
CREATE TYPE material_type AS ENUM ('video', 'document', 'audio', 'interactive');
CREATE TYPE practice_status AS ENUM ('pending', 'in_progress', 'completed', 'reviewed');

-- 2. 创建用户表
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

-- 3. 创建培训资料表
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

-- 4. 创建练习会话表
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

-- 5. 创建反馈表
CREATE TABLE feedback (
    id BIGSERIAL PRIMARY KEY,
    session_id BIGINT REFERENCES practice_sessions(id) NOT NULL,
    user_id BIGINT REFERENCES users(id) NOT NULL,
    content TEXT NOT NULL,
    rating INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. 创建学习进度表
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

-- 7. 创建索引（提高查询性能）
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_practice_sessions_user_id ON practice_sessions(user_id);
CREATE INDEX idx_learning_progress_user_id ON learning_progress(user_id);
CREATE INDEX idx_feedback_session_id ON feedback(session_id);

-- 8. 创建更新时间戳的触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 9. 为表创建更新时间戳触发器
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_training_materials_updated_at BEFORE UPDATE ON training_materials
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_practice_sessions_updated_at BEFORE UPDATE ON practice_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_learning_progress_updated_at BEFORE UPDATE ON learning_progress
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 10. 启用行级安全策略 (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE training_materials ENABLE ROW LEVEL SECURITY;
ALTER TABLE practice_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_progress ENABLE ROW LEVEL SECURITY;

-- 11. 创建基本的RLS策略
-- 用户可以查看自己的信息
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

-- 用户可以更新自己的信息
CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid()::text = id::text);

-- 所有人可以查看培训资料
CREATE POLICY "Everyone can view training materials" ON training_materials
    FOR SELECT USING (true);

-- 管理员可以管理培训资料
CREATE POLICY "Managers can manage training materials" ON training_materials
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id::text = auth.uid()::text 
            AND role = 'manager'
        )
    );

-- 用户可以管理自己的练习会话
CREATE POLICY "Users can manage own sessions" ON practice_sessions
    FOR ALL USING (auth.uid()::text = user_id::text);

-- 用户可以管理自己的学习进度
CREATE POLICY "Users can manage own progress" ON learning_progress
    FOR ALL USING (auth.uid()::text = user_id::text);

-- 用户可以查看自己练习的反馈
CREATE POLICY "Users can view feedback for own sessions" ON feedback
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM practice_sessions 
            WHERE id = session_id 
            AND user_id::text = auth.uid()::text
        )
    );

-- 管理员可以管理所有反馈
CREATE POLICY "Managers can manage all feedback" ON feedback
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id::text = auth.uid()::text 
            AND role = 'manager'
        )
    );

-- 12. 插入测试数据
INSERT INTO training_materials (title, description, content_url, material_type, duration_minutes, created_by) VALUES 
('教学方法基础', '介绍基本的在线教学方法和技巧', 'https://example.com/material1', 'document', 30, 'admin'),
('课堂互动技巧', '如何在在线课堂中提高学生参与度', 'https://example.com/material2', 'video', 45, 'admin'),
('教学工具使用指南', '常用在线教学工具的使用方法', 'https://example.com/material3', 'document', 25, 'admin'),
('发音训练课程', '英语发音技巧和练习方法', 'https://example.com/material4', 'audio', 60, 'admin'),
('互动教学游戏', '适合在线课堂的互动游戏集合', 'https://example.com/material5', 'interactive', 40, 'admin');

-- ========================================
-- 执行完成！
-- 您的数据库已经创建完毕，包含以下表：
-- - users (用户表)
-- - training_materials (培训资料表)
-- - practice_sessions (练习会话表)
-- - feedback (反馈表)
-- - learning_progress (学习进度表)
-- ========================================