from typing import Any, List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
import psutil
import platform
import os

from app.core.db import get_db
from app.core.dependencies import get_current_active_user, get_admin_user
from app.core.config import settings
from app.schemas.user import User as UserSchema
from app.schemas.common import (
    MessageResponse,
    HealthCheckResponse
)
import logging

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter()

# 系统管理相关数据模式
from pydantic import BaseModel

class SystemInfo(BaseModel):
    """系统信息模式"""
    hostname: str
    platform: str
    platform_version: str
    architecture: str
    cpu_count: int
    memory_total: int  # GB
    disk_total: int    # GB
    uptime: int        # 秒
    python_version: str

class SystemStatus(BaseModel):
    """系统状态模式"""
    cpu_usage: float      # 百分比
    memory_usage: float   # 百分比
    disk_usage: float     # 百分比
    network_io: Dict[str, int]  # bytes_sent, bytes_recv
    active_connections: int
    load_average: Optional[List[float]] = None

class ServiceStatus(BaseModel):
    """服务状态模式"""
    database: str
    redis: str
    manticore: str
    celery: str

class SystemConfiguration(BaseModel):
    """系统配置模式"""
    debug_mode: bool
    log_level: str
    max_upload_size: int
    session_timeout: int
    backup_enabled: bool
    backup_interval: int

class BackupInfo(BaseModel):
    """备份信息模式"""
    id: int
    backup_type: str  # full, incremental
    file_path: str
    file_size: int    # bytes
    created_at: datetime
    status: str       # success, failed, in_progress

class SystemLog(BaseModel):
    """系统日志模式"""
    timestamp: datetime
    level: str
    module: str
    message: str
    details: Optional[dict] = None

@router.get("/health", response_model=HealthCheckResponse, summary="系统健康检查")
def health_check(
    db: Session = Depends(get_db)
) -> Any:
    """
    系统健康检查

    检查数据库连接、服务状态等
    """
    try:
        # 检查数据库连接
        db.execute("SELECT 1")
        database_status = "healthy"

        # 检查服务状态
        services = {
            "database": "healthy",
            "redis": "healthy",      # TODO: 实际检查Redis连接
            "manticore": "healthy",  # TODO: 实际检查Manticore连接
            "celery": "healthy"      # TODO: 实际检查Celery状态
        }

        return HealthCheckResponse(
            status="healthy",
            timestamp=datetime.utcnow(),
            version="1.0.0",
            database=database_status,
            services=services
        )

    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        return HealthCheckResponse(
            status="unhealthy",
            timestamp=datetime.utcnow(),
            version="1.0.0",
            database="unhealthy",
            services={"error": str(e)}
        )

@router.get("/info", response_model=SystemInfo, summary="获取系统信息")
def get_system_info(
    current_user: UserSchema = Depends(get_admin_user)
) -> Any:
    """
    获取系统基本信息

    需要管理员权限
    """
    try:
        # 获取系统信息
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')

        return SystemInfo(
            hostname=platform.node(),
            platform=platform.system(),
            platform_version=platform.release(),
            architecture=platform.machine(),
            cpu_count=psutil.cpu_count(),
            memory_total=round(memory_info.total / (1024**3), 2),  # GB
            disk_total=round(disk_info.total / (1024**3), 2),      # GB
            uptime=int(psutil.boot_time()),
            python_version=platform.python_version()
        )

    except Exception as e:
        logger.error(f"获取系统信息失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取系统信息失败"
        )

@router.get("/status", response_model=SystemStatus, summary="获取系统状态")
def get_system_status(
    current_user: UserSchema = Depends(get_admin_user)
) -> Any:
    """
    获取系统实时状态

    包含CPU、内存、磁盘使用率等
    """
    try:
        # CPU使用率
        cpu_usage = psutil.cpu_percent(interval=1)

        # 内存使用率
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent

        # 磁盘使用率
        disk_info = psutil.disk_usage('/')
        disk_usage = (disk_info.used / disk_info.total) * 100

        # 网络IO
        network_info = psutil.net_io_counters()
        network_io = {
            "bytes_sent": network_info.bytes_sent,
            "bytes_recv": network_info.bytes_recv
        }

        # 活跃连接数
        active_connections = len(psutil.net_connections())

        # 负载平均值（仅Linux）
        load_average = None
        if platform.system() == "Linux":
            load_average = list(os.getloadavg())

        return SystemStatus(
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            network_io=network_io,
            active_connections=active_connections,
            load_average=load_average
        )

    except Exception as e:
        logger.error(f"获取系统状态失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取系统状态失败"
        )