-- AI教师培训平台 Supabase 数据库架构
-- 请在 Supabase SQL Editor 中执行以下语句

-- 1. 创建枚举类型
CREATE TYPE user_role AS ENUM ('teacher', 'manager');
CREATE TYPE training_status AS ENUM ('not_started', 'in_progress', 'completed');
CREATE TYPE material_type AS ENUM ('video', 'document', 'audio', 'interactive');
CREATE TYPE practice_status AS ENUM ('pending', 'in_progress', 'completed', 'reviewed');

-- 2. 创建用户表
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL,
    role user_role NOT NULL,
    is_active BOOLEAN DEFAULT true,
    
    -- 培训相关字段
    training_status training_status DEFAULT 'not_started',
    training_progress INTEGER DEFAULT 0, -- 百分比
    
    -- 时间戳
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. 创建培训资料表
CREATE TABLE training_materials (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    category VARCHAR DEFAULT '教学文档', -- 资料类别
    type material_type NOT NULL,
    file_path VARCHAR,
    url VARCHAR,
    duration_minutes INTEGER, -- 学习时长（分钟）
    order_index INTEGER DEFAULT 0, -- 排序索引
    
    -- 文件上传相关字段
    file_url VARCHAR, -- 文件访问URL
    file_size VARCHAR, -- 文件大小（格式化字符串）
    download_count INTEGER DEFAULT 0, -- 下载次数
    status VARCHAR DEFAULT 'draft', -- 状态：draft, published, archived
    
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
    
    -- 录制文件信息
    video_path VARCHAR,
    audio_path VARCHAR,
    duration_seconds INTEGER,
    
    -- AI分析结果占位符
    ai_analysis_result TEXT, -- JSON格式存储AI分析结果
    
    -- 评分
    overall_score REAL,
    pronunciation_score REAL,
    fluency_score REAL,
    content_score REAL,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. 创建反馈表
CREATE TABLE feedback (
    id BIGSERIAL PRIMARY KEY,
    practice_session_id BIGINT REFERENCES practice_sessions(id) NOT NULL,
    reviewer_id BIGINT REFERENCES users(id), -- 评审员ID，可为空（AI评审）
    
    -- 反馈内容
    content TEXT NOT NULL,
    suggestions TEXT,
    
    -- 评分详情
    pronunciation_feedback TEXT,
    fluency_feedback TEXT,
    content_feedback TEXT,
    
    -- 是否为AI生成
    is_ai_generated BOOLEAN DEFAULT false,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. 创建学习进度表
CREATE TABLE learning_progress (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) NOT NULL,
    material_id BIGINT REFERENCES training_materials(id) NOT NULL,
    
    -- 学习时间记录
    start_time TIMESTAMPTZ, -- 开始学习时间
    last_active_time TIMESTAMPTZ, -- 最后活跃时间
    total_study_seconds INTEGER DEFAULT 0, -- 总学习时长（秒）
    
    -- 学习状态
    is_completed BOOLEAN DEFAULT false, -- 是否完成
    completion_time TIMESTAMPTZ, -- 完成时间
    
    -- 时间戳
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- 唯一约束：每个用户对每个资料只能有一条进度记录
    UNIQUE(user_id, material_id)
);

-- 7. 创建索引以提高查询性能
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_training_materials_type ON training_materials(type);
CREATE INDEX idx_training_materials_status ON training_materials(status);
CREATE INDEX idx_practice_sessions_user_id ON practice_sessions(user_id);
CREATE INDEX idx_practice_sessions_status ON practice_sessions(status);
CREATE INDEX idx_feedback_practice_session_id ON feedback(practice_session_id);
CREATE INDEX idx_learning_progress_user_id ON learning_progress(user_id);
CREATE INDEX idx_learning_progress_material_id ON learning_progress(material_id);

-- 8. 创建更新时间戳的触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 9. 为需要的表创建更新时间戳触发器
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

-- 11. 创建基本的RLS策略（可根据需要调整）
-- 用户只能查看和修改自己的数据
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid()::text = id::text);

-- 所有用户都可以查看培训资料
CREATE POLICY "Everyone can view training materials" ON training_materials
    FOR SELECT USING (true);

-- 只有管理员可以管理培训资料
CREATE POLICY "Managers can manage training materials" ON training_materials
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id::text = auth.uid()::text 
            AND role = 'manager'
        )
    );

-- 用户只能查看和管理自己的练习会话
CREATE POLICY "Users can manage own practice sessions" ON practice_sessions
    FOR ALL USING (auth.uid()::text = user_id::text);

-- 用户只能查看和管理自己的学习进度
CREATE POLICY "Users can manage own learning progress" ON learning_progress
    FOR ALL USING (auth.uid()::text = user_id::text);

-- 反馈策略：用户可以查看自己练习的反馈，管理员可以管理所有反馈
CREATE POLICY "Users can view feedback for own sessions" ON feedback
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM practice_sessions 
            WHERE id = practice_session_id 
            AND user_id::text = auth.uid()::text
        )
    );

CREATE POLICY "Managers can manage all feedback" ON feedback
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id::text = auth.uid()::text 
            AND role = 'manager'
        )
    );

-- 12. 插入一些初始数据（可选）
-- 创建默认管理员账户（密码需要在应用中哈希）
INSERT INTO users (email, name, hashed_password, role) VALUES 
('admin@51talk.com', '系统管理员', '$2b$12$placeholder_hash', 'manager');

-- 创建一些示例培训资料
INSERT INTO training_materials (title, description, category, type, status) VALUES 
('教学方法基础', '介绍基本的在线教学方法和技巧', '教学方法', 'document', 'published'),
('课堂互动技巧', '如何在在线课堂中提高学生参与度', '教学技巧', 'video', 'published'),
('教学工具使用指南', '常用在线教学工具的使用方法', '技术工具', 'document', 'published');