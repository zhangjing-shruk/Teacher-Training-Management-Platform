import os
from supabase import create_client, Client
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Supabase 配置
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not url or not key:
    print("错误：缺少 Supabase 配置")
    exit(1)

print(f"Supabase URL: {url}")
print(f"Service Role Key: {key[:20]}...")

# 创建 Supabase 客户端
supabase: Client = create_client(url, key)

try:
    # 检查 auth.users 表
    response = supabase.auth.admin.list_users()
    print(f"Supabase Auth 用户数量: {len(response)}")
    
    for user in response:
        print(f"- ID: {user.id}")
        print(f"  邮箱: {user.email}")
        print(f"  创建时间: {user.created_at}")
        print()
        
except Exception as e:
    print(f"检查 Auth 用户错误: {e}")

try:        
    # 检查 public.users 表
    users_response = supabase.table('users').select('*').execute()
    print(f"Public.users 表用户数量: {len(users_response.data)}")
    
    for user in users_response.data:
        print(f"- ID: {user['id']}")
        print(f"  邮箱: {user['email']}")
        print(f"  姓名: {user['full_name']}")
        print(f"  角色: {user['role']}")
        print()
        
except Exception as e:
    print(f"检查 Public 用户错误: {e}")
