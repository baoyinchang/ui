from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_active_user, get_admin_user
from app.crud.user_crud import user
from app.schemas.user import (
    User,
    UserCreate,
    UserUpdate,
    UserPasswordUpdate,
    UserListResponse,
    UserDetail
)
from app.schemas.common import (
    MessageResponse,
    PaginationParams,
    PaginatedResponse,
    IDResponse
)
import logging

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[User], summary="获取用户列表")
def get_users(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    search: str = Query(None, description="搜索关键词"),
    is_active: bool = Query(None, description="是否活跃"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
) -> Any:
    """
    获取用户列表（需要管理员权限）
    
    - **page**: 页码，从1开始
    - **size**: 每页数量，最大100
    - **search**: 搜索用户名或邮箱
    - **is_active**: 过滤活跃状态
    """
    try:
        skip = (page - 1) * size
        
        # 构建查询条件
        filters = {}
        if is_active is not None:
            filters['is_active'] = is_active
        
        # 获取用户列表
        users = user.get_multi(
            db,
            skip=skip,
            limit=size,
            order_by="created_at",
            order_desc=True
        )
        
        # 获取总数
        total = user.count(db, **filters)
        
        # 如果有搜索条件，需要进一步过滤
        if search:
            filtered_users = []
            for u in users:
                if (search.lower() in u.username.lower() or 
                    (u.email and search.lower() in u.email.lower()) or
                    (u.full_name and search.lower() in u.full_name.lower())):
                    filtered_users.append(u)
            users = filtered_users
        
        return PaginatedResponse.create(
            items=users,
            total=total,
            page=page,
            size=size
        )
        
    except Exception as e:
        logger.error(f"获取用户列表失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户列表失败"
        )

@router.post("/", response_model=User, summary="创建用户")
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
) -> Any:
    """
    创建新用户（需要管理员权限）
    
    - **username**: 用户名，3-50个字符
    - **password**: 密码，至少8个字符
    - **full_name**: 全名（可选）
    - **email**: 邮箱（可选）
    - **is_active**: 是否激活，默认true
    """
    try:
        # 检查用户名是否已存在
        if user.get_by_username(db, username=user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        if user_data.email and user.get_by_email(db, email=user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已存在"
            )
        
        # 创建用户
        new_user = user.create_user(
            db,
            username=user_data.username,
            password=user_data.password,
            full_name=user_data.full_name,
            email=user_data.email,
            is_active=user_data.is_active
        )
        
        logger.info(f"管理员 {current_user.username} 创建了用户 {new_user.username}")
        
        return new_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建用户失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建用户失败"
        )

@router.get("/{user_id}", response_model=UserDetail, summary="获取用户详情")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    获取用户详情
    
    普通用户只能查看自己的信息，管理员可以查看所有用户信息
    """
    try:
        # 获取目标用户
        target_user = user.get(db, id=user_id)
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 权限检查：只能查看自己的信息，除非是管理员
        is_admin = any(role.name in ["admin", "administrator", "系统管理员"] 
                      for role in current_user.roles)
        
        if not is_admin and target_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )
        
        # 获取用户权限列表
        permissions = []
        for role in target_user.roles:
            for permission in role.permissions:
                if permission.name not in permissions:
                    permissions.append(permission.name)
        
        # 构建详细信息
        user_detail = UserDetail(
            id=target_user.id,
            username=target_user.username,
            full_name=target_user.full_name,
            email=target_user.email,
            is_active=target_user.is_active,
            created_at=target_user.created_at,
            updated_at=target_user.updated_at,
            roles=target_user.roles,
            permissions=permissions
        )
        
        return user_detail
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取用户详情失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户详情失败"
        )

@router.put("/{user_id}", response_model=User, summary="更新用户信息")
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    更新用户信息
    
    普通用户只能更新自己的信息，管理员可以更新所有用户信息
    """
    try:
        # 获取目标用户
        target_user = user.get(db, id=user_id)
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 权限检查
        is_admin = any(role.name in ["admin", "administrator", "系统管理员"] 
                      for role in current_user.roles)
        
        if not is_admin and target_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )
        
        # 检查邮箱是否已被其他用户使用
        if user_data.email:
            existing_user = user.get_by_email(db, email=user_data.email)
            if existing_user and existing_user.id != target_user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱已被其他用户使用"
                )
        
        # 更新用户信息
        update_data = user_data.dict(exclude_unset=True)
        updated_user = user.update(db, db_obj=target_user, obj_in=update_data)
        
        logger.info(f"用户信息更新成功: {updated_user.username}")
        
        return updated_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新用户信息失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新用户信息失败"
        )

@router.put("/{user_id}/password", response_model=MessageResponse, summary="更新用户密码")
def update_user_password(
    user_id: int,
    password_data: UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    更新用户密码
    
    用户只能更新自己的密码，需要提供当前密码验证
    """
    try:
        # 获取目标用户
        target_user = user.get(db, id=user_id)
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 只能更新自己的密码
        if target_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只能更新自己的密码"
            )
        
        # 验证当前密码
        authenticated_user = user.authenticate(
            db,
            username=target_user.username,
            password=password_data.current_password
        )
        
        if not authenticated_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="当前密码错误"
            )
        
        # 更新密码
        user.update_password(db, user=target_user, new_password=password_data.new_password)
        
        logger.info(f"用户密码更新成功: {target_user.username}")
        
        return MessageResponse(
            success=True,
            message="密码更新成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新用户密码失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新用户密码失败"
        )

@router.delete("/{user_id}", response_model=MessageResponse, summary="删除用户")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
) -> Any:
    """
    删除用户（需要管理员权限）
    
    注意：不能删除自己的账户
    """
    try:
        # 获取目标用户
        target_user = user.get(db, id=user_id)
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 不能删除自己
        if target_user.id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="不能删除自己的账户"
            )
        
        # 删除用户
        user.remove(db, id=user_id)
        
        logger.info(f"管理员 {current_user.username} 删除了用户 {target_user.username}")
        
        return MessageResponse(
            success=True,
            message="用户删除成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除用户失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除用户失败"
        )
