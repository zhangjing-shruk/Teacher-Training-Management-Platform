-- 修复数据库 ID 类型问题
-- 将 BIGSERIAL 改为 UUID 以兼容 Supabase Auth

-- 1. 删除现有的外键约束
ALTER TABLE practice_sessions DROP CONSTRAINT IF EXISTS practice_sessions_user_id_fkey;
ALTER TABLE feedback DROP CONSTRAINT IF EXISTS feedback_session_id_fkey;
ALTER TABLE feedback DROP CONSTRAINT IF EXISTS feedback_user_id_fkey;
ALTER TABLE learning_progress DROP CONSTRAINT IF EXISTS learning_progress_user_id_fkey;
ALTER TABLE learning_progress DROP CONSTRAINT IF EXISTS learning_progress_material_id_fkey;

-- 2. 删除现有表（如果有数据，请先备份）
DROP TABLE IF EXISTS learning_progress;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS practice_sessions;
DROP TABLE IF EXISTS training_materials;
DROP TABLE IF EXISTS users;

-- 3. 重新创建用户表（使用 UUID）
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

-- 4. 重新创建培训资料表
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

-- 5. 重新创建练习会话表
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

-- 6. 重新创建反馈表
CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES practice_sessions(id) NOT NULL,
    user_id UUID REFERENCES users(id) NOT NULL,
    content TEXT NOT NULL,
    rating INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. 重新创建学习进度表
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

-- 8. 重新创建索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_practice_sessions_user_id ON practice_sessions(user_id);
CREATE INDEX idx_learning_progress_user_id ON learning_progress(user_id);
CREATE INDEX idx_feedback_session_id ON feedback(session_id);

-- 9. 重新创建更新时间戳触发器
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_training_materials_updated_at BEFORE UPDATE ON training_materials
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_practice_sessions_updated_at BEFORE UPDATE ON practice_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_learning_progress_updated_at BEFORE UPDATE ON learning_progress
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 10. 重新启用行级安全策略
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE training_materials ENABLE ROW LEVEL SECURITY;
ALTER TABLE practice_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_progress ENABLE ROW LEVEL SECURITY;

-- 11. 重新创建安全策略
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Everyone can view training materials" ON training_materials
    FOR SELECT USING (true);

CREATE POLICY "Managers can manage training materials" ON training_materials
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = auth.uid() 
            AND role = 'manager'
        )
    );

CREATE POLICY "Users can manage own sessions" ON practice_sessions
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own progress" ON learning_progress
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can view feedback for own sessions" ON feedback
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM practice_sessions 
            WHERE id = session_id 
            AND user_id = auth.uid()
        )
    );

CREATE POLICY "Managers can manage all feedback" ON feedback
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = auth.uid() 
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

-- 完成！现在数据库应该与 Supabase Auth 兼容了