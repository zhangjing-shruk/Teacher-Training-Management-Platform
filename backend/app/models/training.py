from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from app.core.database import Base


class MaterialType(PyEnum):
    VIDEO = "video"
    DOCUMENT = "document"
    AUDIO = "audio"
    INTERACTIVE = "interactive"


class PracticeStatus(PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REVIEWED = "reviewed"


class TrainingMaterial(Base):
    __tablename__ = "training_materials"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String, default="教学文档")  # 资料类别
    type = Column(Enum(MaterialType), nullable=False)
    file_path = Column(String)
    url = Column(String)
    duration_minutes = Column(Integer)  # 学习时长（分钟）
    order_index = Column(Integer, default=0)  # 排序索引
    
    # 文件上传相关字段
    file_url = Column(String)  # 文件访问URL
    file_size = Column(String)  # 文件大小（格式化字符串）
    download_count = Column(Integer, default=0)  # 下载次数
    status = Column(String, default="draft")  # 状态：draft, published, archived
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(PracticeStatus), default=PracticeStatus.PENDING)
    
    # 录制文件信息
    video_path = Column(String)
    audio_path = Column(String)
    duration_seconds = Column(Integer)
    
    # AI分析结果占位符
    ai_analysis_result = Column(Text)  # JSON格式存储AI分析结果
    
    # 评分
    overall_score = Column(Float)
    pronunciation_score = Column(Float)
    fluency_score = Column(Float)
    content_score = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="practice_sessions")
    feedback = relationship("Feedback", back_populates="practice_session")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    practice_session_id = Column(Integer, ForeignKey("practice_sessions.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"))  # 评审员ID，可为空（AI评审）
    
    # 反馈内容
    content = Column(Text, nullable=False)
    suggestions = Column(Text)
    
    # 评分详情
    pronunciation_feedback = Column(Text)
    fluency_feedback = Column(Text)
    content_feedback = Column(Text)
    
    # 是否为AI生成
    is_ai_generated = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    practice_session = relationship("PracticeSession", back_populates="feedback")
    reviewer = relationship("User")


class PracticeMode(Base):
    __tablename__ = "practice_modes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # 练习模式名称
    description = Column(Text)  # 模式描述
    duration_minutes = Column(Integer, default=30)  # 建议练习时长
    difficulty_level = Column(String, default="beginner")  # 难度等级：beginner, intermediate, advanced
    is_active = Column(Boolean, default=True)  # 是否启用
    order_index = Column(Integer, default=0)  # 排序索引
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class CourseTopic(Base):
    __tablename__ = "course_topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)  # 课程主题名称，要求唯一
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class EvaluationFocus(Base):
    __tablename__ = "evaluation_focus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # 评估重点名称
    description = Column(Text)  # 评估重点描述
    category = Column(String)  # 评估类别：pronunciation, fluency, content, interaction
    weight = Column(Float, default=1.0)  # 评估权重
    criteria = Column(Text)  # 评估标准，JSON格式存储
    is_active = Column(Boolean, default=True)  # 是否启用
    order_index = Column(Integer, default=0)  # 排序索引
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())