from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime, timedelta

from app.core.db import get_db
from app.core.dependencies import get_current_active_user, get_current_user_with_permission
from app.models.postgres import Alert, Asset, AlertRule, User
from app.schemas.user import User as UserSchema
from app.schemas.common import (
    MessageResponse,
    PaginatedResponse,
    IDResponse
)
import logging

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter()

# 告警相关数据模式
from pydantic import BaseModel

class AlertBase(BaseModel):
    """告警基础模式"""
    alert_name: str
    severity: str  # low, medium, high, critical
    description: Optional[str] = None

class AlertCreate(AlertBase):
    """创建告警模式"""
    event_id: Optional[int] = None
    asset_id: int

class AlertUpdate(BaseModel):
    """更新告警模式"""
    status: Optional[str] = None  # unhandled, handling, resolved
    handle_notes: Optional[str] = None

class AlertResponse(AlertBase):
    """告警响应模式"""
    id: int
    event_id: Optional[int]
    asset_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    handled_by: Optional[int]
    handle_notes: Optional[str]
    handled_at: Optional[datetime]

    # 关联数据
    asset_name: Optional[str] = None
    handler_name: Optional[str] = None

    class Config:
        from_attributes = True

class AlertDetail(AlertResponse):
    """告警详情模式"""
    raw_data: Optional[dict] = None
    related_events: List[dict] = []

class AlertRuleBase(BaseModel):
    """告警规则基础模式"""
    name: str
    description: Optional[str] = None
    condition: dict
    severity: str
    enabled: bool = True

class AlertRuleCreate(AlertRuleBase):
    """创建告警规则模式"""
    pass

class AlertRuleUpdate(BaseModel):
    """更新告警规则模式"""
    name: Optional[str] = None
    description: Optional[str] = None
    condition: Optional[dict] = None
    severity: Optional[str] = None
    enabled: Optional[bool] = None

