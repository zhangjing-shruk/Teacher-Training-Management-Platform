-- 彻底解决递归策略问题
-- 暂时禁用 RLS 或使用最简单的策略

-- 方案1：暂时禁用 RLS（推荐用于开发测试）
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE training_materials DISABLE ROW LEVEL SECURITY;
ALTER TABLE practice_sessions DISABLE ROW LEVEL SECURITY;
ALTER TABLE feedback DISABLE ROW LEVEL SECURITY;
ALTER TABLE learning_progress DISABLE ROW LEVEL SECURITY;

-- 删除所有现有策略
DROP POLICY IF EXISTS "Enable insert for users based on user_id" ON users;
DROP POLICY IF EXISTS "Enable select for users based on user_id" ON users;
DROP POLICY IF EXISTS "Enable update for users based on user_id" ON users;
DROP POLICY IF EXISTS "Enable all for practice_sessions based on user_id" ON practice_sessions;
DROP POLICY IF EXISTS "Enable all for learning_progress based on user_id" ON learning_progress;
DROP POLICY IF EXISTS "Enable all for feedback based on user_id" ON feedback;
DROP POLICY IF EXISTS "Everyone can view training materials" ON training_materials;
DROP POLICY IF EXISTS "Managers can manage training materials" ON training_materials;

-- 注意：禁用 RLS 后，所有用户都可以访问所有数据
-- 这适合开发和测试环境
-- 生产环境中需要重新启用并配置正确的策略