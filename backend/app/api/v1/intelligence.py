from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from datetime import datetime, timedelta

from app.core.db import get_db
from app.core.dependencies import get_current_active_user, get_current_user_with_permission
from app.models.postgres import IOC, ThreatFamily, IntelligenceSource
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

# 威胁情报相关数据模式
from pydantic import BaseModel

class IOCBase(BaseModel):
    """IOC基础模式"""
    ioc_type: str  # ip, domain, hash, url, email等
    value: str
    threat_type: Optional[str] = None
    severity: str = 'medium'  # low, medium, high, critical
    source: Optional[str] = None
    confidence: Optional[int] = None  # 0-100

class IOCCreate(IOCBase):
    """创建IOC模式"""
    expires_at: Optional[datetime] = None

class IOCUpdate(BaseModel):
    """更新IOC模式"""
    threat_type: Optional[str] = None
    severity: Optional[str] = None
    confidence: Optional[int] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None

class IOCResponse(IOCBase):
    """IOC响应模式"""
    id: int
    first_seen: datetime
    last_seen: datetime
    expires_at: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True

class IOCDetail(IOCResponse):
    """IOC详情模式"""
    related_threats: List[dict] = []
    detection_history: List[dict] = []

class ThreatFamilyBase(BaseModel):
    """威胁家族基础模式"""
    name: str
    description: Optional[str] = None

class ThreatFamilyCreate(ThreatFamilyBase):
    """创建威胁家族模式"""
    associated_iocs: Optional[List[int]] = []

class ThreatFamilyResponse(ThreatFamilyBase):
    """威胁家族响应模式"""
    id: int
    associated_iocs: Optional[List[int]] = []

    class Config:
        from_attributes = True

class IntelligenceSourceBase(BaseModel):
    """情报源基础模式"""
    name: str
    source_type: str  # internal, commercial, open_source
    url: Optional[str] = None
    enabled: bool = True
    sync_interval: Optional[int] = None  # 同步间隔(分钟)

class IntelligenceSourceCreate(IntelligenceSourceBase):
    """创建情报源模式"""
    api_key: Optional[str] = None

class IntelligenceSourceResponse(IntelligenceSourceBase):
    """情报源响应模式"""
    id: int
    last_sync: Optional[datetime]

    class Config:
        from_attributes = True

class IntelligenceStatistics(BaseModel):
    """情报统计模式"""
    total_iocs: int
    active_iocs: int
    expired_iocs: int
    by_type: dict
    by_severity: dict
    recent_additions: int
    threat_families: int
    intelligence_sources: int

@router.get("/iocs", response_model=PaginatedResponse[IOCResponse], summary="获取IOC列表")
def get_iocs(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    ioc_type: Optional[str] = Query(None, description="IOC类型过滤"),
    severity: Optional[str] = Query(None, description="严重程度过滤"),
    is_active: Optional[bool] = Query(None, description="是否活跃过滤"),
    search: Optional[str] = Query(None, description="搜索IOC值"),
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("intelligence:read"))
) -> Any:
    """
    获取IOC（威胁指标）列表
    
    支持多种过滤条件：
    - **ioc_type**: IOC类型 (ip, domain, hash, url, email)
    - **severity**: 严重程度 (low, medium, high, critical)
    - **is_active**: 是否活跃
    - **search**: 搜索IOC值
    """
    try:
        skip = (page - 1) * size
        
        query = db.query(IOC)
        
        # 应用过滤条件
        if ioc_type:
            query = query.filter(IOC.ioc_type == ioc_type)
        
        if severity:
            query = query.filter(IOC.severity == severity)
        
        if is_active is not None:
            query = query.filter(IOC.is_active == is_active)
        
        if search:
            query = query.filter(IOC.value.ilike(f"%{search}%"))
        
        # 获取总数
        total = query.count()
        
        # 分页和排序
        iocs = query.order_by(desc(IOC.last_seen)).offset(skip).limit(size).all()
        
        return PaginatedResponse.create(
            items=iocs,
            total=total,
            page=page,
            size=size
        )
        
    except Exception as e:
        logger.error(f"获取IOC列表失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取IOC列表失败"
        )

