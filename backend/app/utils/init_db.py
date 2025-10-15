"""
数据库初始化脚本
创建表结构并插入初始数据
"""

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal, create_tables
from app.core.security import get_password_hash
from app.models.user import User, UserRole, TrainingStatus
from app.models.training import TrainingMaterial, MaterialType
from app.models.sync import MaterialSyncRecord, SyncLog, MaterialVersion


def create_initial_users(db: Session):
    """创建初始用户"""
    
    # 检查是否已有用户
    existing_users = db.query(User).first()
    if existing_users:
        print("用户已存在，跳过初始用户创建")
        return
    
    # 创建管理员用户
    admin_user = User(
        email="admin@example.com",
        name="系统管理员",
        hashed_password=get_password_hash("admin123"),
        role=UserRole.MANAGER,
        is_active=True,
        training_status=TrainingStatus.COMPLETED,
        training_progress=100
    )
    
    # 创建教师用户
    teacher_users = [
        User(
            email="teacher1@example.com",
            name="张老师",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            is_active=True,
            training_status=TrainingStatus.IN_PROGRESS,
            training_progress=65
        ),
        User(
            email="teacher2@example.com",
            name="李老师",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            is_active=True,
            training_status=TrainingStatus.NOT_STARTED,
            training_progress=0
        ),
        User(
            email="teacher3@example.com",
            name="王老师",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            is_active=True,
            training_status=TrainingStatus.COMPLETED,
            training_progress=100
        )
    ]
    
    # 添加到数据库
    db.add(admin_user)
    for teacher in teacher_users:
        db.add(teacher)
    
    db.commit()
    print("初始用户创建完成")


def create_initial_materials(db: Session):
    """创建初始培训资料"""
    
    # 检查是否已有资料
    existing_materials = db.query(TrainingMaterial).first()
    if existing_materials:
        print("培训资料已存在，跳过初始资料创建")
        return
    
    materials = [
        TrainingMaterial(
            title="英语教学基础理论",
            description="介绍英语教学的基本理论和方法",
            type=MaterialType.VIDEO,
            duration_minutes=45,
            order_index=1
        ),
        TrainingMaterial(
            title="课堂互动技巧",
            description="如何在线上课堂中有效地与学生互动",
            type=MaterialType.DOCUMENT,
            duration_minutes=30,
            order_index=2
        ),
        TrainingMaterial(
            title="发音纠正方法",
            description="常见发音错误及纠正技巧",
            type=MaterialType.AUDIO,
            duration_minutes=25,
            order_index=3
        ),
        TrainingMaterial(
            title="教学评估与反馈",
            description="如何评估学生学习效果并给出有效反馈",
            type=MaterialType.INTERACTIVE,
            duration_minutes=40,
            order_index=4
        )
    ]
    
    for material in materials:
        db.add(material)
    
    db.commit()
    print("初始培训资料创建完成")


def init_database():
    """初始化数据库"""
    print("开始初始化数据库...")
    
    # 创建表结构
    create_tables()
    print("数据库表创建完成")
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 创建初始数据
        create_initial_users(db)
        create_initial_materials(db)
        
        print("数据库初始化完成！")
        print("\n默认账户信息：")
        print("管理员账户：admin@example.com / admin123")
        print("教师账户：teacher1@example.com / teacher123")
        print("教师账户：teacher2@example.com / teacher123")
        print("教师账户：teacher3@example.com / teacher123")
        
    except Exception as e:
        print(f"数据库初始化失败：{e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()