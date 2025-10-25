#!/usr/bin/env python3
"""
清理本地SQLite数据库中的所有用户
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User

def get_all_users():
    """获取所有本地用户"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        print(f"❌ 获取用户失败: {e}")
        return []
    finally:
        db.close()

def delete_all_local_users():
    """删除所有本地用户"""
    db = SessionLocal()
    
    try:
        # 获取所有用户
        users = db.query(User).all()
        
        if not users:
            print("✅ 本地数据库中没有用户需要清理")
            return
        
        print(f"📊 找到 {len(users)} 个本地用户需要清理:")
        for user in users:
            print(f"  - {user.email} (ID: {user.id}, 角色: {user.role})")
        
        # 确认删除
        confirm = input(f"\n⚠️  确认删除所有 {len(users)} 个本地用户吗？(输入 'YES' 确认): ")
        if confirm != "YES":
            print("❌ 操作已取消")
            return
        
        print("\n🗑️  开始删除本地用户...")
        
        # 删除所有用户
        deleted_count = db.query(User).delete()
        db.commit()
        
        print(f"✅ 成功删除 {deleted_count} 个本地用户")
        
    except Exception as e:
        print(f"❌ 删除用户时出错: {e}")
        db.rollback()
    finally:
        db.close()

def check_local_users():
    """检查本地用户状态"""
    db = SessionLocal()
    
    try:
        users = db.query(User).all()
        print(f"📊 本地数据库中共有 {len(users)} 个用户:")
        
        for user in users:
            print(f"- ID: {user.id}")
            print(f"  邮箱: {user.email}")
            print(f"  姓名: {user.name}")
            print(f"  角色: {user.role}")
            print(f"  状态: {'激活' if user.is_active else '未激活'}")
            print()
            
    except Exception as e:
        print(f"❌ 检查用户时出错: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🧹 本地SQLite数据库用户清理工具")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "cleanup":
        delete_all_local_users()
    else:
        check_local_users()
        print("\n💡 使用说明:")
        print("   查看状态: python3 cleanup_local_users.py")
        print("   执行清理: python3 cleanup_local_users.py cleanup")