from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.db import get_db
from app.core.dependencies import get_current_active_user, get_current_user_with_permission
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

# 报告相关数据模式
from pydantic import BaseModel

class ReportTemplate(BaseModel):
    """报告模板模式"""
    id: int
    name: str
    description: str
    template_type: str  # security_overview, incident_report, compliance_report
    content_template: str
    created_at: datetime
    created_by: str

class ReportRequest(BaseModel):
    """报告请求模式"""
    template_id: int
    name: str
    description: Optional[str] = None
    parameters: dict = {}
    schedule_type: str = 'once'  # once, daily, weekly, monthly
    recipients: List[str] = []

class ReportResponse(BaseModel):
    """报告响应模式"""
    id: int
    name: str
    description: Optional[str]
    template_id: int
    template_name: str
    status: str  # generating, completed, failed
    file_path: Optional[str]
    file_size: Optional[int]
    created_at: datetime
    completed_at: Optional[datetime]
    created_by: str

class ReportStatistics(BaseModel):
    """报告统计模式"""
    total_reports: int
    completed_reports: int
    failed_reports: int
    scheduled_reports: int
    total_size: int  # bytes
    popular_templates: List[dict]

@router.get("/templates", response_model=List[ReportTemplate], summary="获取报告模板列表")
def get_report_templates(
    template_type: Optional[str] = Query(None, description="模板类型过滤"),
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("report:read"))
) -> Any:
    """
    获取报告模板列表
    
    - **template_type**: 模板类型 (security_overview, incident_report, compliance_report)
    """
    try:
        # 模拟报告模板数据
        templates = [
            ReportTemplate(
                id=1,
                name="安全态势总览报告",
                description="包含告警统计、资产状态、威胁分析等内容的综合安全报告",
                template_type="security_overview",
                content_template="security_overview_template.html",
                created_at=datetime(2024, 1, 1),
                created_by="system"
            ),
            ReportTemplate(
                id=2,
                name="安全事件调查报告",
                description="针对特定安全事件的详细调查分析报告",
                template_type="incident_report",
                content_template="incident_report_template.html",
                created_at=datetime(2024, 1, 1),
                created_by="system"
            ),
            ReportTemplate(
                id=3,
                name="合规检查报告",
                description="系统合规性检查结果报告",
                template_type="compliance_report",
                content_template="compliance_report_template.html",
                created_at=datetime(2024, 1, 1),
                created_by="system"
            ),
            ReportTemplate(
                id=4,
                name="威胁狩猎报告",
                description="威胁狩猎活动和发现的详细报告",
                template_type="hunting_report",
                content_template="hunting_report_template.html",
                created_at=datetime(2024, 1, 1),
                created_by="system"
            ),
            ReportTemplate(
                id=5,
                name="资产清单报告",
                description="系统资产清单和状态报告",
                template_type="asset_report",
                content_template="asset_report_template.html",
                created_at=datetime(2024, 1, 1),
                created_by="system"
            )
        ]
        
        # 应用过滤条件
        if template_type:
            templates = [t for t in templates if t.template_type == template_type]
        
        return templates
        
    except Exception as e:
        logger.error(f"获取报告模板失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取报告模板失败"
        )

@router.post("/generate", response_model=IDResponse, summary="生成报告")
def generate_report(
    report_request: ReportRequest,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("report:create"))
) -> Any:
    """
    生成报告
    
    - **template_id**: 报告模板ID
    - **name**: 报告名称
    - **description**: 报告描述
    - **parameters**: 报告参数
    - **schedule_type**: 调度类型
    - **recipients**: 接收人邮箱列表
    """
    try:
        # 这里应该启动异步任务生成报告
        # 暂时模拟报告生成
        
        logger.info(f"用户 {current_user.username} 请求生成报告: {report_request.name}")
        
        # 模拟报告ID
        report_id = 1
        
        return IDResponse(
            id=report_id,
            message="报告生成任务已启动"
        )
        
    except Exception as e:
        logger.error(f"生成报告失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="生成报告失败"
        )

