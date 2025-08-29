from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from datetime import datetime, timedelta

from app.core.db import get_db
from app.core.dependencies import get_current_active_user, get_current_user_with_permission
from app.models.postgres import Asset, AssetVulnerability, Vulnerability, AssetComplianceResult, ComplianceCheck
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

# 资产相关数据模式
from pydantic import BaseModel

class AssetBase(BaseModel):
    """资产基础模式"""
    name: str
    asset_type: str  # 服务器、工作站、网络设备等
    ip_address: str
    mac_address: Optional[str] = None
    os_version: Optional[str] = None
    is_honeypot: bool = True
    is_virtual: bool = True

class AssetCreate(AssetBase):
    """创建资产模式"""
    pass

class AssetUpdate(BaseModel):
    """更新资产模式"""
    name: Optional[str] = None
    asset_type: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    os_version: Optional[str] = None
    status: Optional[str] = None  # normal, warning, danger
    is_honeypot: Optional[bool] = None
    is_virtual: Optional[bool] = None

class AssetResponse(AssetBase):
    """资产响应模式"""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    # 统计信息
    vulnerability_count: Optional[int] = None
    alert_count: Optional[int] = None
    last_checkin: Optional[datetime] = None

    class Config:
        from_attributes = True

class AssetDetail(AssetResponse):
    """资产详情模式"""
    vulnerabilities: List[dict] = []
    compliance_results: List[dict] = []
    recent_alerts: List[dict] = []

class AssetStatistics(BaseModel):
    """资产统计模式"""
    total: int
    online: int
    offline: int
    honeypots: int
    virtual_machines: int
    physical_machines: int
    by_type: dict
    by_status: dict

class VulnerabilityResponse(BaseModel):
    """漏洞响应模式"""
    id: int
    cve_id: Optional[str]
    description: Optional[str]
    cvss_score: Optional[float]
    severity: str
    discovered_at: Optional[datetime]
    patched: bool
    first_found: datetime
    status: str

    class Config:
        from_attributes = True

@router.get("/", response_model=PaginatedResponse[AssetResponse], summary="获取资产列表")
def get_assets(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    asset_type: Optional[str] = Query(None, description="资产类型过滤"),
    status: Optional[str] = Query(None, description="状态过滤"),
    is_honeypot: Optional[bool] = Query(None, description="是否蜜罐过滤"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("asset:read"))
) -> Any:
    """
    获取资产列表

    支持多种过滤条件：
    - **asset_type**: 资产类型
    - **status**: 状态 (normal, warning, danger)
    - **is_honeypot**: 是否为蜜罐设备
    - **search**: 搜索资产名称或IP地址
    """
    try:
        skip = (page - 1) * size

        # 构建基础查询，包含统计信息
        query = db.query(
            Asset,
            func.count(AssetVulnerability.vulnerability_id).label('vulnerability_count')
        ).outerjoin(
            AssetVulnerability, Asset.id == AssetVulnerability.asset_id
        ).group_by(Asset.id)

        # 应用过滤条件
        if asset_type:
            query = query.filter(Asset.asset_type == asset_type)

        if status:
            query = query.filter(Asset.status == status)

        if is_honeypot is not None:
            query = query.filter(Asset.is_honeypot == is_honeypot)

        if search:
            query = query.filter(
                or_(
                    Asset.name.ilike(f"%{search}%"),
                    Asset.ip_address.ilike(f"%{search}%")
                )
            )

        # 获取总数
        total = query.count()

        # 分页和排序
        results = query.order_by(desc(Asset.created_at)).offset(skip).limit(size).all()

        # 构建响应数据
        assets = []
        for asset, vuln_count in results:
            asset_data = AssetResponse(
                id=asset.id,
                name=asset.name,
                asset_type=asset.asset_type,
                ip_address=asset.ip_address,
                mac_address=asset.mac_address,
                os_version=asset.os_version,
                status=asset.status,
                is_honeypot=asset.is_honeypot,
                is_virtual=asset.is_virtual,
                created_at=asset.created_at,
                updated_at=asset.updated_at,
                vulnerability_count=vuln_count or 0,
                alert_count=0,  # TODO: 实际统计告警数量
                last_checkin=asset.created_at  # TODO: 实际的最后心跳时间
            )
            assets.append(asset_data)

        return PaginatedResponse.create(
            items=assets,
            total=total,
            page=page,
            size=size
        )

    except Exception as e:
        logger.error(f"获取资产列表失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取资产列表失败"
        )

