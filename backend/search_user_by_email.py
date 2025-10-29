#!/usr/bin/env python3
"""
通过邮箱搜索用户的详细脚本
使用Supabase管理API查找用户
"""

import os
import sys
import requests
from datetime import datetime

# 从环境变量获取Supabase配置
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://jmankrgaywrjsnarsbhf.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

if not SUPABASE_SERVICE_KEY:
    print("错误: 请设置 SUPABASE_SERVICE_KEY 环境变量")
    sys.exit(1)

def search_users_by_email(email):
    """使用Supabase管理API搜索用户"""
    
    # Supabase管理API端点
    admin_url = f"{SUPABASE_URL}/auth/v1/admin/users"
    
    headers = {
        'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
        'Content-Type': 'application/json',
        'apikey': SUPABASE_SERVICE_KEY
    }
    
    try:
        # 获取所有用户
        response = requests.get(admin_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            users = data.get('users', [])
            
            print(f"总共找到 {len(users)} 个认证用户")
            
            # 搜索目标邮箱
            target_users = []
            for user in users:
                if user.get('email') == email:
                    target_users.append(user)
                    
            return target_users, users
        else:
            print(f"API请求失败: {response.status_code} - {response.text}")
            return [], []
            
    except Exception as e:
        print(f"搜索用户失败: {e}")
        return [], []

def main():
    target_email = "1464466374@qq.com"
    
    print(f"搜索邮箱: {target_email}")
    print("=" * 60)
    
    # 搜索用户
    target_users, all_users = search_users_by_email(target_email)
    
    if target_users:
        print(f"\n✓ 找到 {len(target_users)} 个匹配的用户:")
        for i, user in enumerate(target_users):
            print(f"\n用户 {i+1}:")
            print(f"  ID: {user.get('id')}")
            print(f"  邮箱: {user.get('email')}")
            print(f"  创建时间: {user.get('created_at')}")
            print(f"  邮箱验证时间: {user.get('email_confirmed_at')}")
            print(f"  最后登录: {user.get('last_sign_in_at')}")
            print(f"  用户元数据: {user.get('user_metadata', {})}")
    else:
        print(f"\n✗ 未找到邮箱为 {target_email} 的用户")
        
        # 显示所有用户的邮箱，看看是否有相似的
        print(f"\n所有用户的邮箱列表:")
        for i, user in enumerate(all_users):
            email = user.get('email', 'N/A')
            user_id = user.get('id', 'N/A')
            print(f"  {i+1}. {email} (ID: {user_id})")
            
            # 检查是否有相似的邮箱
            if target_email.lower() in email.lower() or email.lower() in target_email.lower():
                print(f"    ⚠️  相似邮箱!")

if __name__ == "__main__":
    main()