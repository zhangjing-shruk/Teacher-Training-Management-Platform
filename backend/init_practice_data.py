#!/usr/bin/env python3
"""
初始化练习相关数据的脚本
"""
import sys
import os
sys.path.append('.')

from sqlalchemy.orm import Session
from app.core.database import engine, get_db
from app.models.training import PracticeMode, CourseTopic, EvaluationFocus
from app.core.database import Base

def init_practice_data():
    """初始化练习相关数据"""
    
    # 创建所有表
    print("创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("✓ 数据库表创建完成")
    
    # 获取数据库会话
    db = next(get_db())
    
    try:
        # 检查是否已有数据
        existing_modes = db.query(PracticeMode).count()
        if existing_modes > 0:
            print("练习模式数据已存在，跳过初始化")
        else:
            # 插入练习模式数据
            practice_modes = [
                PracticeMode(
                    name="自由练习",
                    description="自由选择主题进行试讲练习，适合日常训练",
                    duration_minutes=30,
                    difficulty_level="beginner",
                    order_index=1
                ),
                PracticeMode(
                    name="模拟课堂",
                    description="模拟真实课堂环境，包含学生互动环节",
                    duration_minutes=45,
                    difficulty_level="intermediate",
                    order_index=2
                ),
                PracticeMode(
                    name="专题训练",
                    description="针对特定教学技能进行专项训练",
                    duration_minutes=20,
                    difficulty_level="intermediate",
                    order_index=3
                ),
                PracticeMode(
                    name="考核模式",
                    description="按照正式考核标准进行评估",
                    duration_minutes=60,
                    difficulty_level="advanced",
                    order_index=4
                )
            ]
            
            for mode in practice_modes:
                db.add(mode)
            print("✓ 练习模式数据插入完成")
        
        # 检查课程主题数据
        existing_topics = db.query(CourseTopic).count()
        if existing_topics > 0:
            print("课程主题数据已存在，跳过初始化")
        else:
            # 插入课程主题数据
            course_topics = [
                CourseTopic(name="数学基础概念"),
                CourseTopic(name="语文阅读理解"),
                CourseTopic(name="英语口语交流"),
                CourseTopic(name="科学实验探索"),
                CourseTopic(name="历史文化传承")
            ]
            
            for topic in course_topics:
                db.add(topic)
            print("✓ 课程主题数据插入完成")
        
        # 检查评估重点数据
        existing_focus = db.query(EvaluationFocus).count()
        if existing_focus > 0:
            print("评估重点数据已存在，跳过初始化")
        else:
            # 插入评估重点数据
            evaluation_focus = [
                EvaluationFocus(
                    name="发音准确性",
                    description="评估教师发音的准确性和清晰度",
                    category="pronunciation",
                    weight=1.0,
                    criteria='["发音清晰", "语调自然", "语速适中"]',
                    order_index=1
                ),
                EvaluationFocus(
                    name="语言流畅性",
                    description="评估教师语言表达的流畅程度",
                    category="fluency",
                    weight=1.0,
                    criteria='["表达流畅", "逻辑清晰", "用词准确"]',
                    order_index=2
                ),
                EvaluationFocus(
                    name="教学内容",
                    description="评估教学内容的准确性和完整性",
                    category="content",
                    weight=1.5,
                    criteria='["内容准确", "结构完整", "重点突出"]',
                    order_index=3
                ),
                EvaluationFocus(
                    name="课堂互动",
                    description="评估与学生的互动效果",
                    category="interaction",
                    weight=1.2,
                    criteria='["互动自然", "引导有效", "回应及时"]',
                    order_index=4
                ),
                EvaluationFocus(
                    name="教学方法",
                    description="评估教学方法的有效性",
                    category="content",
                    weight=1.3,
                    criteria='["方法得当", "形式多样", "效果明显"]',
                    order_index=5
                )
            ]
            
            for focus in evaluation_focus:
                db.add(focus)
            print("✓ 评估重点数据插入完成")
        
        # 提交所有更改
        db.commit()
        print("🎉 练习数据初始化完成！")
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_practice_data()