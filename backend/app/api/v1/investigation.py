from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime, timedelta

from app.core.db import get_db
from app.core.dependencies import get_current_active_user, get_current_user_with_permission
from app.models.postgres import InvestigationSession, User
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

# 调查与响应相关数据模式
from pydantic import BaseModel

class InvestigationSessionBase(BaseModel):
    """调查会话基础模式"""
    name: str
    description: Optional[str] = None

class InvestigationSessionCreate(InvestigationSessionBase):
    """创建调查会话模式"""
    pass

class InvestigationSessionUpdate(BaseModel):
    """更新调查会话模式"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None  # active, completed, archived

class InvestigationSessionResponse(InvestigationSessionBase):
    """调查会话响应模式"""
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    status: str
    
    # 关联数据
    creator_name: Optional[str] = None

    class Config:
        from_attributes = True

class InvestigationSessionDetail(InvestigationSessionResponse):
    """调查会话详情模式"""
    timeline: List[dict] = []
    evidence: List[dict] = []
    notes: List[dict] = []
    related_alerts: List[dict] = []

class TimelineEvent(BaseModel):
    """时间线事件模式"""
    timestamp: datetime
    event_type: str
    description: str
    source: str
    confidence: float
    details: Optional[dict] = None

class Evidence(BaseModel):
    """证据模式"""
    id: int
    type: str  # file, network_log, system_log, screenshot
    name: str
    description: Optional[str]
    file_path: Optional[str]
    hash_value: Optional[str]
    collected_at: datetime
    collected_by: str

class InvestigationNote(BaseModel):
    """调查笔记模式"""
    id: int
    content: str
    created_at: datetime
    created_by: str
    tags: List[str] = []

class ResponseAction(BaseModel):
    """响应动作模式"""
    id: int
    action_type: str  # isolate, block_ip, quarantine_file, reset_password
    target: str
    description: str
    status: str  # pending, in_progress, completed, failed
    executed_at: Optional[datetime]
    executed_by: Optional[str]
    result: Optional[str]

class InvestigationStatistics(BaseModel):
    """调查统计模式"""
    total_sessions: int
    active_sessions: int
    completed_sessions: int
    archived_sessions: int
    avg_resolution_time: Optional[float] = None  # 小时
    total_evidence: int
    total_actions: int

@router.get("/", response_model=PaginatedResponse[InvestigationSessionResponse], summary="获取调查会话列表")
def get_investigation_sessions(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="状态过滤"),
    created_by: Optional[int] = Query(None, description="创建者过滤"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("investigation:read"))
) -> Any:
    """
    获取调查会话列表
    
    支持多种过滤条件：
    - **status**: 会话状态 (active, completed, archived)
    - **created_by**: 创建者用户ID
    - **search**: 搜索会话名称或描述
    """
    try:
        skip = (page - 1) * size
        
        # 构建查询
        query = db.query(InvestigationSession, User.full_name.label('creator_name')).join(
            User, InvestigationSession.created_by == User.id
        )
        
        # 应用过滤条件
        if status:
            query = query.filter(InvestigationSession.status == status)
        
        if created_by:
            query = query.filter(InvestigationSession.created_by == created_by)
        
        if search:
            query = query.filter(
                or_(
                    InvestigationSession.name.ilike(f"%{search}%"),
                    InvestigationSession.description.ilike(f"%{search}%")
                )
            )
        
        # 获取总数
        total = query.count()
        
        # 分页和排序
        results = query.order_by(desc(InvestigationSession.created_at)).offset(skip).limit(size).all()
        
        # 构建响应数据
        sessions = []
        for session, creator_name in results:
            session_data = InvestigationSessionResponse(
                id=session.id,
                name=session.name,
                description=session.description,
                created_by=session.created_by,
                created_at=session.created_at,
                updated_at=session.updated_at,
                status=session.status,
                creator_name=creator_name
            )
            sessions.append(session_data)
        
        return PaginatedResponse.create(
            items=sessions,
            total=total,
            page=page,
            size=size
        )
        
    except Exception as e:
        logger.error(f"获取调查会话列表失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取调查会话列表失败"
        )

@router.post("/", response_model=IDResponse, summary="创建调查会话")
def create_investigation_session(
    session_data: InvestigationSessionCreate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("investigation:create"))
) -> Any:
    """
    创建新的调查会话
    
    - **name**: 会话名称
    - **description**: 会话描述
    """
    try:
        # 创建调查会话
        session = InvestigationSession(
            name=session_data.name,
            description=session_data.description,
            created_by=current_user.id,
            status='active'
        )
        
        db.add(session)
        db.commit()
        db.refresh(session)
        
        logger.info(f"用户 {current_user.username} 创建了调查会话: {session.name}")
        
        return IDResponse(
            id=session.id,
            message="调查会话创建成功"
        )
        
    except Exception as e:
        logger.error(f"创建调查会话失败: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建调查会话失败"
        )

@router.get("/{session_id}", response_model=InvestigationSessionDetail, summary="获取调查会话详情")
def get_investigation_session_detail(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("investigation:read"))
) -> Any:
    """
    获取调查会话详情
    
    包含会话基本信息、时间线、证据、笔记、关联告警等
    """
    try:
        # 查询会话详情
        result = db.query(InvestigationSession, User.full_name.label('creator_name')).join(
            User, InvestigationSession.created_by == User.id
        ).filter(InvestigationSession.id == session_id).first()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="调查会话不存在"
            )
        
        session, creator_name = result
        
        # 模拟时间线数据
        timeline = [
            {
                "timestamp": "2024-01-15T10:30:00Z",
                "event_type": "alert_triggered",
                "description": "检测到可疑进程创建",
                "source": "EDR",
                "confidence": 0.95,
                "details": {"process": "powershell.exe", "command_line": "encoded_command"}
            },
            {
                "timestamp": "2024-01-15T10:32:00Z",
                "event_type": "network_connection",
                "description": "建立外部网络连接",
                "source": "Network Monitor",
                "confidence": 0.88,
                "details": {"destination_ip": "192.168.1.100", "port": 443}
            }
        ]
        
        # 模拟证据数据
        evidence = [
            {
                "id": 1,
                "type": "file",
                "name": "suspicious_script.ps1",
                "description": "可疑PowerShell脚本",
                "file_path": "/evidence/suspicious_script.ps1",
                "hash_value": "sha256:abc123...",
                "collected_at": "2024-01-15T10:35:00Z",
                "collected_by": "analyst"
            }
        ]
        
        # 模拟笔记数据
        notes = [
            {
                "id": 1,
                "content": "初步分析显示这是一个APT攻击的早期阶段",
                "created_at": "2024-01-15T11:00:00Z",
                "created_by": "analyst",
                "tags": ["apt", "initial_analysis"]
            }
        ]
        
        # 模拟关联告警
        related_alerts = [
            {
                "id": 1,
                "alert_name": "可疑进程创建",
                "severity": "high",
                "created_at": "2024-01-15T10:30:00Z"
            }
        ]
        
        session_detail = InvestigationSessionDetail(
            id=session.id,
            name=session.name,
            description=session.description,
            created_by=session.created_by,
            created_at=session.created_at,
            updated_at=session.updated_at,
            status=session.status,
            creator_name=creator_name,
            timeline=timeline,
            evidence=evidence,
            notes=notes,
            related_alerts=related_alerts
        )
        
        return session_detail
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取调查会话详情失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取调查会话详情失败"
        )

@router.get("/statistics", response_model=InvestigationStatistics, summary="获取调查统计")
def get_investigation_statistics(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("investigation:read"))
) -> Any:
    """
    获取调查与响应统计数据
    
    包含会话总数、各状态数量、平均解决时间等
    """
    try:
        # 会话统计
        total_sessions = db.query(InvestigationSession).count()
        active_sessions = db.query(InvestigationSession).filter(InvestigationSession.status == 'active').count()
        completed_sessions = db.query(InvestigationSession).filter(InvestigationSession.status == 'completed').count()
        archived_sessions = db.query(InvestigationSession).filter(InvestigationSession.status == 'archived').count()
        
        # 平均解决时间（模拟数据）
        avg_resolution_time = 24.5  # 小时
        
        # 证据和动作统计（模拟数据）
        total_evidence = 156
        total_actions = 89
        
        return InvestigationStatistics(
            total_sessions=total_sessions,
            active_sessions=active_sessions,
            completed_sessions=completed_sessions,
            archived_sessions=archived_sessions,
            avg_resolution_time=avg_resolution_time,
            total_evidence=total_evidence,
            total_actions=total_actions
        )
        
    except Exception as e:
        logger.error(f"获取调查统计失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取调查统计失败"
        )
