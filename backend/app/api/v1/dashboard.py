from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta

from app.core.db import get_db
from app.core.dependencies import get_current_active_user
from app.models.postgres import Alert, Asset, Event, User
from app.schemas.user import User as UserSchema
from app.schemas.common import StatisticsResponse
import logging

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter()

# 安全态势数据模式
from pydantic import BaseModel

class SecurityMetrics(BaseModel):
    """安全态势关键指标"""
    today_alerts: int
    unhandled_alerts: int
    affected_assets: int
    active_hunting_tasks: int
    handled_events: int

class AlertTrendData(BaseModel):
    """告警趋势数据"""
    dates: List[str]
    counts: List[int]
    critical_counts: List[int]
    high_counts: List[int]
    medium_counts: List[int]

class ThreatDistribution(BaseModel):
    """威胁类型分布"""
    types: List[str]
    counts: List[int]

class AssetStatusDistribution(BaseModel):
    """资产状态分布"""
    normal: int
    warning: int
    danger: int
    offline: int
    normal_percent: float
    warning_percent: float
    danger_percent: float
    offline_percent: float
    total: int

class RecentAlert(BaseModel):
    """最近告警"""
    id: int
    alert_name: str
    severity: str
    asset_name: str
    created_at: datetime

class BigScreenData(BaseModel):
    """大屏视图数据"""
    metrics: SecurityMetrics
    alert_trend: AlertTrendData
    threat_distribution: ThreatDistribution
    asset_status: AssetStatusDistribution
    recent_alerts: List[RecentAlert]

@router.get("/metrics", response_model=SecurityMetrics, summary="获取安全态势关键指标")
def get_security_metrics(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_active_user)
) -> Any:
    """
    获取安全态势关键指标
    
    返回今日新增告警、未处理告警、受影响资产等关键数据
    """
    try:
        # 获取今天的日期范围
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())
        
        # 今日新增告警
        today_alerts = db.query(Alert).filter(
            and_(
                Alert.created_at >= today_start,
                Alert.created_at <= today_end
            )
        ).count()
        
        # 未处理告警
        unhandled_alerts = db.query(Alert).filter(
            Alert.status == 'unhandled'
        ).count()
        
        # 受影响资产（有告警的资产）
        affected_assets = db.query(Alert.asset_id).distinct().count()
        
        # 活跃威胁狩猎任务（这里暂时返回模拟数据）
        active_hunting_tasks = 8
        
        # 已处理安全事件（今日）
        handled_events = db.query(Alert).filter(
            and_(
                Alert.status == 'resolved',
                Alert.handled_at >= today_start,
                Alert.handled_at <= today_end
            )
        ).count()
        
        return SecurityMetrics(
            today_alerts=today_alerts,
            unhandled_alerts=unhandled_alerts,
            affected_assets=affected_assets,
            active_hunting_tasks=active_hunting_tasks,
            handled_events=handled_events
        )
        
    except Exception as e:
        logger.error(f"获取安全态势指标失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取安全态势指标失败"
        )

@router.get("/alert-trend", response_model=AlertTrendData, summary="获取告警趋势数据")
def get_alert_trend(
    days: int = Query(7, ge=1, le=30, description="天数"),
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_active_user)
) -> Any:
    """
    获取告警趋势数据
    
    - **days**: 查询天数，默认7天，最大30天
    """
    try:
        # 计算日期范围
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days-1)
        
        dates = []
        counts = []
        critical_counts = []
        high_counts = []
        medium_counts = []
        
        # 按天统计告警数据
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            date_start = datetime.combine(current_date, datetime.min.time())
            date_end = datetime.combine(current_date, datetime.max.time())
            
            # 总告警数
            total_count = db.query(Alert).filter(
                and_(
                    Alert.created_at >= date_start,
                    Alert.created_at <= date_end
                )
            ).count()
            
            # 紧急告警数
            critical_count = db.query(Alert).filter(
                and_(
                    Alert.created_at >= date_start,
                    Alert.created_at <= date_end,
                    Alert.severity == 'critical'
                )
            ).count()
            
            # 高危告警数
            high_count = db.query(Alert).filter(
                and_(
                    Alert.created_at >= date_start,
                    Alert.created_at <= date_end,
                    Alert.severity == 'high'
                )
            ).count()
            
            # 中危告警数
            medium_count = db.query(Alert).filter(
                and_(
                    Alert.created_at >= date_start,
                    Alert.created_at <= date_end,
                    Alert.severity == 'medium'
                )
            ).count()
            
            dates.append(current_date.strftime("%m/%d"))
            counts.append(total_count)
            critical_counts.append(critical_count)
            high_counts.append(high_count)
            medium_counts.append(medium_count)
        
        return AlertTrendData(
            dates=dates,
            counts=counts,
            critical_counts=critical_counts,
            high_counts=high_counts,
            medium_counts=medium_counts
        )
        
    except Exception as e:
        logger.error(f"获取告警趋势数据失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取告警趋势数据失败"
        )

