#!/usr/bin/env python3
"""
为 zhangjing32@51talk.com 创建管理员账号
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Supabase 配置
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not url or not key:
    print("❌ 错误：缺少 Supabase 配置")
    exit(1)

print(f"🔗 连接到 Supabase: {url}")

# 创建 Supabase 客户端
supabase: Client = create_client(url, key)

# 管理员账号信息
admin_data = {
    "email": "zhangjing32@51talk.com",
    "password": "admin123456",  # 请在创建后修改密码
    "full_name": "张静 - 管理员",
    "role": "manager"
}

try:
    print(f"🔨 创建管理员账号: {admin_data['email']}")
    
    # 1. 先检查是否已存在 Auth 用户
    try:
        existing_auth = supabase.auth.admin.list_users()
        existing_emails = [user.email for user in existing_auth]
        
        if admin_data["email"] in existing_emails:
            print(f"⚠️  Auth 用户已存在，跳过创建")
            # 获取现有用户ID
            auth_user = next(user for user in existing_auth if user.email == admin_data["email"])
            user_id = auth_user.id
        else:
            # 创建 Auth 用户
            auth_response = supabase.auth.admin.create_user({
                "email": admin_data["email"],
                "password": admin_data["password"],
                "email_confirm": True
            })
            user_id = auth_response.user.id
            print(f"✅ Auth 用户创建成功: {user_id}")
            
    except Exception as auth_error:
        print(f"❌ Auth 用户创建失败: {auth_error}")
        raise
    
    # 2. 创建或更新 public.users 记录
    public_user_data = {
        "id": user_id,
        "email": admin_data["email"],
        "full_name": admin_data["full_name"],
        "role": admin_data["role"],
        "is_active": True,
        "created_at": "now()",
        "updated_at": "now()"
    }
    
    # 检查 public.users 表是否已存在
    existing_public = supabase.table('users').select('*').eq('email', admin_data['email']).execute()
    
    if existing_public.data:
        # 更新现有记录
        result = supabase.table('users').update({
            "full_name": admin_data["full_name"],
            "role": admin_data["role"],
            "is_active": True,
            "updated_at": "now()"
        }).eq('email', admin_data['email']).execute()
        print(f"✅ Public 用户记录更新成功")
    else:
        # 创建新记录
        result = supabase.table('users').insert(public_user_data).execute()
        print(f"✅ Public 用户记录创建成功")
    
    print(f"\n🎉 管理员账号创建完成！")
    print(f"📧 邮箱: {admin_data['email']}")
    print(f"🔑 密码: {admin_data['password']}")
    print(f"👤 角色: {admin_data['role']}")
    print(f"\n⚠️  请登录后立即修改密码！")
        
except Exception as e:
    print(f"❌ 创建管理员账号失败: {e}")
    import traceback
    traceback.print_exc()