@router.get("/{asset_id}", response_model=AssetDetail, summary="获取资产详情")
def get_asset_detail(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("asset:read"))
) -> Any:
    """
    获取资产详情

    包含资产基本信息、漏洞列表、合规检查结果、最近告警等
    """
    try:
        # 查询资产基本信息
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="资产不存在"
            )

        # 查询漏洞信息
        vulnerabilities = db.query(
            AssetVulnerability, Vulnerability
        ).join(
            Vulnerability, AssetVulnerability.vulnerability_id == Vulnerability.id
        ).filter(
            AssetVulnerability.asset_id == asset_id
        ).all()

        vuln_list = []
        for asset_vuln, vuln in vulnerabilities:
            vuln_list.append({
                "id": vuln.id,
                "cve_id": vuln.cve_id,
                "description": vuln.description,
                "cvss_score": float(vuln.cvss_score) if vuln.cvss_score else None,
                "severity": vuln.severity,
                "discovered_at": vuln.discovered_at,
                "patched": vuln.patched,
                "first_found": asset_vuln.first_found,
                "status": asset_vuln.status
            })

        # 查询合规检查结果
        compliance_results = db.query(
            AssetComplianceResult, ComplianceCheck
        ).join(
            ComplianceCheck, AssetComplianceResult.check_id == ComplianceCheck.id
        ).filter(
            AssetComplianceResult.asset_id == asset_id
        ).all()

        compliance_list = []
        for result, check in compliance_results:
            compliance_list.append({
                "check_id": check.id,
                "policy_name": check.policy_name,
                "check_item": check.check_item,
                "severity": check.severity,
                "result": result.result,
                "checked_at": result.checked_at
            })

        # 构建详情响应
        asset_detail = AssetDetail(
            id=asset.id,
            name=asset.name,
            asset_type=asset.asset_type,
            ip_address=asset.ip_address,
            mac_address=asset.mac_address,
            os_version=asset.os_version,
            status=asset.status,
            is_honeypot=asset.is_honeypot,
            is_virtual=asset.is_virtual,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            vulnerability_count=len(vuln_list),
            alert_count=0,  # TODO: 实际统计告警数量
            last_checkin=asset.created_at,  # TODO: 实际的最后心跳时间
            vulnerabilities=vuln_list,
            compliance_results=compliance_list,
            recent_alerts=[]  # TODO: 查询最近告警
        )

        return asset_detail

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取资产详情失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取资产详情失败"
        )

@router.post("/", response_model=IDResponse, summary="创建资产")
def create_asset(
    asset_data: AssetCreate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("asset:create"))
) -> Any:
    """
    创建新资产

    - **name**: 资产名称
    - **asset_type**: 资产类型
    - **ip_address**: IP地址
    - **mac_address**: MAC地址（可选）
    - **os_version**: 操作系统版本（可选）
    - **is_honeypot**: 是否为蜜罐设备
    - **is_virtual**: 是否为虚拟机
    """
    try:
        # 检查IP地址是否已存在
        existing_asset = db.query(Asset).filter(Asset.ip_address == asset_data.ip_address).first()
        if existing_asset:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="IP地址已存在"
            )

        # 创建资产
        asset = Asset(
            name=asset_data.name,
            asset_type=asset_data.asset_type,
            ip_address=asset_data.ip_address,
            mac_address=asset_data.mac_address,
            os_version=asset_data.os_version,
            is_honeypot=asset_data.is_honeypot,
            is_virtual=asset_data.is_virtual,
            status='normal'
        )

        db.add(asset)
        db.commit()
        db.refresh(asset)

        logger.info(f"用户 {current_user.username} 创建了资产: {asset.name}")

        return IDResponse(
            id=asset.id,
            message="资产创建成功"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建资产失败: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建资产失败"
        )

@router.put("/{asset_id}", response_model=MessageResponse, summary="更新资产信息")
def update_asset(
    asset_id: int,
    asset_update: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("asset:update"))
) -> Any:
    """
    更新资产信息
    """
    try:
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="资产不存在"
            )

        # 如果更新IP地址，检查是否冲突
        if asset_update.ip_address and asset_update.ip_address != asset.ip_address:
            existing_asset = db.query(Asset).filter(
                and_(
                    Asset.ip_address == asset_update.ip_address,
                    Asset.id != asset_id
                )
            ).first()
            if existing_asset:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="IP地址已被其他资产使用"
                )

        # 更新字段
        update_data = asset_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(asset, field, value)

        asset.updated_at = datetime.utcnow()

        db.commit()

        logger.info(f"用户 {current_user.username} 更新了资产: {asset.name}")

        return MessageResponse(
            success=True,
            message="资产信息更新成功"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新资产信息失败: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新资产信息失败"
        )

@router.delete("/{asset_id}", response_model=MessageResponse, summary="删除资产")
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("asset:delete"))
) -> Any:
    """
    删除资产

    注意：删除资产会同时删除相关的漏洞记录、告警记录等
    """
    try:
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="资产不存在"
            )

        asset_name = asset.name

        # 删除资产（级联删除相关记录）
        db.delete(asset)
        db.commit()

        logger.info(f"用户 {current_user.username} 删除了资产: {asset_name}")

        return MessageResponse(
            success=True,
            message="资产删除成功"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除资产失败: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除资产失败"
        )

@router.get("/statistics", response_model=AssetStatistics, summary="获取资产统计")
def get_asset_statistics(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("asset:read"))
) -> Any:
    """
    获取资产统计数据

    包含总数、在线/离线数量、蜜罐/物理机数量、按类型/状态分布等
    """
    try:
        # 总资产数
        total = db.query(Asset).count()

        # 在线/离线统计（基于最后心跳时间）
        offline_threshold = datetime.utcnow() - timedelta(hours=24)
        online = db.query(Asset).filter(Asset.updated_at >= offline_threshold).count()
        offline = total - online

        # 蜜罐/物理机统计
        honeypots = db.query(Asset).filter(Asset.is_honeypot == True).count()
        virtual_machines = db.query(Asset).filter(Asset.is_virtual == True).count()
        physical_machines = total - virtual_machines

        # 按类型统计
        type_stats = db.query(
            Asset.asset_type,
            func.count(Asset.id).label('count')
        ).group_by(Asset.asset_type).all()

        by_type = {asset_type: count for asset_type, count in type_stats}

        # 按状态统计
        status_stats = db.query(
            Asset.status,
            func.count(Asset.id).label('count')
        ).group_by(Asset.status).all()

        by_status = {status_name: count for status_name, count in status_stats}

        return AssetStatistics(
            total=total,
            online=online,
            offline=offline,
            honeypots=honeypots,
            virtual_machines=virtual_machines,
            physical_machines=physical_machines,
            by_type=by_type,
            by_status=by_status
        )

    except Exception as e:
        logger.error(f"获取资产统计失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取资产统计失败"
        )