@router.post("/iocs", response_model=IDResponse, summary="创建IOC")
def create_ioc(
    ioc_data: IOCCreate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("intelligence:create"))
) -> Any:
    """
    创建新的IOC（威胁指标）
    
    - **ioc_type**: IOC类型
    - **value**: IOC值
    - **threat_type**: 威胁类型
    - **severity**: 严重程度
    - **source**: 情报源
    - **confidence**: 置信度 (0-100)
    - **expires_at**: 过期时间
    """
    try:
        # 检查IOC是否已存在
        existing_ioc = db.query(IOC).filter(IOC.value == ioc_data.value).first()
        if existing_ioc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="IOC已存在"
            )
        
        # 创建IOC
        ioc = IOC(
            ioc_type=ioc_data.ioc_type,
            value=ioc_data.value,
            threat_type=ioc_data.threat_type,
            severity=ioc_data.severity,
            source=ioc_data.source,
            confidence=ioc_data.confidence,
            expires_at=ioc_data.expires_at
        )
        
        db.add(ioc)
        db.commit()
        db.refresh(ioc)
        
        logger.info(f"用户 {current_user.username} 创建了IOC: {ioc.value}")
        
        return IDResponse(
            id=ioc.id,
            message="IOC创建成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建IOC失败: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建IOC失败"
        )

@router.get("/iocs/{ioc_id}", response_model=IOCDetail, summary="获取IOC详情")
def get_ioc_detail(
    ioc_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("intelligence:read"))
) -> Any:
    """
    获取IOC详情
    
    包含IOC基本信息、关联威胁、检测历史等
    """
    try:
        ioc = db.query(IOC).filter(IOC.id == ioc_id).first()
        if not ioc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="IOC不存在"
            )
        
        # 模拟关联威胁数据
        related_threats = [
            {
                "family_name": "APT29",
                "description": "高级持续性威胁组织",
                "first_seen": "2024-01-10T08:00:00Z"
            }
        ]
        
        # 模拟检测历史
        detection_history = [
            {
                "timestamp": "2024-01-15T14:30:00Z",
                "asset_name": "Honeypot-01",
                "detection_type": "network_connection",
                "confidence": 0.95
            }
        ]
        
        ioc_detail = IOCDetail(
            id=ioc.id,
            ioc_type=ioc.ioc_type,
            value=ioc.value,
            threat_type=ioc.threat_type,
            severity=ioc.severity,
            source=ioc.source,
            confidence=ioc.confidence,
            first_seen=ioc.first_seen,
            last_seen=ioc.last_seen,
            expires_at=ioc.expires_at,
            is_active=ioc.is_active,
            related_threats=related_threats,
            detection_history=detection_history
        )
        
        return ioc_detail
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取IOC详情失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取IOC详情失败"
        )

@router.get("/statistics", response_model=IntelligenceStatistics, summary="获取情报统计")
def get_intelligence_statistics(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("intelligence:read"))
) -> Any:
    """
    获取威胁情报统计数据
    
    包含IOC总数、活跃数量、按类型分布、按严重程度分布等
    """
    try:
        # IOC统计
        total_iocs = db.query(IOC).count()
        active_iocs = db.query(IOC).filter(IOC.is_active == True).count()
        
        # 过期IOC统计
        now = datetime.utcnow()
        expired_iocs = db.query(IOC).filter(
            and_(IOC.expires_at.isnot(None), IOC.expires_at < now)
        ).count()
        
        # 按类型统计
        type_stats = db.query(
            IOC.ioc_type,
            func.count(IOC.id).label('count')
        ).group_by(IOC.ioc_type).all()
        
        by_type = {ioc_type: count for ioc_type, count in type_stats}
        
        # 按严重程度统计
        severity_stats = db.query(
            IOC.severity,
            func.count(IOC.id).label('count')
        ).group_by(IOC.severity).all()
        
        by_severity = {severity: count for severity, count in severity_stats}
        
        # 最近添加的IOC数量（24小时内）
        yesterday = now - timedelta(days=1)
        recent_additions = db.query(IOC).filter(IOC.first_seen >= yesterday).count()
        
        # 威胁家族数量
        threat_families = db.query(ThreatFamily).count()
        
        # 情报源数量
        intelligence_sources = db.query(IntelligenceSource).count()
        
        return IntelligenceStatistics(
            total_iocs=total_iocs,
            active_iocs=active_iocs,
            expired_iocs=expired_iocs,
            by_type=by_type,
            by_severity=by_severity,
            recent_additions=recent_additions,
            threat_families=threat_families,
            intelligence_sources=intelligence_sources
        )
        
    except Exception as e:
        logger.error(f"获取情报统计失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取情报统计失败"
        )
