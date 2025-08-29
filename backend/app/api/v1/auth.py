from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    generate_password_reset_token,
    verify_password_reset_token
)
from app.core.dependencies import get_current_active_user
from app.crud.user_crud import user, authenticate_user, get_user_by_username
from app.schemas.user import (
    LoginRequest,
    LoginResponse,
    TokenRefreshRequest,
    TokenRefreshResponse,
    PasswordResetRequest,
    PasswordResetConfirm,
    User,
    CurrentUser
)
from app.schemas.common import MessageResponse, BaseResponse
import logging

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/login", response_model=LoginResponse, summary="用户登录")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
) -> Any:
    """
    用户登录接口
    
    - **username**: 用户名
    - **password**: 密码
    
    返回访问令牌和用户信息
    """
    try:
        # 验证用户凭据
        authenticated_user = authenticate_user(
            db, 
            username=login_data.username, 
            password=login_data.password
        )
        
        if not authenticated_user:
            logger.warning(f"登录失败: {login_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 创建访问令牌和刷新令牌
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=authenticated_user.username,
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(subject=authenticated_user.username)
        
        logger.info(f"用户登录成功: {authenticated_user.username}")
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=authenticated_user
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"登录过程中发生错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登录服务暂时不可用"
        )

@router.post("/login/oauth", response_model=LoginResponse, summary="OAuth2密码登录")
def login_oauth(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    OAuth2标准密码登录接口
    兼容标准OAuth2客户端
    """
    try:
        authenticated_user = authenticate_user(
            db, 
            username=form_data.username, 
            password=form_data.password
        )
        
        if not authenticated_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=authenticated_user.username,
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(subject=authenticated_user.username)
        
        # 构造登录数据
        from app.schemas.user import LoginData
        login_data = LoginData(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=authenticated_user
        )

        return LoginResponse(
            code=200,
            message="登录成功",
            data=login_data,
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OAuth2登录过程中发生错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登录服务暂时不可用"
        )

@router.post("/refresh", response_model=TokenRefreshResponse, summary="刷新访问令牌")
def refresh_token(
    refresh_data: TokenRefreshRequest,
    db: Session = Depends(get_db)
) -> Any:
    """
    刷新访问令牌接口
    
    - **refresh_token**: 刷新令牌
    
    返回新的访问令牌
    """
    try:
        # 验证刷新令牌
        username = verify_refresh_token(refresh_data.refresh_token)
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="刷新令牌无效或已过期"
            )
        
        # 检查用户是否仍然存在且活跃
        current_user = get_user_by_username(db, username=username)
        if not current_user or not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在或已被禁用"
            )
        
        # 创建新的访问令牌
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=username,
            expires_delta=access_token_expires
        )
        
        logger.info(f"令牌刷新成功: {username}")
        
        return TokenRefreshResponse(
            access_token=access_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"令牌刷新过程中发生错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="令牌刷新服务暂时不可用"
        )

@router.post("/logout", response_model=MessageResponse, summary="用户登出")
def logout(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    用户登出接口
    
    注意：由于JWT是无状态的，实际的令牌失效需要在客户端处理
    这个接口主要用于记录登出日志和清理服务端会话（如果有的话）
    """
    try:
        logger.info(f"用户登出: {current_user.username}")
        
        return MessageResponse(
            success=True,
            message="登出成功"
        )
        
    except Exception as e:
        logger.error(f"登出过程中发生错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登出服务暂时不可用"
        )

@router.get("/me", response_model=CurrentUser, summary="获取当前用户信息")
def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    获取当前登录用户的详细信息
    
    返回用户基本信息、角色和权限列表
    """
    try:
        # 获取用户权限列表
        permissions = []
        for role in current_user.roles:
            for permission in role.permissions:
                if permission.name not in permissions:
                    permissions.append(permission.name)
        
        # 构建响应数据
        user_info = CurrentUser(
            id=current_user.id,
            username=current_user.username,
            full_name=current_user.full_name,
            email=current_user.email,
            is_active=current_user.is_active,
            created_at=current_user.created_at,
            updated_at=current_user.updated_at,
            roles=current_user.roles,
            permissions=permissions
        )
        
        return user_info
        
    except Exception as e:
        logger.error(f"获取用户信息失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户信息失败"
        )

@router.post("/password-reset", response_model=MessageResponse, summary="请求密码重置")
def request_password_reset(
    reset_data: PasswordResetRequest,
    db: Session = Depends(get_db)
) -> Any:
    """
    请求密码重置接口
    
    - **email**: 用户邮箱
    
    发送密码重置邮件（实际实现中需要集成邮件服务）
    """
    try:
        # 检查邮箱是否存在
        existing_user = user.get_by_email(db, email=reset_data.email)
        if not existing_user:
            # 为了安全考虑，即使邮箱不存在也返回成功消息
            logger.warning(f"密码重置请求的邮箱不存在: {reset_data.email}")
        else:
            # 生成密码重置令牌
            reset_token = generate_password_reset_token(reset_data.email)
            
            # TODO: 在实际实现中，这里应该发送包含重置链接的邮件
            # send_password_reset_email(reset_data.email, reset_token)
            
            logger.info(f"密码重置令牌已生成: {reset_data.email}")
        
        return MessageResponse(
            success=True,
            message="如果该邮箱存在，密码重置链接已发送到您的邮箱"
        )
        
    except Exception as e:
        logger.error(f"密码重置请求失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="密码重置服务暂时不可用"
        )

@router.post("/password-reset/confirm", response_model=MessageResponse, summary="确认密码重置")
def confirm_password_reset(
    confirm_data: PasswordResetConfirm,
    db: Session = Depends(get_db)
) -> Any:
    """
    确认密码重置接口
    
    - **token**: 密码重置令牌
    - **new_password**: 新密码
    """
    try:
        # 验证重置令牌
        email = verify_password_reset_token(confirm_data.token)
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="密码重置令牌无效或已过期"
            )
        
        # 获取用户
        existing_user = user.get_by_email(db, email=email)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 更新密码
        user.update_password(db, user=existing_user, new_password=confirm_data.new_password)
        
        logger.info(f"密码重置成功: {email}")
        
        return MessageResponse(
            success=True,
            message="密码重置成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"密码重置确认失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="密码重置服务暂时不可用"
        )
