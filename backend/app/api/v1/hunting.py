from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime, timedelta

from app.core.db import get_db
from app.core.dependencies import get_current_active_user, get_current_user_with_permission
from app.models.postgres import HuntingTask, User
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

# 威胁狩猎相关数据模式
from pydantic import BaseModel

class HuntingTaskBase(BaseModel):
    """狩猎任务基础模式"""
    name: str
    query_string: str
    query_type: str = 'advanced'  # advanced, visual

class HuntingTaskCreate(HuntingTaskBase):
    """创建狩猎任务模式"""
    pass

class HuntingTaskUpdate(BaseModel):
    """更新狩猎任务模式"""
    name: Optional[str] = None
    query_string: Optional[str] = None
    query_type: Optional[str] = None

class HuntingTaskResponse(HuntingTaskBase):
    """狩猎任务响应模式"""
    id: int
    created_by: int
    created_at: datetime
    status: str  # pending, running, completed, failed
    result_count: int
    completed_at: Optional[datetime]

    # 关联数据
    creator_name: Optional[str] = None

    class Config:
        from_attributes = True

class HuntingTaskDetail(HuntingTaskResponse):
    """狩猎任务详情模式"""
    results: List[dict] = []
    execution_log: List[dict] = []

class HuntingTemplate(BaseModel):
    """狩猎模板模式"""
    id: int
    name: str
    description: str
    query_template: str
    category: str
    difficulty: str  # easy, medium, hard
    tags: List[str] = []

class HuntingStatistics(BaseModel):
    """狩猎统计模式"""
    total_tasks: int
    running_tasks: int
    completed_tasks: int
    failed_tasks: int
    today_tasks: int
    total_results: int
    avg_execution_time: Optional[float] = None

@router.get("/", response_model=PaginatedResponse[HuntingTaskResponse], summary="获取狩猎任务列表")
def get_hunting_tasks(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="任务状态过滤"),
    created_by: Optional[int] = Query(None, description="创建者过滤"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("hunting:read"))
) -> Any:
    """
    获取威胁狩猎任务列表

    支持多种过滤条件：
    - **status**: 任务状态 (pending, running, completed, failed)
    - **created_by**: 创建者用户ID
    - **search**: 搜索任务名称或查询语句
    """
    try:
        skip = (page - 1) * size

        # 构建查询
        query = db.query(HuntingTask, User.full_name.label('creator_name')).join(
            User, HuntingTask.created_by == User.id
        )

        # 应用过滤条件
        if status:
            query = query.filter(HuntingTask.status == status)

        if created_by:
            query = query.filter(HuntingTask.created_by == created_by)

        if search:
            query = query.filter(
                or_(
                    HuntingTask.name.ilike(f"%{search}%"),
                    HuntingTask.query_string.ilike(f"%{search}%")
                )
            )

        # 获取总数
        total = query.count()

        # 分页和排序
        results = query.order_by(desc(HuntingTask.created_at)).offset(skip).limit(size).all()

        # 构建响应数据
        tasks = []
        for task, creator_name in results:
            task_data = HuntingTaskResponse(
                id=task.id,
                name=task.name,
                query_string=task.query_string,
                query_type=task.query_type,
                created_by=task.created_by,
                created_at=task.created_at,
                status=task.status,
                result_count=task.result_count,
                completed_at=task.completed_at,
                creator_name=creator_name
            )
            tasks.append(task_data)

        return PaginatedResponse.create(
            items=tasks,
            total=total,
            page=page,
            size=size
        )

    except Exception as e:
        logger.error(f"获取狩猎任务列表失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取狩猎任务列表失败"
        )

