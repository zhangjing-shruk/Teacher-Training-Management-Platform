-- 修复行级安全策略问题
-- 允许用户注册时创建自己的资料

-- 1. 删除现有的用户表策略
DROP POLICY IF EXISTS "Users can view own profile" ON users;
DROP POLICY IF EXISTS "Users can update own profile" ON users;

-- 2. 创建新的策略，允许用户注册和管理自己的资料
-- 允许用户插入自己的资料（注册时）
CREATE POLICY "Users can insert own profile" ON users
    FOR INSERT WITH CHECK (auth.uid() = id);

-- 允许用户查看自己的资料
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid() = id);

-- 允许用户更新自己的资料
CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid() = id);

-- 3. 允许管理员查看和管理所有用户
CREATE POLICY "Managers can view all users" ON users
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = auth.uid() 
            AND role = 'manager'
        )
    );

CREATE POLICY "Managers can update all users" ON users
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = auth.uid() 
            AND role = 'manager'
        )
    );

-- 4. 修复其他表的策略
-- 练习会话策略
DROP POLICY IF EXISTS "Users can manage own sessions" ON practice_sessions;
CREATE POLICY "Users can manage own sessions" ON practice_sessions
    FOR ALL USING (auth.uid() = user_id);

-- 学习进度策略
DROP POLICY IF EXISTS "Users can manage own progress" ON learning_progress;
CREATE POLICY "Users can manage own progress" ON learning_progress
    FOR ALL USING (auth.uid() = user_id);

-- 反馈策略
DROP POLICY IF EXISTS "Users can view feedback for own sessions" ON feedback;
DROP POLICY IF EXISTS "Managers can manage all feedback" ON feedback;

CREATE POLICY "Users can view feedback for own sessions" ON feedback
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM practice_sessions 
            WHERE id = session_id 
            AND user_id = auth.uid()
        )
    );

CREATE POLICY "Users can create feedback for own sessions" ON feedback
    FOR INSERT WITH CHECK (
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

-- 完成！现在用户应该能够正常注册和使用系统了