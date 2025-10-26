# Supabase Storage 设置指南

## 🎯 目标
为 AI 教师培训平台设置 Supabase Storage，用于存储和访问培训资料文件。

## 📋 前提条件
- 已有 Supabase 项目
- 已配置好 Supabase 环境变量

## 🚀 设置步骤

### 第一步：登录 Supabase 控制台
1. 访问 [Supabase Dashboard](https://app.supabase.com/)
2. 登录您的账户
3. 选择您的项目

### 第二步：创建 Storage Bucket
1. 在左侧菜单中点击 **"Storage"**
2. 点击 **"Create a new bucket"** 按钮
3. 填写以下信息：
   - **Bucket name**: `training-materials`
   - **Public bucket**: ✅ **勾选** (允许公开访问)
   - **File size limit**: `100 MB`
   - **Allowed MIME types**: 保持默认或添加以下类型：
     ```
     application/pdf
     application/msword
     application/vnd.openxmlformats-officedocument.wordprocessingml.document
     application/vnd.ms-powerpoint
     application/vnd.openxmlformats-officedocument.presentationml.presentation
     video/mp4
     video/avi
     video/mov
     audio/mp3
     audio/wav
     audio/mpeg
     image/jpeg
     image/png
     image/gif
     ```
4. 点击 **"Create bucket"**

### 第三步：配置 Bucket 策略（可选）
如果需要更细粒度的访问控制，可以在 **"Policies"** 标签中配置 RLS 策略。

对于公开访问的培训资料，建议使用以下策略：

```sql
-- 允许所有人读取文件
CREATE POLICY "Public Access" ON storage.objects FOR SELECT USING (bucket_id = 'training-materials');

-- 允许认证用户上传文件
CREATE POLICY "Authenticated users can upload" ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'training-materials' AND auth.role() = 'authenticated');

-- 允许认证用户删除自己上传的文件
CREATE POLICY "Users can delete own files" ON storage.objects FOR DELETE USING (bucket_id = 'training-materials' AND auth.uid() = owner);
```

## ✅ 验证设置
1. 在前端应用中尝试上传一个测试文件
2. 检查文件是否出现在 Supabase Storage 中
3. 尝试预览上传的文件

## 🔧 故障排除

### 问题：无法创建 bucket
**解决方案**：
- 检查您是否有项目的管理员权限
- 确保 bucket 名称唯一且符合命名规范

### 问题：文件上传失败
**解决方案**：
- 检查文件大小是否超过限制
- 验证文件类型是否在允许列表中
- 检查网络连接

### 问题：无法访问上传的文件
**解决方案**：
- 确保 bucket 设置为公开
- 检查 RLS 策略配置
- 验证文件 URL 格式

## 📞 需要帮助？
如果遇到任何问题，请：
1. 检查 Supabase 控制台的错误日志
2. 查看浏览器开发者工具的网络请求
3. 联系技术支持并提供具体错误信息

## 🎉 完成！
设置完成后，您的 AI 教师培训平台将能够：
- ✅ 上传培训资料到云存储
- ✅ 在生产环境中正常预览文件
- ✅ 提供稳定的文件访问服务