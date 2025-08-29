from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import verify_token
from app.models.postgres import User
from app.crud.user_crud import get_user_by_username
import logging

# 配置日志
logger = logging.getLogger(__name__)

# HTTP Bearer 认证方案
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前认证用户的依赖项

    Args:
        credentials: HTTP Bearer 认证凭据
        db: 数据库会话

    Returns:
        User: 当前用户对象

    Raises:
        HTTPException: 认证失败时抛出401错误
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 验证JWT令牌
        username = verify_token(credentials.credentials)
        if username is None:
            logger.warning("JWT令牌验证失败")
            raise credentials_exception
    except Exception as e:
        logger.error(f"令牌验证过程中发生错误: {e}")
        raise credentials_exception

    # 从数据库获取用户信息
    user = get_user_by_username(db, username=username)
    if user is None:
        logger.warning(f"用户 {username} 不存在")
        raise credentials_exception

    if not user.is_active:
        logger.warning(f"用户 {username} 已被禁用")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户账户已被禁用"
        )

    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前活跃用户的依赖项

    Args:
        current_user: 当前用户

    Returns:
        User: 活跃用户对象

    Raises:
        HTTPException: 用户不活跃时抛出403错误
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户账户已被禁用"
        )
    return current_user

def get_current_user_with_permission(permission: str):
    """
    创建需要特定权限的用户依赖项

    Args:
        permission: 所需权限名称

    Returns:
        function: 依赖项函数
    """
    def _get_current_user_with_permission(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        """
        检查用户是否具有指定权限

        Args:
            current_user: 当前用户

        Returns:
            User: 具有权限的用户对象

        Raises:
            HTTPException: 权限不足时抛出403错误
        """
        # 检查用户是否具有所需权限
        user_permissions = []
        for role in current_user.roles:
            for perm in role.permissions:
                user_permissions.append(perm.name)

        if permission not in user_permissions:
            logger.warning(f"用户 {current_user.username} 缺少权限: {permission}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"权限不足，需要权限: {permission}"
            )

        return current_user

    return _get_current_user_with_permission

def get_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    获取管理员用户的依赖项

    Args:
        current_user: 当前用户

    Returns:
        User: 管理员用户对象

    Raises:
        HTTPException: 非管理员时抛出403错误
    """
    # 检查用户是否具有管理员角色
    admin_roles = ["admin", "administrator", "系统管理员"]
    user_roles = [role.name for role in current_user.roles]

    if not any(role in admin_roles for role in user_roles):
        logger.warning(f"用户 {current_user.username} 尝试访问管理员功能")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )

    return current_user

def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    获取可选的当前用户（用于可选认证的接口）

    Args:
        credentials: HTTP Bearer 认证凭据（可选）
        db: 数据库会话

    Returns:
        Optional[User]: 用户对象或None
    """
    if credentials is None:
        return None

    try:
        username = verify_token(credentials.credentials)
        if username is None:
            return None

        user = get_user_by_username(db, username=username)
        if user is None or not user.is_active:
            return None

        return user
    except Exception as e:
        logger.warning(f"可选认证失败: {e}")
        return None