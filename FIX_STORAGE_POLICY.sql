-- 修复 Supabase Storage 行级安全策略
-- 解决 "new row violates row-level security policy" 错误

-- 1. 删除现有的 Storage 策略（如果存在）
DROP POLICY IF EXISTS "Public Access" ON storage.objects;
DROP POLICY IF EXISTS "Authenticated users can upload" ON storage.objects;
DROP POLICY IF EXISTS "Users can delete own files" ON storage.objects;
DROP POLICY IF EXISTS "Allow public read access" ON storage.objects;
DROP POLICY IF EXISTS "Allow authenticated uploads" ON storage.objects;
DROP POLICY IF EXISTS "Allow authenticated deletes" ON storage.objects;

-- 2. 创建新的 Storage 策略
-- 允许所有人读取 training-materials bucket 中的文件
CREATE POLICY "Allow public read access to training-materials" 
ON storage.objects FOR SELECT 
USING (bucket_id = 'training-materials');

-- 允许认证用户上传文件到 training-materials bucket
CREATE POLICY "Allow authenticated uploads to training-materials" 
ON storage.objects FOR INSERT 
WITH CHECK (
    bucket_id = 'training-materials' 
    AND auth.role() = 'authenticated'
);

-- 允许认证用户更新文件到 training-materials bucket
CREATE POLICY "Allow authenticated updates to training-materials" 
ON storage.objects FOR UPDATE 
USING (
    bucket_id = 'training-materials' 
    AND auth.role() = 'authenticated'
);

-- 允许认证用户删除 training-materials bucket 中的文件
CREATE POLICY "Allow authenticated deletes from training-materials" 
ON storage.objects FOR DELETE 
USING (
    bucket_id = 'training-materials' 
    AND auth.role() = 'authenticated'
);

-- 3. 确保 Storage buckets 表也有正确的策略
-- 允许认证用户查看 buckets
CREATE POLICY IF NOT EXISTS "Allow authenticated users to view buckets" 
ON storage.buckets FOR SELECT 
USING (auth.role() = 'authenticated');

-- 允许认证用户创建 buckets（如果需要）
CREATE POLICY IF NOT EXISTS "Allow authenticated users to create buckets" 
ON storage.buckets FOR INSERT 
WITH CHECK (auth.role() = 'authenticated');

-- 4. 验证策略
-- 查看当前的 Storage 策略
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual 
FROM pg_policies 
WHERE schemaname = 'storage' 
ORDER BY tablename, policyname;