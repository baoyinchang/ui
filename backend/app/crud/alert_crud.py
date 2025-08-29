"""
Alert CRUD操作模块
提供告警数据的增删改查操作
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from datetime import datetime, timedelta
from app.core.logger import get_logger
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertUpdate

logger = get_logger(__name__)

class AlertCRUD:
    """
    Alert CRUD操作类
    """

    def get(self, db: Session, id: int) -> Optional[Alert]:
        """根据ID获取告警记录"""
        try:
            return db.query(Alert).filter(Alert.id == id).first()
        except Exception as e:
            logger.error(f"获取告警记录失败: {e}")
            return None

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        level: Optional[str] = None,
        status: Optional[str] = None,
        source: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Alert]:
        """获取多条告警记录"""
        try:
            query = db.query(Alert)

            # 添加过滤条件
            if level:
                query = query.filter(Alert.level == level)
            if status:
                query = query.filter(Alert.status == status)
            if source:
                query = query.filter(Alert.source.ilike(f"%{source}%"))
            if start_time:
                query = query.filter(Alert.created_at >= start_time)
            if end_time:
                query = query.filter(Alert.created_at <= end_time)

            # 按创建时间倒序排列
            query = query.order_by(desc(Alert.created_at))

            return query.offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"获取告警列表失败: {e}")
            return []

    def get_count(
        self,
        db: Session,
        *,
        level: Optional[str] = None,
        status: Optional[str] = None,
        source: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> int:
        """获取告警总数"""
        try:
            query = db.query(func.count(Alert.id))

            # 添加过滤条件
            if level:
                query = query.filter(Alert.level == level)
            if status:
                query = query.filter(Alert.status == status)
            if source:
                query = query.filter(Alert.source.ilike(f"%{source}%"))
            if start_time:
                query = query.filter(Alert.created_at >= start_time)
            if end_time:
                query = query.filter(Alert.created_at <= end_time)

            return query.scalar() or 0
        except Exception as e:
            logger.error(f"获取告警总数失败: {e}")
            return 0

    def create(self, db: Session, *, obj_in: AlertCreate) -> Alert:
        """创建告警记录"""
        try:
            db_obj = Alert(
                title=obj_in.title,
                description=obj_in.description,
                level=obj_in.level,
                source=obj_in.source,
                source_ip=obj_in.source_ip,
                target_ip=obj_in.target_ip,
                target_port=obj_in.target_port,
                protocol=obj_in.protocol,
                attack_type=obj_in.attack_type,
                payload=obj_in.payload,
                status="pending",
                created_at=datetime.utcnow()
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

            logger.info(f"创建告警记录成功: {db_obj.id}")
            return db_obj
        except Exception as e:
            logger.error(f"创建告警记录失败: {e}")
            db.rollback()
            raise

    def update(self, db: Session, *, db_obj: Alert, obj_in: AlertUpdate) -> Alert:
        """更新告警记录"""
        try:
            update_data = obj_in.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()

            for field, value in update_data.items():
                setattr(db_obj, field, value)

            db.commit()
            db.refresh(db_obj)

            logger.info(f"更新告警记录成功: {db_obj.id}")
            return db_obj
        except Exception as e:
            logger.error(f"更新告警记录失败: {e}")
            db.rollback()
            raise

    def remove(self, db: Session, *, id: int) -> Optional[Alert]:
        """删除告警记录"""
        try:
            obj = db.query(Alert).filter(Alert.id == id).first()
            if obj:
                db.delete(obj)
                db.commit()
                logger.info(f"删除告警记录成功: {id}")
                return obj
            return None
        except Exception as e:
            logger.error(f"删除告警记录失败: {e}")
            db.rollback()
            raise

    def get_statistics(self, db: Session, days: int = 7) -> Dict[str, Any]:
        """获取告警统计信息"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)

            # 总告警数
            total_count = self.get_count(db)

            # 最近N天告警数
            recent_count = self.get_count(db, start_time=start_time, end_time=end_time)

            # 按级别统计
            level_stats = {}
            for level in ['高危', '中危', '低危', '信息']:
                count = self.get_count(db, level=level)
                level_stats[level] = count

            # 按状态统计
            status_stats = {}
            for status in ['pending', 'processing', 'resolved', 'ignored']:
                count = self.get_count(db, status=status)
                status_stats[status] = count

            return {
                'total_count': total_count,
                'recent_count': recent_count,
                'level_stats': level_stats,
                'status_stats': status_stats
            }
        except Exception as e:
            logger.error(f"获取告警统计失败: {e}")
            return {}

# 创建CRUD实例
alert_crud = AlertCRUD()
