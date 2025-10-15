from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class LearningProgress(Base):
    """学习进度记录表"""
    __tablename__ = "learning_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("training_materials.id"), nullable=False)
    
    # 学习时间记录
    start_time = Column(DateTime(timezone=True))  # 开始学习时间
    last_active_time = Column(DateTime(timezone=True))  # 最后活跃时间
    total_study_seconds = Column(Integer, default=0)  # 总学习时长（秒）
    
    # 学习状态
    is_completed = Column(Boolean, default=False)  # 是否完成
    completion_time = Column(DateTime(timezone=True))  # 完成时间
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User")
    material = relationship("TrainingMaterial")