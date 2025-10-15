-- 修复递归策略问题
-- 简化策略，避免无限递归

-- 1. 删除所有现有的用户表策略
DROP POLICY IF EXISTS "Users can insert own profile" ON users;
DROP POLICY IF EXISTS "Users can view own profile" ON users;
DROP POLICY IF EXISTS "Users can update own profile" ON users;
DROP POLICY IF EXISTS "Managers can view all users" ON users;
DROP POLICY IF EXISTS "Managers can update all users" ON users;

-- 2. 创建简化的策略，避免递归查询
-- 允许用户插入自己的资料（注册时）
CREATE POLICY "Enable insert for users based on user_id" ON users
    FOR INSERT WITH CHECK (auth.uid() = id);

-- 允许用户查看自己的资料
CREATE POLICY "Enable select for users based on user_id" ON users
    FOR SELECT USING (auth.uid() = id);

-- 允许用户更新自己的资料
CREATE POLICY "Enable update for users based on user_id" ON users
    FOR UPDATE USING (auth.uid() = id);

-- 3. 暂时禁用其他表的复杂策略，使用简单策略
-- 练习会话 - 简化策略
DROP POLICY IF EXISTS "Users can manage own sessions" ON practice_sessions;
CREATE POLICY "Enable all for practice_sessions based on user_id" ON practice_sessions
    FOR ALL USING (auth.uid() = user_id);

-- 学习进度 - 简化策略
DROP POLICY IF EXISTS "Users can manage own progress" ON learning_progress;
CREATE POLICY "Enable all for learning_progress based on user_id" ON learning_progress
    FOR ALL USING (auth.uid() = user_id);

-- 反馈 - 简化策略
DROP POLICY IF EXISTS "Users can view feedback for own sessions" ON feedback;
DROP POLICY IF EXISTS "Users can create feedback for own sessions" ON feedback;
DROP POLICY IF EXISTS "Managers can manage all feedback" ON feedback;

CREATE POLICY "Enable all for feedback based on user_id" ON feedback
    FOR ALL USING (auth.uid() = user_id);

-- 完成！现在策略应该不会有递归问题了