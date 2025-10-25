# 触发Vercel重新部署

## 部署状态检查

最新代码已推送到GitHub (commit: ff47ba1)

关键修复内容：
- 修复supabaseAuth store中fetchUserProfile方法未正确暴露的问题
- 优化登录后的用户角色检查和跳转逻辑
- 确保管理员用户正确跳转到/manager界面

## 自动部署

Vercel应该会自动检测到GitHub上的新提交并触发重新部署。

如果需要手动触发部署，可以：
1. 访问Vercel Dashboard
2. 找到项目
3. 点击"Redeploy"按钮

## 验证部署

部署完成后，请：
1. 清除浏览器缓存
2. 使用管理员账号登录
3. 验证是否正确跳转到管理员界面

时间戳: $(date)