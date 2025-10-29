#!/usr/bin/env python3
"""
为教师用户创建用户资料
使用正确的用户ID: 8fe12dc2-d648-46d8-8fce-2f772d844dce
"""

import os
import sys
from supabase import create_client, Client
from datetime import datetime

# 从环境变量获取Supabase配置
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://jmankrgaywrjsnarsbhf.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

if not SUPABASE_SERVICE_KEY:
    print("错误: 请设置 SUPABASE_SERVICE_KEY 环境变量")
    sys.exit(1)

def main():
    try:
        # 创建Supabase客户端
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        
        # 正确的用户信息
        correct_user_id = "8fe12dc2-d648-46d8-8fce-2f772d844dce"
        target_email = "1464466374@qq.com"
        
        print(f"为用户创建资料: {target_email}")
        print(f"用户ID: {correct_user_id}")
        print("=" * 60)
        
        # 1. 验证认证用户存在
        print("\n1. 验证认证用户...")
        try:
            auth_user_response = supabase.auth.admin.get_user_by_id(correct_user_id)
            
            if hasattr(auth_user_response, 'user') and auth_user_response.user:
                user = auth_user_response.user
                print(f"✓ 认证用户存在: {user.email} (ID: {user.id})")
                print(f"  创建时间: {user.created_at}")
                print(f"  邮箱验证: {user.email_confirmed_at}")
                print(f"  最后登录: {user.last_sign_in_at}")
            else:
                print("✗ 认证用户不存在")
                return
                
        except Exception as e:
            print(f"✗ 验证认证用户失败: {e}")
            return
        
        # 2. 检查是否已有用户资料
        print("\n2. 检查现有用户资料...")
        try:
            existing_profile = supabase.table('users').select('*').eq('id', correct_user_id).execute()
            
            if existing_profile.data:
                print(f"✓ 用户资料已存在: {existing_profile.data[0]}")
                print("无需创建新的用户资料")
                return
            else:
                print("✗ 用户资料不存在，需要创建")
                
        except Exception as e:
            print(f"✗ 检查用户资料失败: {e}")
        
        # 3. 创建用户资料
        print("\n3. 创建用户资料...")
        
        # 构建用户资料数据
        user_profile = {
            'id': correct_user_id,
            'email': target_email,
            'full_name': target_email.split('@')[0],  # 使用邮箱前缀作为姓名
            'role': 'teacher',
            'is_active': True,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        print(f"准备创建的用户资料: {user_profile}")
        
        try:
            insert_response = supabase.table('users').insert(user_profile).execute()
            
            if insert_response.data:
                print(f"✓ 用户资料创建成功!")
                print(f"  创建的资料: {insert_response.data[0]}")
                
                # 4. 验证创建结果
                print("\n4. 验证创建结果...")
                verify_response = supabase.table('users').select('*').eq('id', correct_user_id).execute()
                
                if verify_response.data:
                    print(f"✓ 验证成功: {verify_response.data[0]}")
                    
                    # 5. 测试用户资料查询（模拟前端的查询）
                    print("\n5. 测试用户资料查询...")
                    test_response = supabase.table('users').select('*').eq('email', target_email).execute()
                    
                    if test_response.data:
                        print(f"✓ 通过邮箱查询成功: {test_response.data[0]}")
                    else:
                        print("✗ 通过邮箱查询失败")
                        
                else:
                    print("✗ 验证失败")
                    
            else:
                print("✗ 用户资料创建失败")
                
        except Exception as e:
            print(f"✗ 创建用户资料时出错: {e}")
            
            # 检查是否是重复键错误
            if "duplicate key" in str(e).lower() or "already exists" in str(e).lower():
                print("用户资料可能已存在，重新检查...")
                verify_response = supabase.table('users').select('*').eq('id', correct_user_id).execute()
                if verify_response.data:
                    print(f"✓ 用户资料确实已存在: {verify_response.data[0]}")
        
        print("\n" + "=" * 60)
        print("用户资料创建完成！")
        print(f"现在用户 {target_email} 应该可以正常登录了")
        
    except Exception as e:
        print(f"脚本执行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()