"""
认证相关的数据模式
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from .user import UserResponse
from .common import BaseResponse

# 登录请求模式
class LoginRequest(BaseModel):
    """登录请求数据模式"""
    username: str
    password: str

    @validator('username')
    def username_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('用户名不能为空')
        return v.strip()

    @validator('password')
    def password_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('密码不能为空')
        return v

# 登录响应数据
class LoginData(BaseModel):
    """登录响应数据"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

# 登录响应模式
class LoginResponse(BaseResponse[LoginData]):
    """登录响应模式"""
    pass

# 注册请求模式
class RegisterRequest(BaseModel):
    """注册请求数据模式"""
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

    @validator('username')
    def username_must_be_valid(cls, v):
        if len(v) < 3:
            raise ValueError('用户名长度不能少于3个字符')
        if len(v) > 50:
            raise ValueError('用户名长度不能超过50个字符')
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('用户名只能包含字母、数字、下划线和连字符')
        return v

    @validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('密码长度不能少于8个字符')
        if len(v) > 128:
            raise ValueError('密码长度不能超过128个字符')
        return v

# 刷新令牌请求模式
class RefreshTokenRequest(BaseModel):
    """刷新令牌请求数据模式"""
    refresh_token: str

# 刷新令牌响应数据
class RefreshTokenData(BaseModel):
    """刷新令牌响应数据"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

# 刷新令牌响应模式
class RefreshTokenResponse(BaseResponse[RefreshTokenData]):
    """刷新令牌响应模式"""
    pass

# 修改密码请求模式
class ChangePasswordRequest(BaseModel):
    """修改密码请求数据模式"""
    old_password: str
    new_password: str

    @validator('new_password')
    def new_password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('新密码长度不能少于8个字符')
        if len(v) > 128:
            raise ValueError('新密码长度不能超过128个字符')
        return v

# 重置密码请求模式
class ResetPasswordRequest(BaseModel):
    """重置密码请求数据模式"""
    email: EmailStr

# 重置密码确认模式
class ResetPasswordConfirmRequest(BaseModel):
    """重置密码确认请求数据模式"""
    token: str
    new_password: str

    @validator('new_password')
    def new_password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('新密码长度不能少于8个字符')
        if len(v) > 128:
            raise ValueError('新密码长度不能超过128个字符')
        return v

# 令牌验证响应模式
class TokenValidationResponse(BaseModel):
    """令牌验证响应模式"""
    valid: bool
    user_id: Optional[int] = None
    username: Optional[str] = None
    expires_at: Optional[datetime] = None

# 用户权限响应模式
class UserPermissionsResponse(BaseModel):
    """用户权限响应模式"""
    permissions: list[str]
    roles: list[str]
