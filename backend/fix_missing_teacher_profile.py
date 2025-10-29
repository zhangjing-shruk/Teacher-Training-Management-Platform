#!/usr/bin/env python3
"""
诊断和修复教师用户问题
全面检查认证用户和数据库状态
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
        
        # 目标用户信息
        target_user_id = "8f6f2dc2-8648-46d8-8fce-2f772d844dce"
        target_email = "1464466374@qq.com"
        
        print(f"诊断用户 {target_email} (ID: {target_user_id})")
        print("=" * 60)
        
        # 1. 直接检查目标用户ID的认证用户
        print("\n1. 检查认证用户...")
        try:
            # 直接通过ID查找用户
            auth_user_response = supabase.auth.admin.get_user_by_id(target_user_id)
            
            target_auth_user = None
            if hasattr(auth_user_response, 'user') and auth_user_response.user:
                user = auth_user_response.user
                if user.email == target_email:
                    target_auth_user = user
                    print(f"✓ 找到认证用户: {user.email} (ID: {user.id})")
                    print(f"  创建时间: {user.created_at}")
                    print(f"  邮箱验证: {user.email_confirmed_at}")
                else:
                    print(f"✗ 用户ID {target_user_id} 对应的邮箱是 {user.email}，不是 {target_email}")
            else:
                print(f"✗ 未找到ID为 {target_user_id} 的认证用户")
                
                # 尝试通过邮箱搜索
                print(f"\n尝试通过邮箱搜索...")
                try:
                    # 查询users表找到可能的用户
                    users_with_email = supabase.table('users').select('*').eq('email', target_email).execute()
                    if users_with_email.data:
                        for user_profile in users_with_email.data:
                            print(f"  在users表中找到: {user_profile['email']} (ID: {user_profile['id']})")
                            # 尝试用这个ID查找认证用户
                            try:
                                auth_check = supabase.auth.admin.get_user_by_id(user_profile['id'])
                                if hasattr(auth_check, 'user') and auth_check.user:
                                    target_auth_user = auth_check.user
                                    target_user_id = user_profile['id']  # 更新目标用户ID
                                    print(f"  ✓ 找到对应的认证用户: {auth_check.user.email}")
                                    break
                            except:
                                print(f"  ✗ ID {user_profile['id']} 没有对应的认证用户")
                except Exception as search_e:
                    print(f"  搜索失败: {search_e}")
                    
        except Exception as e:
            print(f"✗ 检查认证用户失败: {e}")
            target_auth_user = None
        
        # 2. 检查users表中的所有用户
        print("\n2. 检查users表...")
        try:
            users_response = supabase.table('users').select('*').execute()
            
            print(f"users表中共有 {len(users_response.data)} 个用户资料")
            
            target_profile = None
            for user_profile in users_response.data:
                if user_profile['email'] == target_email:
                    target_profile = user_profile
                    print(f"✓ 找到用户资料: {user_profile}")
                    break
            
            if not target_profile:
                print(f"✗ users表中未找到邮箱为 {target_email} 的用户资料")
                
                # 显示前几个用户资料作为参考
                print("\n前5个用户资料:")
                for i, profile in enumerate(users_response.data[:5]):
                    print(f"  {i+1}. {profile['email']} (ID: {profile['id']})")
                    
        except Exception as e:
            print(f"✗ 查询users表失败: {e}")
        
        # 3. 如果找到了认证用户但没有用户资料，创建用户资料
        if target_auth_user and not target_profile:
            print(f"\n3. 为认证用户创建用户资料...")
            
            # 使用认证用户的实际ID
            actual_user_id = target_auth_user.id
            
            user_profile = {
                'id': actual_user_id,
                'email': target_email,
                'full_name': target_email.split('@')[0],
                'role': 'teacher',
                'is_active': True,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            try:
                insert_response = supabase.table('users').insert(user_profile).execute()
                
                if insert_response.data:
                    print(f"✓ 用户资料创建成功: {insert_response.data[0]}")
                else:
                    print("✗ 用户资料创建失败")
                    
            except Exception as e:
                print(f"✗ 创建用户资料时出错: {e}")
        
        # 4. 如果都没找到，创建完整的用户（认证用户 + 用户资料）
        elif not target_auth_user and not target_profile:
            print(f"\n3. 创建完整的用户账户...")
            
            try:
                # 创建认证用户
                auth_response = supabase.auth.admin.create_user({
                    "email": target_email,
                    "password": "TempPassword123!",  # 临时密码，用户需要重置
                    "email_confirm": True  # 直接确认邮箱
                })
                
                if auth_response.user:
                    print(f"✓ 认证用户创建成功: {auth_response.user.email} (ID: {auth_response.user.id})")
                    
                    # 创建用户资料
                    user_profile = {
                        'id': auth_response.user.id,
                        'email': target_email,
                        'full_name': target_email.split('@')[0],
                        'role': 'teacher',
                        'is_active': True,
                        'created_at': datetime.utcnow().isoformat(),
                        'updated_at': datetime.utcnow().isoformat()
                    }
                    
                    insert_response = supabase.table('users').insert(user_profile).execute()
                    
                    if insert_response.data:
                        print(f"✓ 用户资料创建成功: {insert_response.data[0]}")
                        print(f"\n⚠️  注意: 为用户设置了临时密码 'TempPassword123!'")
                        print(f"   用户首次登录时需要重置密码")
                    else:
                        print("✗ 用户资料创建失败")
                else:
                    print("✗ 认证用户创建失败")
                    
            except Exception as e:
                print(f"✗ 创建用户账户时出错: {e}")
        
        print("\n" + "=" * 60)
        print("诊断完成！")
        
    except Exception as e:
        print(f"脚本执行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()