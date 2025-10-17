#!/usr/bin/env python3
"""
修复缺失的用户配置文件
为在 Supabase Auth 中存在但在 users 表中缺失的用户创建记录
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def main():
    # 初始化 Supabase 客户端
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        print("错误: 缺少 Supabase 配置")
        return
    
    supabase: Client = create_client(url, key)
    
    # 缺失的用户信息
    missing_user_id = "b9469539-0d7d-4af6-a92e-ccaeeb23c65d"
    missing_user_email = "zhangjing32@51talk.com"
    
    try:
        # 检查用户是否已存在
        existing_user = supabase.table('users').select('*').eq('id', missing_user_id).execute()
        
        if existing_user.data:
            print(f"用户 {missing_user_email} 已存在于 users 表中")
            return
        
        # 创建用户记录
        user_data = {
            'id': missing_user_id,
            'email': missing_user_email,
            'full_name': '张静',  # 根据邮箱推测的姓名
            'role': 'teacher',   # 默认角色为教师
            'is_active': True,
            'created_at': '2025-10-14T22:17:27.770614+00:00'  # 使用认证创建时间
        }
        
        result = supabase.table('users').insert(user_data).execute()
        
        if result.data:
            print(f"✅ 成功为用户 {missing_user_email} 创建配置文件")
            print(f"   用户ID: {missing_user_id}")
            print(f"   姓名: {user_data['full_name']}")
            print(f"   角色: {user_data['role']}")
        else:
            print(f"❌ 创建用户配置文件失败")
            
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    main()