@router.post("/", response_model=IDResponse, summary="创建狩猎任务")
def create_hunting_task(
    task_data: HuntingTaskCreate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("hunting:create"))
) -> Any:
    """
    创建威胁狩猎任务

    - **name**: 任务名称
    - **query_string**: 查询语句
    - **query_type**: 查询类型 (advanced, visual)
    """
    try:
        # 创建狩猎任务
        task = HuntingTask(
            name=task_data.name,
            query_string=task_data.query_string,
            query_type=task_data.query_type,
            created_by=current_user.id,
            status='pending'
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        logger.info(f"用户 {current_user.username} 创建了狩猎任务: {task.name}")

        return IDResponse(
            id=task.id,
            message="狩猎任务创建成功"
        )

    except Exception as e:
        logger.error(f"创建狩猎任务失败: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建狩猎任务失败"
        )

@router.get("/{task_id}", response_model=HuntingTaskDetail, summary="获取狩猎任务详情")
def get_hunting_task_detail(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("hunting:read"))
) -> Any:
    """
    获取狩猎任务详情

    包含任务基本信息、执行结果、执行日志等
    """
    try:
        # 查询任务详情
        result = db.query(HuntingTask, User.full_name.label('creator_name')).join(
            User, HuntingTask.created_by == User.id
        ).filter(HuntingTask.id == task_id).first()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="狩猎任务不存在"
            )

        task, creator_name = result

        # 模拟执行结果和日志
        results = []
        execution_log = []

        if task.status == 'completed':
            # 模拟搜索结果
            results = [
                {
                    "id": 1,
                    "timestamp": "2024-01-15T10:30:00Z",
                    "event_type": "process_creation",
                    "asset_name": "Honeypot-01",
                    "description": "可疑进程创建",
                    "confidence": 0.85
                },
                {
                    "id": 2,
                    "timestamp": "2024-01-15T11:15:00Z",
                    "event_type": "network_connection",
                    "asset_name": "Honeypot-02",
                    "description": "异常网络连接",
                    "confidence": 0.92
                }
            ]

            # 模拟执行日志
            execution_log = [
                {
                    "timestamp": task.created_at.isoformat(),
                    "level": "INFO",
                    "message": "任务开始执行"
                },
                {
                    "timestamp": (task.created_at + timedelta(seconds=30)).isoformat(),
                    "level": "INFO",
                    "message": "正在搜索Manticore索引..."
                },
                {
                    "timestamp": (task.completed_at or task.created_at).isoformat(),
                    "level": "INFO",
                    "message": f"搜索完成，找到 {len(results)} 条结果"
                }
            ]

        task_detail = HuntingTaskDetail(
            id=task.id,
            name=task.name,
            query_string=task.query_string,
            query_type=task.query_type,
            created_by=task.created_by,
            created_at=task.created_at,
            status=task.status,
            result_count=task.result_count,
            completed_at=task.completed_at,
            creator_name=creator_name,
            results=results,
            execution_log=execution_log
        )

        return task_detail

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取狩猎任务详情失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取狩猎任务详情失败"
        )

@router.post("/{task_id}/execute", response_model=MessageResponse, summary="执行狩猎任务")
def execute_hunting_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("hunting:execute"))
) -> Any:
    """
    执行威胁狩猎任务

    将任务状态更新为运行中，并启动后台执行
    """
    try:
        task = db.query(HuntingTask).filter(HuntingTask.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="狩猎任务不存在"
            )

        if task.status != 'pending':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="任务状态不允许执行"
            )

        # 更新任务状态
        task.status = 'running'
        db.commit()

        # TODO: 这里应该启动异步任务执行查询
        # 暂时模拟执行完成
        task.status = 'completed'
        task.result_count = 2  # 模拟结果数量
        task.completed_at = datetime.utcnow()
        db.commit()

        logger.info(f"用户 {current_user.username} 执行了狩猎任务: {task.name}")

        return MessageResponse(
            success=True,
            message="狩猎任务执行成功"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"执行狩猎任务失败: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="执行狩猎任务失败"
        )

