#!/usr/bin/env python3
"""
清理Supabase Auth中的所有用户
"""
import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def get_auth_users():
    """获取所有Auth用户"""
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    }
    
    auth_url = f"{SUPABASE_URL}/auth/v1/admin/users"
    response = requests.get(auth_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('users', [])
    else:
        print(f"❌ 获取用户失败: {response.status_code}")
        print(f"响应: {response.text}")
        return []

def delete_auth_user(user_id):
    """删除单个Auth用户"""
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    }
    
    delete_url = f"{SUPABASE_URL}/auth/v1/admin/users/{user_id}"
    response = requests.delete(delete_url, headers=headers)
    
    return response.status_code == 200

def cleanup_all_auth_users():
    """清理所有Auth用户"""
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        print("❌ 缺少Supabase配置信息")
        return
    
    print("🔍 获取所有Auth用户...")
    users = get_auth_users()
    
    if not users:
        print("✅ 没有找到需要清理的用户")
        return
    
    print(f"📊 找到 {len(users)} 个用户需要清理:")
    for user in users:
        print(f"  - {user.get('email')} (ID: {user.get('id')})")
    
    # 确认删除
    confirm = input(f"\n⚠️  确认删除所有 {len(users)} 个用户吗？(输入 'YES' 确认): ")
    if confirm != "YES":
        print("❌ 操作已取消")
        return
    
    print("\n🗑️  开始删除用户...")
    success_count = 0
    
    for user in users:
        user_id = user.get('id')
        email = user.get('email')
        
        print(f"删除用户: {email}...", end=" ")
        
        if delete_auth_user(user_id):
            print("✅ 成功")
            success_count += 1
        else:
            print("❌ 失败")
    
    print(f"\n📊 清理完成: 成功删除 {success_count}/{len(users)} 个用户")

if __name__ == "__main__":
    print("🧹 Supabase Auth 用户清理工具")
    print("=" * 50)
    cleanup_all_auth_users()