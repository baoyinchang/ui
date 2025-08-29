from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime

# 用户基础模式
class UserBase(BaseModel):
    """用户基础数据模式"""
    username: str
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: bool = True

    @validator('username')
    def username_must_be_valid(cls, v):
        """验证用户名格式"""
        if len(v) < 3:
            raise ValueError('用户名长度不能少于3个字符')
        if len(v) > 50:
            raise ValueError('用户名长度不能超过50个字符')
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('用户名只能包含字母、数字、下划线和连字符')
        return v

# 用户创建模式
class UserCreate(UserBase):
    """创建用户的数据模式"""
    password: str

    @validator('password')
    def password_must_be_strong(cls, v):
        """验证密码强度"""
        if len(v) < 8:
            raise ValueError('密码长度不能少于8个字符')
        if len(v) > 128:
            raise ValueError('密码长度不能超过128个字符')
        return v

# 用户更新模式
class UserUpdate(BaseModel):
    """更新用户的数据模式"""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

# 密码更新模式
class UserPasswordUpdate(BaseModel):
    """更新密码的数据模式"""
    current_password: str
    new_password: str

    @validator('new_password')
    def password_must_be_strong(cls, v):
        """验证新密码强度"""
        if len(v) < 8:
            raise ValueError('密码长度不能少于8个字符')
        if len(v) > 128:
            raise ValueError('密码长度不能超过128个字符')
        return v

# 角色模式
class RoleBase(BaseModel):
    """角色基础数据模式"""
    name: str
    description: Optional[str] = None

class Role(RoleBase):
    """角色数据模式"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# 权限模式
class PermissionBase(BaseModel):
    """权限基础数据模式"""
    name: str
    description: Optional[str] = None

class Permission(PermissionBase):
    """权限数据模式"""
    id: int

    class Config:
        from_attributes = True

# 用户响应模式
class User(UserBase):
    """用户响应数据模式"""
    id: int
    created_at: datetime
    updated_at: datetime
    roles: List[Role] = []

    class Config:
        from_attributes = True

# 用户详细信息模式
class UserDetail(User):
    """用户详细信息数据模式"""
    permissions: List[str] = []

# 登录请求模式
class LoginRequest(BaseModel):
    """登录请求数据模式"""
    username: str
    password: str

# 登录响应数据
class LoginData(BaseModel):
    """登录响应数据"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User

# 登录响应模式 - 使用统一格式
class LoginResponse(BaseModel):
    """登录响应数据模式 - 统一格式"""
    code: int = 200
    message: str = "登录成功"
    data: LoginData
    success: bool = True
    timestamp: datetime = None

    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now()
        super().__init__(**data)

# 令牌刷新请求模式
class TokenRefreshRequest(BaseModel):
    """令牌刷新请求数据模式"""
    refresh_token: str

# 令牌刷新响应模式
class TokenRefreshResponse(BaseModel):
    """令牌刷新响应数据模式"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int

# 密码重置请求模式
class PasswordResetRequest(BaseModel):
    """密码重置请求数据模式"""
    email: EmailStr

# 密码重置确认模式
class PasswordResetConfirm(BaseModel):
    """密码重置确认数据模式"""
    token: str
    new_password: str

    @validator('new_password')
    def password_must_be_strong(cls, v):
        """验证新密码强度"""
        if len(v) < 8:
            raise ValueError('密码长度不能少于8个字符')
        if len(v) > 128:
            raise ValueError('密码长度不能超过128个字符')
        return v

# 用户列表响应模式
class UserListResponse(BaseModel):
    """用户列表响应数据模式"""
    total: int
    items: List[User]
    page: int
    size: int
    pages: int

# 当前用户信息模式
class CurrentUser(UserDetail):
    """当前用户信息数据模式"""
    last_login: Optional[datetime] = None
