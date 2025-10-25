#!/usr/bin/env python3
"""
检查Supabase数据库中的用户数据
"""
import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def check_supabase_users():
    """检查Supabase数据库中的用户"""
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        print("❌ 缺少Supabase配置信息")
        return
    
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # 查询users表
        users_url = f"{SUPABASE_URL}/rest/v1/users"
        response = requests.get(users_url, headers=headers)
        
        if response.status_code == 200:
            users = response.json()
            print(f"📊 Supabase数据库中共有 {len(users)} 个用户:")
            
            for user in users:
                print(f"- ID: {user.get('id')}")
                print(f"  邮箱: {user.get('email')}")
                print(f"  姓名: {user.get('name', 'N/A')}")
                print(f"  角色: {user.get('role', 'N/A')}")
                print(f"  创建时间: {user.get('created_at', 'N/A')}")
                print()
        else:
            print(f"❌ 查询失败: {response.status_code}")
            print(f"响应: {response.text}")
            
    except Exception as e:
        print(f"❌ 检查用户时出错: {e}")

if __name__ == "__main__":
    print("🔍 检查Supabase数据库用户状态...")
    check_supabase_users()