@router.get("/templates", response_model=List[HuntingTemplate], summary="获取狩猎模板列表")
def get_hunting_templates(
    category: Optional[str] = Query(None, description="模板分类过滤"),
    difficulty: Optional[str] = Query(None, description="难度过滤"),
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("hunting:read"))
) -> Any:
    """
    获取威胁狩猎模板列表

    - **category**: 模板分类 (malware, lateral_movement, persistence, etc.)
    - **difficulty**: 难度级别 (easy, medium, hard)
    """
    try:
        # 模拟狩猎模板数据
        templates = [
            HuntingTemplate(
                id=1,
                name="可疑进程创建检测",
                description="检测系统中创建的可疑进程，包括PowerShell、CMD等",
                query_template="event_type:process_creation AND (process_name:powershell.exe OR process_name:cmd.exe)",
                category="malware",
                difficulty="easy",
                tags=["process", "powershell", "cmd"]
            ),
            HuntingTemplate(
                id=2,
                name="横向移动检测",
                description="检测网络中的横向移动行为，如SMB、RDP连接",
                query_template="event_type:network_connection AND (port:445 OR port:3389) AND NOT src_ip:internal_range",
                category="lateral_movement",
                difficulty="medium",
                tags=["network", "smb", "rdp", "lateral_movement"]
            ),
            HuntingTemplate(
                id=3,
                name="持久化机制检测",
                description="检测恶意软件的持久化机制，如注册表修改、计划任务等",
                query_template="event_type:registry_modification OR event_type:scheduled_task_creation",
                category="persistence",
                difficulty="medium",
                tags=["registry", "scheduled_task", "persistence"]
            ),
            HuntingTemplate(
                id=4,
                name="数据渗出检测",
                description="检测大量数据传输和异常网络流量",
                query_template="event_type:network_connection AND bytes_out:>10MB AND duration:>300s",
                category="exfiltration",
                difficulty="hard",
                tags=["network", "data_exfiltration", "traffic_analysis"]
            ),
            HuntingTemplate(
                id=5,
                name="暴力破解检测",
                description="检测针对SSH、RDP、Web应用的暴力破解攻击",
                query_template="event_type:authentication_failure AND count:>10 AND timespan:5m",
                category="credential_access",
                difficulty="easy",
                tags=["authentication", "brute_force", "ssh", "rdp"]
            )
        ]

        # 应用过滤条件
        filtered_templates = templates

        if category:
            filtered_templates = [t for t in filtered_templates if t.category == category]

        if difficulty:
            filtered_templates = [t for t in filtered_templates if t.difficulty == difficulty]

        return filtered_templates

    except Exception as e:
        logger.error(f"获取狩猎模板失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取狩猎模板失败"
        )

@router.get("/statistics", response_model=HuntingStatistics, summary="获取狩猎统计")
def get_hunting_statistics(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("hunting:read"))
) -> Any:
    """
    获取威胁狩猎统计数据

    包含任务总数、各状态数量、今日任务数、总结果数等
    """
    try:
        # 总任务数
        total_tasks = db.query(HuntingTask).count()

        # 按状态统计
        running_tasks = db.query(HuntingTask).filter(HuntingTask.status == 'running').count()
        completed_tasks = db.query(HuntingTask).filter(HuntingTask.status == 'completed').count()
        failed_tasks = db.query(HuntingTask).filter(HuntingTask.status == 'failed').count()

        # 今日任务数
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_tasks = db.query(HuntingTask).filter(HuntingTask.created_at >= today_start).count()

        # 总结果数
        total_results = db.query(HuntingTask).with_entities(
            db.func.sum(HuntingTask.result_count)
        ).scalar() or 0

        # 平均执行时间（模拟数据）
        avg_execution_time = 45.2  # 秒

        return HuntingStatistics(
            total_tasks=total_tasks,
            running_tasks=running_tasks,
            completed_tasks=completed_tasks,
            failed_tasks=failed_tasks,
            today_tasks=today_tasks,
            total_results=total_results,
            avg_execution_time=avg_execution_time
        )

    except Exception as e:
        logger.error(f"获取狩猎统计失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取狩猎统计失败"
        )

@router.delete("/{task_id}", response_model=MessageResponse, summary="删除狩猎任务")
def delete_hunting_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("hunting:delete"))
) -> Any:
    """
    删除威胁狩猎任务

    只能删除已完成或失败的任务
    """
    try:
        task = db.query(HuntingTask).filter(HuntingTask.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="狩猎任务不存在"
            )

        # 检查任务状态
        if task.status in ['pending', 'running']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无法删除正在执行的任务"
            )

        # 检查权限（只能删除自己创建的任务，除非是管理员）
        is_admin = any(role.name in ["admin", "administrator", "系统管理员"]
                      for role in current_user.roles)

        if not is_admin and task.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只能删除自己创建的任务"
            )

        task_name = task.name

        # 删除任务
        db.delete(task)
        db.commit()

        logger.info(f"用户 {current_user.username} 删除了狩猎任务: {task_name}")

        return MessageResponse(
            success=True,
            message="狩猎任务删除成功"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除狩猎任务失败: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除狩猎任务失败"
        )