@router.get("/", response_model=PaginatedResponse[ReportResponse], summary="获取报告列表")
def get_reports(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="状态过滤"),
    template_id: Optional[int] = Query(None, description="模板ID过滤"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("report:read"))
) -> Any:
    """
    获取报告列表
    
    支持多种过滤条件：
    - **status**: 报告状态 (generating, completed, failed)
    - **template_id**: 模板ID
    - **search**: 搜索报告名称
    """
    try:
        # 模拟报告数据
        reports = [
            ReportResponse(
                id=1,
                name="2024年1月安全态势报告",
                description="2024年1月份的安全态势总览",
                template_id=1,
                template_name="安全态势总览报告",
                status="completed",
                file_path="/reports/security_overview_202401.pdf",
                file_size=2048576,  # 2MB
                created_at=datetime(2024, 1, 15, 10, 0),
                completed_at=datetime(2024, 1, 15, 10, 5),
                created_by=current_user.username
            ),
            ReportResponse(
                id=2,
                name="APT攻击事件调查报告",
                description="针对1月10日APT攻击事件的详细调查报告",
                template_id=2,
                template_name="安全事件调查报告",
                status="completed",
                file_path="/reports/incident_report_apt_20240110.pdf",
                file_size=5242880,  # 5MB
                created_at=datetime(2024, 1, 12, 14, 30),
                completed_at=datetime(2024, 1, 12, 15, 15),
                created_by=current_user.username
            ),
            ReportResponse(
                id=3,
                name="系统合规检查报告",
                description="系统合规性检查结果",
                template_id=3,
                template_name="合规检查报告",
                status="generating",
                file_path=None,
                file_size=None,
                created_at=datetime.utcnow(),
                completed_at=None,
                created_by=current_user.username
            )
        ]
        
        # 应用过滤条件
        filtered_reports = reports
        
        if status:
            filtered_reports = [r for r in filtered_reports if r.status == status]
        
        if template_id:
            filtered_reports = [r for r in filtered_reports if r.template_id == template_id]
        
        if search:
            filtered_reports = [r for r in filtered_reports if search.lower() in r.name.lower()]
        
        # 分页
        skip = (page - 1) * size
        paginated_reports = filtered_reports[skip:skip + size]
        
        return PaginatedResponse.create(
            items=paginated_reports,
            total=len(filtered_reports),
            page=page,
            size=size
        )
        
    except Exception as e:
        logger.error(f"获取报告列表失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取报告列表失败"
        )

@router.get("/statistics", response_model=ReportStatistics, summary="获取报告统计")
def get_report_statistics(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("report:read"))
) -> Any:
    """
    获取报告统计数据
    
    包含报告总数、完成数量、失败数量、热门模板等
    """
    try:
        # 模拟统计数据
        return ReportStatistics(
            total_reports=156,
            completed_reports=142,
            failed_reports=8,
            scheduled_reports=6,
            total_size=524288000,  # 500MB
            popular_templates=[
                {"template_id": 1, "template_name": "安全态势总览报告", "usage_count": 45},
                {"template_id": 2, "template_name": "安全事件调查报告", "usage_count": 32},
                {"template_id": 3, "template_name": "合规检查报告", "usage_count": 28}
            ]
        )
        
    except Exception as e:
        logger.error(f"获取报告统计失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取报告统计失败"
        )

@router.delete("/{report_id}", response_model=MessageResponse, summary="删除报告")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user_with_permission("report:delete"))
) -> Any:
    """
    删除报告
    
    删除报告记录和相关文件
    """
    try:
        # 这里应该删除数据库记录和文件
        # 暂时模拟删除操作
        
        logger.info(f"用户 {current_user.username} 删除了报告 ID: {report_id}")
        
        return MessageResponse(
            success=True,
            message="报告删除成功"
        )
        
    except Exception as e:
        logger.error(f"删除报告失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除报告失败"
        )
