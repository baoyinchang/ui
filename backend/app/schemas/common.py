from typing import Any, Optional, List, Generic, TypeVar
from pydantic import BaseModel
from datetime import datetime

# 泛型类型变量
DataType = TypeVar('DataType')

class BaseResponse(BaseModel, Generic[DataType]):
    """统一响应格式"""
    code: int = 200
    message: str = "success"
    data: Optional[DataType] = None
    success: bool = True
    timestamp: datetime = None

    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now()
        super().__init__(**data)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class MessageResponse(BaseModel):
    """通用消息响应模式"""
    success: bool
    message: str
    code: Optional[str] = None

class ErrorResponse(BaseModel):
    """错误响应模式"""
    success: bool = False
    error: str
    code: Optional[str] = None
    details: Optional[Any] = None

class PaginationParams(BaseModel):
    """分页参数模式"""
    page: int = 1
    size: int = 20

    def get_offset(self) -> int:
        """获取偏移量"""
        return (self.page - 1) * self.size

class PaginatedResponse(BaseModel, Generic[DataType]):
    """分页响应模式"""
    total: int
    items: List[DataType]
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool

    @classmethod
    def create(
        cls,
        items: List[DataType],
        total: int,
        page: int,
        size: int
    ) -> "PaginatedResponse[DataType]":
        """创建分页响应"""
        pages = (total + size - 1) // size  # 向上取整
        return cls(
            total=total,
            items=items,
            page=page,
            size=size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1
        )

class FilterParams(BaseModel):
    """通用过滤参数模式"""
    search: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    order_by: Optional[str] = None
    order_desc: bool = False

class IDResponse(BaseModel):
    """ID响应模式"""
    id: int
    success: bool = True
    message: Optional[str] = None

class BulkOperationResponse(BaseModel):
    """批量操作响应模式"""
    success_count: int
    failed_count: int
    total_count: int
    success: bool
    message: str
    failed_items: Optional[List[Any]] = None

class HealthCheckResponse(BaseModel):
    """健康检查响应模式"""
    status: str
    timestamp: datetime
    version: str
    database: str
    services: dict

class StatisticsResponse(BaseModel):
    """统计数据响应模式"""
    total: int
    active: int
    inactive: int
    today: int
    this_week: int
    this_month: int
    growth_rate: Optional[float] = None