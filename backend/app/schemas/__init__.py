# 导入所有数据模式
from .common import (
    MessageResponse,
    ErrorResponse,
    PaginationParams,
    PaginatedResponse,
    FilterParams,
    IDResponse,
    BulkOperationResponse,
    HealthCheckResponse,
    StatisticsResponse
)

from .user import (
    User,
    UserCreate,
    UserUpdate,
    UserPasswordUpdate,
    Role,
    Permission,
    UserDetail,
    LoginRequest,
    LoginResponse,
    TokenRefreshRequest,
    TokenRefreshResponse,
    PasswordResetRequest,
    PasswordResetConfirm,
    UserListResponse,
    CurrentUser
)

# 导出所有模式
__all__ = [
    # 通用模式
    "MessageResponse",
    "ErrorResponse",
    "PaginationParams",
    "PaginatedResponse",
    "FilterParams",
    "IDResponse",
    "BulkOperationResponse",
    "HealthCheckResponse",
    "StatisticsResponse",

    # 用户相关模式
    "User",
    "UserCreate",
    "UserUpdate",
    "UserPasswordUpdate",
    "Role",
    "Permission",
    "UserDetail",
    "LoginRequest",
    "LoginResponse",
    "TokenRefreshRequest",
    "TokenRefreshResponse",
    "PasswordResetRequest",
    "PasswordResetConfirm",
    "UserListResponse",
    "CurrentUser"
]