class AlertRuleResponse(AlertRuleBase):
    """告警规则响应模式"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AlertStatistics(BaseModel):
    """告警统计模式"""
    total: int
    unhandled: int
    handling: int
    resolved: int
    critical: int
    high: int
    medium: int
    low: int
    today_new: int
    this_week_new: int

@router.get("/", response_model=PaginatedResponse[AlertResponse], summary="获取告警列表")
def get_alerts(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    severity: Optional[str] = Query(None, description="告警级别过滤"),
    status: Optional[str] = Query(None, description="处理状态过滤"),
    asset_id: Optional[int] = Query(None, description="资产ID过滤"),
    start_time: Optional[datetime] = Query(None, description="开始时间"),
    end_time: Optional[datetime] = Query(None, description="结束时间"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("alert:read"))
) -> Any:
    """
    获取告警列表

    支持多种过滤条件：
    - **severity**: 告警级别 (critical, high, medium, low)
    - **status**: 处理状态 (unhandled, handling, resolved)
    - **asset_id**: 资产ID
    - **start_time**: 开始时间
    - **end_time**: 结束时间
    - **search**: 搜索告警名称或描述
    """
    try:
        skip = (page - 1) * size

        # 构建查询
        query = db.query(Alert, Asset.name.label('asset_name'), User.full_name.label('handler_name')).join(
            Asset, Alert.asset_id == Asset.id
        ).outerjoin(
            User, Alert.handled_by == User.id
        )

        # 应用过滤条件
        if severity:
            query = query.filter(Alert.severity == severity)

        if status:
            query = query.filter(Alert.status == status)

        if asset_id:
            query = query.filter(Alert.asset_id == asset_id)

        if start_time:
            query = query.filter(Alert.created_at >= start_time)

        if end_time:
            query = query.filter(Alert.created_at <= end_time)

        if search:
            query = query.filter(
                or_(
                    Alert.alert_name.ilike(f"%{search}%"),
                    Alert.description.ilike(f"%{search}%")
                )
            )

        # 获取总数
        total = query.count()

        # 分页和排序
        results = query.order_by(desc(Alert.created_at)).offset(skip).limit(size).all()

        # 构建响应数据
        alerts = []
        for alert, asset_name, handler_name in results:
            alert_data = AlertResponse(
                id=alert.id,
                alert_name=alert.alert_name,
                severity=alert.severity,
                description=alert.description,
                event_id=alert.event_id,
                asset_id=alert.asset_id,
                status=alert.status,
                created_at=alert.created_at,
                updated_at=alert.updated_at,
                handled_by=alert.handled_by,
                handle_notes=alert.handle_notes,
                handled_at=alert.handled_at,
                asset_name=asset_name,
                handler_name=handler_name
            )
            alerts.append(alert_data)

        return PaginatedResponse.create(
            items=alerts,
            total=total,
            page=page,
            size=size
        )

    except Exception as e:
        logger.error(f"获取告警列表失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取告警列表失败"
        )

@router.get("/{alert_id}", response_model=AlertDetail, summary="获取告警详情")
def get_alert_detail(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("alert:read"))
) -> Any:
    """
    获取告警详情

    包含告警基本信息、关联事件、处理记录等
    """
    try:
        # 查询告警详情
        result = db.query(Alert, Asset.name.label('asset_name'), User.full_name.label('handler_name')).join(
            Asset, Alert.asset_id == Asset.id
        ).outerjoin(
            User, Alert.handled_by == User.id
        ).filter(Alert.id == alert_id).first()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="告警不存在"
            )

        alert, asset_name, handler_name = result

        # 获取关联事件（模拟数据）
        related_events = []
        if alert.event_id:
            related_events = [
                {
                    "id": alert.event_id,
                    "event_type": "process_creation",
                    "event_time": alert.created_at.isoformat(),
                    "description": "可疑进程创建事件"
                }
            ]

        alert_detail = AlertDetail(
            id=alert.id,
            alert_name=alert.alert_name,
            severity=alert.severity,
            description=alert.description,
            event_id=alert.event_id,
            asset_id=alert.asset_id,
            status=alert.status,
            created_at=alert.created_at,
            updated_at=alert.updated_at,
            handled_by=alert.handled_by,
            handle_notes=alert.handle_notes,
            handled_at=alert.handled_at,
            asset_name=asset_name,
            handler_name=handler_name,
            raw_data={"source": "honeypot", "confidence": 0.85},
            related_events=related_events
        )

        return alert_detail

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取告警详情失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取告警详情失败"
        )

@router.put("/{alert_id}/status", response_model=MessageResponse, summary="更新告警状态")
def update_alert_status(
    alert_id: int,
    alert_update: AlertUpdate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("alert:handle"))
) -> Any:
    """
    更新告警处理状态

    - **status**: 新状态 (unhandled, handling, resolved)
    - **handle_notes**: 处理备注
    """
    try:
        # 查询告警
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="告警不存在"
            )

        # 更新状态
        if alert_update.status:
            alert.status = alert_update.status
            alert.handled_by = current_user.id
            alert.handled_at = datetime.utcnow()

        if alert_update.handle_notes:
            alert.handle_notes = alert_update.handle_notes

        alert.updated_at = datetime.utcnow()

        db.commit()

        logger.info(f"用户 {current_user.username} 更新了告警 {alert_id} 的状态为 {alert_update.status}")

        return MessageResponse(
            success=True,
            message="告警状态更新成功"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新告警状态失败: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新告警状态失败"
        )

@router.post("/", response_model=IDResponse, summary="创建告警")
def create_alert(
    alert_data: AlertCreate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("alert:create"))
) -> Any:
    """
    创建新告警

    - **alert_name**: 告警名称
    - **severity**: 告警级别
    - **asset_id**: 关联资产ID
    - **event_id**: 关联事件ID（可选）
    - **description**: 告警描述
    """
    try:
        # 检查资产是否存在
        asset = db.query(Asset).filter(Asset.id == alert_data.asset_id).first()
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="指定的资产不存在"
            )

        # 创建告警
        alert = Alert(
            alert_name=alert_data.alert_name,
            severity=alert_data.severity,
            description=alert_data.description,
            event_id=alert_data.event_id,
            asset_id=alert_data.asset_id,
            status='unhandled'
        )

        db.add(alert)
        db.commit()
        db.refresh(alert)

        logger.info(f"用户 {current_user.username} 创建了告警: {alert.alert_name}")

        return IDResponse(
            id=alert.id,
            message="告警创建成功"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建告警失败: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建告警失败"
        )

@router.get("/statistics", response_model=AlertStatistics, summary="获取告警统计")
def get_alert_statistics(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("alert:read"))
) -> Any:
    """
    获取告警统计数据

    包含总数、各状态数量、各级别数量、时间段统计等
    """
    try:
        # 总告警数
        total = db.query(Alert).count()

        # 按状态统计
        unhandled = db.query(Alert).filter(Alert.status == 'unhandled').count()
        handling = db.query(Alert).filter(Alert.status == 'handling').count()
        resolved = db.query(Alert).filter(Alert.status == 'resolved').count()

        # 按级别统计
        critical = db.query(Alert).filter(Alert.severity == 'critical').count()
        high = db.query(Alert).filter(Alert.severity == 'high').count()
        medium = db.query(Alert).filter(Alert.severity == 'medium').count()
        low = db.query(Alert).filter(Alert.severity == 'low').count()

        # 时间段统计
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        week_start = today_start - timedelta(days=7)

        today_new = db.query(Alert).filter(Alert.created_at >= today_start).count()
        this_week_new = db.query(Alert).filter(Alert.created_at >= week_start).count()

        return AlertStatistics(
            total=total,
            unhandled=unhandled,
            handling=handling,
            resolved=resolved,
            critical=critical,
            high=high,
            medium=medium,
            low=low,
            today_new=today_new,
            this_week_new=this_week_new
        )

    except Exception as e:
        logger.error(f"获取告警统计失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取告警统计失败"
        )

@router.get("/rules", response_model=PaginatedResponse[AlertRuleResponse], summary="获取告警规则列表")
def get_alert_rules(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    enabled: Optional[bool] = Query(None, description="是否启用"),
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("alert:read"))
) -> Any:
    """
    获取告警规则列表

    - **enabled**: 过滤启用状态
    """
    try:
        skip = (page - 1) * size

        query = db.query(AlertRule)

        if enabled is not None:
            query = query.filter(AlertRule.enabled == enabled)

        total = query.count()
        rules = query.order_by(desc(AlertRule.created_at)).offset(skip).limit(size).all()

        return PaginatedResponse.create(
            items=rules,
            total=total,
            page=page,
            size=size
        )

    except Exception as e:
        logger.error(f"获取告警规则列表失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取告警规则列表失败"
        )

@router.post("/rules", response_model=IDResponse, summary="创建告警规则")
def create_alert_rule(
    rule_data: AlertRuleCreate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("alert:create"))
) -> Any:
    """
    创建告警规则

    - **name**: 规则名称
    - **description**: 规则描述
    - **condition**: 触发条件（JSON格式）
    - **severity**: 告警级别
    - **enabled**: 是否启用
    """
    try:
        # 检查规则名称是否已存在
        existing_rule = db.query(AlertRule).filter(AlertRule.name == rule_data.name).first()
        if existing_rule:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="规则名称已存在"
            )

        # 创建规则
        rule = AlertRule(
            name=rule_data.name,
            description=rule_data.description,
            condition=rule_data.condition,
            severity=rule_data.severity,
            enabled=rule_data.enabled
        )

        db.add(rule)
        db.commit()
        db.refresh(rule)

        logger.info(f"用户 {current_user.username} 创建了告警规则: {rule.name}")

        return IDResponse(
            id=rule.id,
            message="告警规则创建成功"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建告警规则失败: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建告警规则失败"
        )

@router.put("/rules/{rule_id}", response_model=MessageResponse, summary="更新告警规则")
def update_alert_rule(
    rule_id: int,
    rule_update: AlertRuleUpdate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("alert:create"))
) -> Any:
    """
    更新告警规则
    """
    try:
        rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
        if not rule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="告警规则不存在"
            )

        # 更新字段
        update_data = rule_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(rule, field, value)

        rule.updated_at = datetime.utcnow()

        db.commit()

        logger.info(f"用户 {current_user.username} 更新了告警规则: {rule.name}")

        return MessageResponse(
            success=True,
            message="告警规则更新成功"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新告警规则失败: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新告警规则失败"
        )