@router.get("/threat-distribution", response_model=ThreatDistribution, summary="获取威胁类型分布")
def get_threat_distribution(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_active_user)
) -> Any:
    """
    获取威胁类型分布数据
    """
    try:
        # 这里使用模拟数据，实际应该从数据库统计
        # 可以根据告警名称或事件类型进行分类统计
        threat_types = [
            "恶意软件", "可疑脚本", "横向移动", 
            "持久化", "数据渗出", "暴力破解"
        ]
        
        threat_counts = []
        for threat_type in threat_types:
            # 这里应该根据实际的威胁分类逻辑进行统计
            # 暂时使用模拟数据
            if threat_type == "恶意软件":
                count = 42
            elif threat_type == "可疑脚本":
                count = 38
            elif threat_type == "横向移动":
                count = 15
            elif threat_type == "持久化":
                count = 24
            elif threat_type == "数据渗出":
                count = 8
            else:  # 暴力破解
                count = 22
            
            threat_counts.append(count)
        
        return ThreatDistribution(
            types=threat_types,
            counts=threat_counts
        )
        
    except Exception as e:
        logger.error(f"获取威胁类型分布失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取威胁类型分布失败"
        )

@router.get("/asset-status", response_model=AssetStatusDistribution, summary="获取资产状态分布")
def get_asset_status_distribution(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_active_user)
) -> Any:
    """
    获取资产状态分布数据
    """
    try:
        # 统计各状态的资产数量
        normal_count = db.query(Asset).filter(Asset.status == 'normal').count()
        warning_count = db.query(Asset).filter(Asset.status == 'warning').count()
        danger_count = db.query(Asset).filter(Asset.status == 'danger').count()
        
        # 离线资产（假设超过24小时没有心跳的为离线）
        offline_threshold = datetime.now() - timedelta(hours=24)
        offline_count = db.query(Asset).filter(
            or_(
                Asset.last_checkin < offline_threshold,
                Asset.last_checkin.is_(None)
            )
        ).count()
        
        total_count = normal_count + warning_count + danger_count + offline_count
        
        # 计算百分比
        if total_count > 0:
            normal_percent = round((normal_count / total_count) * 100, 1)
            warning_percent = round((warning_count / total_count) * 100, 1)
            danger_percent = round((danger_count / total_count) * 100, 1)
            offline_percent = round((offline_count / total_count) * 100, 1)
        else:
            normal_percent = warning_percent = danger_percent = offline_percent = 0.0
        
        return AssetStatusDistribution(
            normal=normal_count,
            warning=warning_count,
            danger=danger_count,
            offline=offline_count,
            normal_percent=normal_percent,
            warning_percent=warning_percent,
            danger_percent=danger_percent,
            offline_percent=offline_percent,
            total=total_count
        )
        
    except Exception as e:
        logger.error(f"获取资产状态分布失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取资产状态分布失败"
        )

@router.get("/recent-alerts", response_model=List[RecentAlert], summary="获取最近高优先级告警")
def get_recent_alerts(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_active_user)
) -> Any:
    """
    获取最近的高优先级告警
    
    - **limit**: 返回数量，默认10条，最大50条
    """
    try:
        # 查询最近的高优先级告警
        alerts = db.query(Alert, Asset.name.label('asset_name')).join(
            Asset, Alert.asset_id == Asset.id
        ).filter(
            Alert.severity.in_(['critical', 'high'])
        ).order_by(
            Alert.created_at.desc()
        ).limit(limit).all()
        
        recent_alerts = []
        for alert, asset_name in alerts:
            recent_alerts.append(RecentAlert(
                id=alert.id,
                alert_name=alert.alert_name,
                severity=alert.severity,
                asset_name=asset_name,
                created_at=alert.created_at
            ))
        
        return recent_alerts
        
    except Exception as e:
        logger.error(f"获取最近告警失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取最近告警失败"
        )

@router.get("/big-screen", response_model=BigScreenData, summary="获取大屏视图数据")
def get_big_screen_data(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_active_user)
) -> Any:
    """
    获取大屏视图所需的综合数据
    
    包含所有安全态势相关的数据，用于大屏展示
    """
    try:
        # 获取各个模块的数据
        metrics = get_security_metrics(db, current_user)
        alert_trend = get_alert_trend(7, db, current_user)
        threat_distribution = get_threat_distribution(db, current_user)
        asset_status = get_asset_status_distribution(db, current_user)
        recent_alerts = get_recent_alerts(5, db, current_user)
        
        return BigScreenData(
            metrics=metrics,
            alert_trend=alert_trend,
            threat_distribution=threat_distribution,
            asset_status=asset_status,
            recent_alerts=recent_alerts
        )
        
    except Exception as e:
        logger.error(f"获取大屏数据失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取大屏数据失败"
        )
