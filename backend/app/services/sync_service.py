"""
数据同步服务
处理管理员和教师之间的培训资料同步
"""

import json
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.user import User, UserRole
from app.models.training import TrainingMaterial
from app.models.sync import MaterialSyncRecord, SyncLog, MaterialVersion, SyncOperation, SyncStatus


class SyncService:
    """数据同步服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_version(self) -> str:
        """生成版本号"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"v{timestamp}-{unique_id}"
    
    def create_material_version(self, material: TrainingMaterial, user: User, change_description: str = None) -> MaterialVersion:
        """创建资料版本记录"""
        version = self.generate_version()
        
        # 将当前版本设为非当前版本
        self.db.query(MaterialVersion).filter(
            and_(
                MaterialVersion.material_id == material.id,
                MaterialVersion.is_current == True
            )
        ).update({"is_current": False})
        
        # 创建新版本
        material_version = MaterialVersion(
            material_id=material.id,
            version=version,
            title=material.title,
            description=material.description,
            file_url=material.file_url,
            file_size=material.file_size,
            change_description=change_description,
            created_by=user.id,
            is_current=True
        )
        
        self.db.add(material_version)
        self.db.commit()
        
        return material_version
    
    def log_sync_operation(self, operation: SyncOperation, user: User, description: str, 
                          material_id: int = None, status: SyncStatus = SyncStatus.COMPLETED,
                          details: dict = None, error_message: str = None, batch_id: str = None):
        """记录同步操作日志"""
        sync_log = SyncLog(
            operation=operation,
            status=status,
            user_id=user.id,
            material_id=material_id,
            batch_id=batch_id,
            description=description,
            details=json.dumps(details) if details else None,
            error_message=error_message
        )
        
        self.db.add(sync_log)
        self.db.commit()
        
        return sync_log
    
    def sync_material_to_teachers(self, material_id: int, source_user: User, target_teacher_ids: List[int] = None) -> bool:
        """将管理员的培训资料同步给教师"""
        try:
            # 获取资料
            material = self.db.query(TrainingMaterial).filter(TrainingMaterial.id == material_id).first()
            if not material:
                raise ValueError(f"培训资料 {material_id} 不存在")
            
            # 生成批量操作ID
            batch_id = str(uuid.uuid4())
            
            # 如果没有指定目标教师，则同步给所有教师
            if target_teacher_ids is None:
                teachers = self.db.query(User).filter(User.role == UserRole.TEACHER).all()
                target_teacher_ids = [teacher.id for teacher in teachers]
            
            # 将资料状态设为已发布（教师只能看到已发布的资料）
            material.status = "published"
            
            # 创建版本记录
            version = self.create_material_version(
                material, 
                source_user, 
                f"同步到教师账户 (批次: {batch_id})"
            )
            
            # 为每个目标教师创建同步记录
            for teacher_id in target_teacher_ids:
                sync_record = MaterialSyncRecord(
                    material_id=material_id,
                    operation=SyncOperation.SYNC_TO_TEACHER,
                    status=SyncStatus.COMPLETED,
                    source_user_id=source_user.id,
                    target_user_id=teacher_id,
                    version=version.version,
                    sync_details=json.dumps({
                        "batch_id": batch_id,
                        "material_title": material.title,
                        "sync_time": datetime.now().isoformat()
                    }),
                    completed_at=datetime.now()
                )
                self.db.add(sync_record)
            
            self.db.commit()
            
            # 记录操作日志
            self.log_sync_operation(
                operation=SyncOperation.SYNC_TO_TEACHER,
                user=source_user,
                description=f"将培训资料 '{material.title}' 同步给 {len(target_teacher_ids)} 位教师",
                material_id=material_id,
                batch_id=batch_id,
                details={
                    "target_teacher_count": len(target_teacher_ids),
                    "target_teacher_ids": target_teacher_ids,
                    "version": version.version
                }
            )
            
            return True
            
        except Exception as e:
            # 记录错误日志
            self.log_sync_operation(
                operation=SyncOperation.SYNC_TO_TEACHER,
                user=source_user,
                description=f"同步培训资料失败: {str(e)}",
                material_id=material_id,
                status=SyncStatus.FAILED,
                error_message=str(e),
                batch_id=batch_id if 'batch_id' in locals() else None
            )
            return False
    
    def sync_all_materials_to_teachers(self, source_user: User, target_teacher_ids: List[int] = None) -> dict:
        """将所有管理员资料同步给教师"""
        try:
            # 获取所有管理员创建的资料
            materials = self.db.query(TrainingMaterial).all()
            
            batch_id = str(uuid.uuid4())
            success_count = 0
            failed_count = 0
            failed_materials = []
            
            for material in materials:
                try:
                    if self.sync_material_to_teachers(material.id, source_user, target_teacher_ids):
                        success_count += 1
                    else:
                        failed_count += 1
                        failed_materials.append(material.title)
                except Exception as e:
                    failed_count += 1
                    failed_materials.append(f"{material.title}: {str(e)}")
            
            # 记录批量操作日志
            self.log_sync_operation(
                operation=SyncOperation.SYNC_TO_TEACHER,
                user=source_user,
                description=f"批量同步完成: 成功 {success_count} 个，失败 {failed_count} 个",
                batch_id=batch_id,
                status=SyncStatus.COMPLETED if failed_count == 0 else SyncStatus.FAILED,
                details={
                    "total_materials": len(materials),
                    "success_count": success_count,
                    "failed_count": failed_count,
                    "failed_materials": failed_materials
                }
            )
            
            return {
                "success": True,
                "total": len(materials),
                "success_count": success_count,
                "failed_count": failed_count,
                "failed_materials": failed_materials,
                "batch_id": batch_id
            }
            
        except Exception as e:
            self.log_sync_operation(
                operation=SyncOperation.SYNC_TO_TEACHER,
                user=source_user,
                description=f"批量同步失败: {str(e)}",
                status=SyncStatus.FAILED,
                error_message=str(e)
            )
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_sync_logs(self, user_id: int = None, material_id: int = None, limit: int = 50) -> List[SyncLog]:
        """获取同步日志"""
        query = self.db.query(SyncLog)
        
        if user_id:
            query = query.filter(SyncLog.user_id == user_id)
        
        if material_id:
            query = query.filter(SyncLog.material_id == material_id)
        
        return query.order_by(SyncLog.created_at.desc()).limit(limit).all()
    
    def get_material_versions(self, material_id: int) -> List[MaterialVersion]:
        """获取资料版本历史"""
        return self.db.query(MaterialVersion).filter(
            MaterialVersion.material_id == material_id
        ).order_by(MaterialVersion.created_at.desc()).all()
    
    def delete_virtual_materials_for_teacher(self, teacher_id: int, admin_user: User) -> dict:
        """删除教师账户中的虚拟学习资料（前端硬编码的数据不需要删除，只需要确保API返回真实数据）"""
        try:
            # 由于虚拟资料是前端硬编码的，我们只需要记录这个操作
            self.log_sync_operation(
                operation=SyncOperation.DELETE,
                user=admin_user,
                description=f"清理教师 {teacher_id} 的虚拟学习资料",
                details={
                    "teacher_id": teacher_id,
                    "operation_type": "clear_virtual_materials"
                }
            )
            
            return {
                "success": True,
                "message": "虚拟资料清理完成（前端将显示真实数据）"
            }
            
        except Exception as e:
            self.log_sync_operation(
                operation=SyncOperation.DELETE,
                user=admin_user,
                description=f"清理教师虚拟资料失败: {str(e)}",
                status=SyncStatus.FAILED,
                error_message=str(e)
            )
            return {
                "success": False,
                "error": str(e)
            }