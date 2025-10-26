#!/usr/bin/env python3
"""
创建本地数据库管理员用户
"""

from app.core.database import get_db, engine
from app.models.user import User, UserRole, TrainingStatus, Base
from app.core.security import get_password_hash
from sqlalchemy.orm import Session

def create_local_admin():
    """在本地数据库中创建管理员用户"""
    
    # 确保数据库表存在
    Base.metadata.create_all(bind=engine)
    
    # 获取数据库会话
    db = next(get_db())
    
    try:
        # 检查用户是否已存在
        existing_user = db.query(User).filter(User.email == "zhangjing32@51talk.com").first()
        
        password = "admin123456"[:72]  # 确保密码不超过72字节
        
        if existing_user:
            print(f"用户 {existing_user.email} 已存在，更新密码...")
            # 更新密码
            existing_user.hashed_password = get_password_hash(password)
            existing_user.role = UserRole.MANAGER
            db.commit()
            print(f"✅ 用户 {existing_user.email} 密码已更新")
        else:
            # 创建新用户
            admin_user = User(
                email="zhangjing32@51talk.com",
                name="管理员",
                hashed_password=get_password_hash(password),
                role=UserRole.MANAGER,
                training_status=TrainingStatus.COMPLETED,
                training_progress=100
            )
            
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            print(f"✅ 管理员用户创建成功:")
            print(f"   邮箱: {admin_user.email}")
            print(f"   密码: admin123456")
            print(f"   角色: {admin_user.role.value}")
            print(f"   ID: {admin_user.id}")
            
    except Exception as e:
        print(f"❌ 创建用户失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_local_admin()