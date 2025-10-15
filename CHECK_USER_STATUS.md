# 🔍 用户状态检查指南

## 🚨 当前问题

错误 `PGRST116` 表示：
- ✅ Supabase Auth 中用户存在（可以登录）
- ❌ `users` 表中没有对应的用户资料

## 🔧 解决方案

### 方案1：重新注册（推荐）

1. **清除当前用户**
   - 在浏览器中按 F12 打开开发者工具
   - 进入 Application/Storage 标签
   - 清除 localStorage 和 sessionStorage
   - 刷新页面

2. **重新注册**
   - 使用不同的邮箱地址
   - 例如：teacher2@test.com
   - 密码：123456
   - 角色：教师

### 方案2：手动创建用户资料

在 Supabase SQL Editor 中执行：

```sql
-- 查看当前 Auth 用户
SELECT id, email FROM auth.users;

-- 为现有用户创建资料（替换 YOUR_USER_ID 为实际的用户ID）
INSERT INTO users (id, email, full_name, role, is_active) 
VALUES (
  'YOUR_USER_ID',  -- 从上面查询结果复制用户ID
  'teacher@test.com',
  '测试教师',
  'teacher',
  true
);
```

### 方案3：清理并重新开始

```sql
-- 删除所有测试用户（谨慎使用）
DELETE FROM auth.users WHERE email LIKE '%test.com';
DELETE FROM users WHERE email LIKE '%test.com';
```

## 🧪 测试步骤

1. **选择上述方案之一执行**
2. **重新注册用户**
3. **测试登录功能**

## 🎯 预期结果

- ✅ 注册成功
- ✅ 登录成功
- ✅ 自动跳转到对应界面
- ✅ 没有错误信息

## 📞 如果还有问题

请告诉我：
1. 选择了哪个方案
2. 执行结果如何
3. 是否还有错误信息