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

# 创建 Supabase 客户端
supabase: Client = create_client(url, key)

# 要创建的用户
users_to_create = [
    {
        "email": "teacher1@example.com",
        "password": "teacher123",
        "full_name": "教师用户",
        "role": "teacher"
    },
    {
        "email": "admin@example.com", 
        "password": "admin123",
        "full_name": "管理员用户",
        "role": "manager"
    }
]

for user_data in users_to_create:
    try:
        print(f"创建用户: {user_data['email']}")
        
        # 创建 Auth 用户
        auth_response = supabase.auth.admin.create_user({
            "email": user_data["email"],
            "password": user_data["password"],
            "email_confirm": True
        })
        
        print(f"  Auth 用户创建成功: {auth_response.user.id}")
        
        # 创建或更新 public.users 记录
        public_user_data = {
            "id": auth_response.user.id,
            "email": user_data["email"],
            "full_name": user_data["full_name"],
            "role": user_data["role"],
            "status": "active"
        }
        
        # 先检查是否已存在
        existing = supabase.table('users').select('*').eq('email', user_data['email']).execute()
        
        if existing.data:
            # 更新现有记录
            result = supabase.table('users').update(public_user_data).eq('email', user_data['email']).execute()
            print(f"  Public 用户更新成功")
        else:
            # 创建新记录
            result = supabase.table('users').insert(public_user_data).execute()
            print(f"  Public 用户创建成功")
            
    except Exception as e:
        print(f"  创建用户失败: {e}")
        
print("\n用户创建完成！")
