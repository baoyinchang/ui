from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from app.core.db import Base
import logging

# 配置日志
logger = logging.getLogger(__name__)

# 泛型类型变量
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    基础CRUD操作类
    提供通用的数据库操作方法
    """

    def __init__(self, model: Type[ModelType]):
        """
        初始化CRUD对象

        Args:
            model: SQLAlchemy模型类
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        根据ID获取单个记录

        Args:
            db: 数据库会话
            id: 记录ID

        Returns:
            Optional[ModelType]: 记录对象或None
        """
        try:
            return db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            logger.error(f"获取记录失败 (ID: {id}): {e}")
            return None

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        order_desc: bool = False
    ) -> List[ModelType]:
        """
        获取多个记录

        Args:
            db: 数据库会话
            skip: 跳过记录数
            limit: 限制记录数
            order_by: 排序字段
            order_desc: 是否降序排列

        Returns:
            List[ModelType]: 记录列表
        """
        try:
            query = db.query(self.model)

            # 添加排序
            if order_by and hasattr(self.model, order_by):
                order_field = getattr(self.model, order_by)
                if order_desc:
                    query = query.order_by(desc(order_field))
                else:
                    query = query.order_by(asc(order_field))

            return query.offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"获取多个记录失败: {e}")
            return []

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        创建新记录

        Args:
            db: 数据库会话
            obj_in: 创建数据模式

        Returns:
            ModelType: 创建的记录对象
        """
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            logger.info(f"创建记录成功 (ID: {db_obj.id})")
            return db_obj
        except Exception as e:
            logger.error(f"创建记录失败: {e}")
            db.rollback()
            raise

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        更新记录

        Args:
            db: 数据库会话
            db_obj: 数据库记录对象
            obj_in: 更新数据

        Returns:
            ModelType: 更新后的记录对象
        """
        try:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])

            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            logger.info(f"更新记录成功 (ID: {db_obj.id})")
            return db_obj
        except Exception as e:
            logger.error(f"更新记录失败 (ID: {db_obj.id}): {e}")
            db.rollback()
            raise

    def remove(self, db: Session, *, id: int) -> ModelType:
        """
        删除记录

        Args:
            db: 数据库会话
            id: 记录ID

        Returns:
            ModelType: 被删除的记录对象
        """
        try:
            obj = db.query(self.model).get(id)
            if obj:
                db.delete(obj)
                db.commit()
                logger.info(f"删除记录成功 (ID: {id})")
                return obj
            else:
                logger.warning(f"要删除的记录不存在 (ID: {id})")
                return None
        except Exception as e:
            logger.error(f"删除记录失败 (ID: {id}): {e}")
            db.rollback()
            raise

    def count(self, db: Session, **filters) -> int:
        """
        统计记录数量

        Args:
            db: 数据库会话
            **filters: 过滤条件

        Returns:
            int: 记录数量
        """
        try:
            query = db.query(self.model)

            # 应用过滤条件
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.filter(getattr(self.model, field) == value)

            return query.count()
        except Exception as e:
            logger.error(f"统计记录数量失败: {e}")
            return 0

    def exists(self, db: Session, id: Any) -> bool:
        """
        检查记录是否存在

        Args:
            db: 数据库会话
            id: 记录ID

        Returns:
            bool: 记录是否存在
        """
        try:
            return db.query(self.model).filter(self.model.id == id).first() is not None
        except Exception as e:
            logger.error(f"检查记录存在性失败 (ID: {id}): {e}")
            return False

    def get_by_field(self, db: Session, field: str, value: Any) -> Optional[ModelType]:
        """
        根据指定字段获取记录

        Args:
            db: 数据库会话
            field: 字段名
            value: 字段值

        Returns:
            Optional[ModelType]: 记录对象或None
        """
        try:
            if hasattr(self.model, field):
                return db.query(self.model).filter(getattr(self.model, field) == value).first()
            else:
                logger.warning(f"模型 {self.model.__name__} 没有字段 {field}")
                return None
        except Exception as e:
            logger.error(f"根据字段获取记录失败 ({field}={value}): {e}")
            return None

    def get_multi_by_field(
        self,
        db: Session,
        field: str,
        value: Any,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """
        根据指定字段获取多个记录

        Args:
            db: 数据库会话
            field: 字段名
            value: 字段值
            skip: 跳过记录数
            limit: 限制记录数

        Returns:
            List[ModelType]: 记录列表
        """
        try:
            if hasattr(self.model, field):
                return (db.query(self.model)
                       .filter(getattr(self.model, field) == value)
                       .offset(skip)
                       .limit(limit)
                       .all())
            else:
                logger.warning(f"模型 {self.model.__name__} 没有字段 {field}")
                return []
        except Exception as e:
            logger.error(f"根据字段获取多个记录失败 ({field}={value}): {e}")
            return []