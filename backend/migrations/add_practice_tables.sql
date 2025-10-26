-- 添加练习模式表
CREATE TABLE IF NOT EXISTS practice_modes (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    duration_minutes INTEGER DEFAULT 30,
    difficulty_level VARCHAR DEFAULT 'beginner',
    is_active BOOLEAN DEFAULT TRUE,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- 添加课程主题表
CREATE TABLE IF NOT EXISTS course_topics (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    subject VARCHAR,
    grade_level VARCHAR,
    keywords TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- 添加评估重点表
CREATE TABLE IF NOT EXISTS evaluation_focus (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    category VARCHAR,
    weight FLOAT DEFAULT 1.0,
    criteria TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- 插入默认练习模式数据
INSERT INTO practice_modes (name, description, duration_minutes, difficulty_level, order_index) VALUES
('自由练习', '自由选择主题进行试讲练习，适合日常训练', 30, 'beginner', 1),
('模拟课堂', '模拟真实课堂环境，包含学生互动环节', 45, 'intermediate', 2),
('专题训练', '针对特定教学技能进行专项训练', 20, 'intermediate', 3),
('考核模式', '按照正式考核标准进行评估', 60, 'advanced', 4);

-- 插入默认课程主题数据
INSERT INTO course_topics (name, description, subject, grade_level, keywords, order_index) VALUES
('数学基础概念', '小学数学基础概念教学', '数学', '小学', '["加减法", "乘除法", "基础概念"]', 1),
('语文阅读理解', '语文阅读理解技巧教学', '语文', '小学', '["阅读", "理解", "技巧"]', 2),
('英语口语交流', '英语日常口语交流教学', '英语', '小学', '["口语", "交流", "日常用语"]', 3),
('科学实验探索', '科学实验方法和探索精神培养', '科学', '小学', '["实验", "探索", "科学方法"]', 4),
('历史文化传承', '中国历史文化知识传授', '历史', '小学', '["历史", "文化", "传承"]', 5);

-- 插入默认评估重点数据
INSERT INTO evaluation_focus (name, description, category, weight, criteria, order_index) VALUES
('发音准确性', '评估教师发音的准确性和清晰度', 'pronunciation', 1.0, '["发音清晰", "语调自然", "语速适中"]', 1),
('语言流畅性', '评估教师语言表达的流畅程度', 'fluency', 1.0, '["表达流畅", "逻辑清晰", "用词准确"]', 2),
('教学内容', '评估教学内容的准确性和完整性', 'content', 1.5, '["内容准确", "结构完整", "重点突出"]', 3),
('课堂互动', '评估与学生的互动效果', 'interaction', 1.2, '["互动自然", "引导有效", "回应及时"]', 4),
('教学方法', '评估教学方法的有效性', 'content', 1.3, '["方法得当", "形式多样", "效果明显"]', 5);