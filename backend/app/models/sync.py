from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from app.core.database import Base


class SyncOperation(PyEnum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    SYNC_TO_TEACHER = "sync_to_teacher"
    SYNC_FROM_TEACHER = "sync_from_teacher"


class SyncStatus(PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class MaterialSyncRecord(Base):
    """培训资料同步记录表"""
    __tablename__ = "material_sync_records"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("training_materials.id"), nullable=False)
    operation = Column(Enum(SyncOperation), nullable=False)
    status = Column(Enum(SyncStatus), default=SyncStatus.PENDING)
    
    # 同步相关信息
    source_user_id = Column(Integer, ForeignKey("users.id"))  # 操作发起者
    target_user_id = Column(Integer, ForeignKey("users.id"))  # 同步目标用户（可为空，表示同步给所有教师）
    
    # 版本控制
    version = Column(String, nullable=False)  # 版本号
    previous_version = Column(String)  # 上一个版本号
    
    # 同步详情
    sync_details = Column(Text)  # JSON格式存储同步详情
    error_message = Column(Text)  # 错误信息
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # 关系
    material = relationship("TrainingMaterial")
    source_user = relationship("User", foreign_keys=[source_user_id])
    target_user = relationship("User", foreign_keys=[target_user_id])


class SyncLog(Base):
    """同步操作日志表"""
    __tablename__ = "sync_logs"

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(Enum(SyncOperation), nullable=False)
    status = Column(Enum(SyncStatus), nullable=False)
    
    # 操作信息
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("training_materials.id"))
    batch_id = Column(String)  # 批量操作ID
    
    # 日志详情
    description = Column(Text, nullable=False)
    details = Column(Text)  # JSON格式存储详细信息
    error_message = Column(Text)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    user = relationship("User")
    material = relationship("TrainingMaterial")


class MaterialVersion(Base):
    """培训资料版本控制表"""
    __tablename__ = "material_versions"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("training_materials.id"), nullable=False)
    version = Column(String, nullable=False)
    
    # 版本信息
    title = Column(String, nullable=False)
    description = Column(Text)
    file_url = Column(String)
    file_size = Column(String)
    
    # 变更信息
    change_description = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_current = Column(Boolean, default=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    material = relationship("TrainingMaterial")
    creator = relationship("User")