-- 更新课程主题表结构
-- 根据用户要求简化 course_topics 表，只保留必需字段

-- 首先备份现有数据（如果需要保留的话）
CREATE TABLE IF NOT EXISTS course_topics_backup AS 
SELECT id, name, created_at, updated_at FROM course_topics;

-- 删除不需要的列
ALTER TABLE course_topics DROP COLUMN IF EXISTS description;
ALTER TABLE course_topics DROP COLUMN IF EXISTS subject;
ALTER TABLE course_topics DROP COLUMN IF EXISTS grade_level;
ALTER TABLE course_topics DROP COLUMN IF EXISTS keywords;
ALTER TABLE course_topics DROP COLUMN IF EXISTS is_active;
ALTER TABLE course_topics DROP COLUMN IF EXISTS order_index;

-- 为 name 字段添加唯一约束
ALTER TABLE course_topics ADD CONSTRAINT course_topics_name_unique UNIQUE (name);

-- 确保 updated_at 字段在更新时自动更新
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为 course_topics 表创建触发器
DROP TRIGGER IF EXISTS update_course_topics_updated_at ON course_topics;
CREATE TRIGGER update_course_topics_updated_at
    BEFORE UPDATE ON course_topics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 插入一些基础的课程主题数据（如果表为空）
INSERT INTO course_topics (name) VALUES 
('语文'),
('数学'),
('英语'),
('科学'),
('历史'),
('地理'),
('物理'),
('化学'),
('生物')
ON CONFLICT (name) DO NOTHING;