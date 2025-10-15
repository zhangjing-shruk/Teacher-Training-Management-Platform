#!/usr/bin/env python3
"""
检查数据库中的用户数据
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password

def check_users():
    """检查数据库中的用户"""
    db = SessionLocal()
    
    try:
        users = db.query(User).all()
        print(f"数据库中共有 {len(users)} 个用户:")
        
        for user in users:
            print(f"- ID: {user.id}")
            print(f"  邮箱: {user.email}")
            print(f"  姓名: {user.name}")
            print(f"  角色: {user.role}")
            print(f"  状态: {'激活' if user.is_active else '未激活'}")
            print(f"  密码哈希: {user.hashed_password[:50]}...")
            
            # 测试密码验证
            if user.email == "admin@example.com":
                is_valid = verify_password("admin123", user.hashed_password)
                print(f"  密码验证 (admin123): {'通过' if is_valid else '失败'}")
            elif user.email.startswith("teacher"):
                is_valid = verify_password("teacher123", user.hashed_password)
                print(f"  密码验证 (teacher123): {'通过' if is_valid else '失败'}")
            print()
            
    except Exception as e:
        print(f"检查用户时出错: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_users()