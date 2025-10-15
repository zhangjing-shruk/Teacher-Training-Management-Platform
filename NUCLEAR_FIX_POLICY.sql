-- 核弹级策略清理 - 彻底解决递归问题
-- 这将删除所有策略并禁用所有 RLS

-- 1. 查看所有现有策略（用于调试）
-- SELECT schemaname, tablename, policyname FROM pg_policies WHERE schemaname = 'public';

-- 2. 删除 users 表的所有策略
DO $$ 
DECLARE 
    r RECORD;
BEGIN
    FOR r IN (SELECT policyname FROM pg_policies WHERE schemaname = 'public' AND tablename = 'users')
    LOOP
        EXECUTE 'DROP POLICY IF EXISTS "' || r.policyname || '" ON users';
    END LOOP;
END $$;

-- 3. 删除其他表的所有策略
DO $$ 
DECLARE 
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename, policyname FROM pg_policies WHERE schemaname = 'public' AND tablename IN ('training_materials', 'practice_sessions', 'feedback', 'learning_progress'))
    LOOP
        EXECUTE 'DROP POLICY IF EXISTS "' || r.policyname || '" ON ' || r.tablename;
    END LOOP;
END $$;

-- 4. 禁用所有表的 RLS
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE training_materials DISABLE ROW LEVEL SECURITY;
ALTER TABLE practice_sessions DISABLE ROW LEVEL SECURITY;
ALTER TABLE feedback DISABLE ROW LEVEL SECURITY;
ALTER TABLE learning_progress DISABLE ROW LEVEL SECURITY;

-- 5. 验证 - 查看剩余的策略（应该为空）
-- SELECT schemaname, tablename, policyname FROM pg_policies WHERE schemaname = 'public';

-- 完成！现在应该没有任何策略了