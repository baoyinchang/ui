from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status
import logging
from app.core.config import settings

# 配置日志
logger = logging.getLogger(__name__)

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT算法
ALGORITHM = "HS256"

def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    创建JWT访问令牌

    Args:
        subject: 令牌主体（通常是用户ID或用户名）
        expires_delta: 过期时间增量，如果为None则使用默认配置

    Returns:
        str: JWT令牌字符串
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}

    try:
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=ALGORITHM
        )
        logger.info(f"为用户 {subject} 创建JWT令牌成功")
        return encoded_jwt
    except Exception as e:
        logger.error(f"创建JWT令牌失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="令牌创建失败"
        )

def verify_token(token: str) -> Optional[str]:
    """
    验证JWT令牌

    Args:
        token: JWT令牌字符串

    Returns:
        Optional[str]: 如果验证成功返回用户标识，否则返回None
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            logger.warning("JWT令牌中缺少用户标识")
            return None
        return username
    except JWTError as e:
        logger.warning(f"JWT令牌验证失败: {e}")
        return None
    except Exception as e:
        logger.error(f"令牌验证过程中发生错误: {e}")
        return None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码

    Args:
        plain_password: 明文密码
        hashed_password: 哈希密码

    Returns:
        bool: 密码是否匹配
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"密码验证失败: {e}")
        return False

def get_password_hash(password: str) -> str:
    """
    生成密码哈希

    Args:
        password: 明文密码

    Returns:
        str: 哈希后的密码
    """
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"密码哈希生成失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="密码处理失败"
        )

def create_refresh_token(subject: Union[str, Any]) -> str:
    """
    创建刷新令牌（有效期更长）

    Args:
        subject: 令牌主体

    Returns:
        str: 刷新令牌
    """
    expire = datetime.utcnow() + timedelta(days=7)  # 刷新令牌7天有效期
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}

    try:
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"创建刷新令牌失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="刷新令牌创建失败"
        )

def verify_refresh_token(token: str) -> Optional[str]:
    """
    验证刷新令牌

    Args:
        token: 刷新令牌

    Returns:
        Optional[str]: 如果验证成功返回用户标识，否则返回None
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        token_type: str = payload.get("type")

        if username is None or token_type != "refresh":
            logger.warning("刷新令牌格式无效")
            return None
        return username
    except JWTError as e:
        logger.warning(f"刷新令牌验证失败: {e}")
        return None
    except Exception as e:
        logger.error(f"刷新令牌验证过程中发生错误: {e}")
        return None

def generate_password_reset_token(email: str) -> str:
    """
    生成密码重置令牌

    Args:
        email: 用户邮箱

    Returns:
        str: 密码重置令牌
    """
    expire = datetime.utcnow() + timedelta(hours=1)  # 1小时有效期
    to_encode = {"exp": expire, "sub": email, "type": "password_reset"}

    try:
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"创建密码重置令牌失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="密码重置令牌创建失败"
        )

def verify_password_reset_token(token: str) -> Optional[str]:
    """
    验证密码重置令牌

    Args:
        token: 密码重置令牌

    Returns:
        Optional[str]: 如果验证成功返回邮箱，否则返回None
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        token_type: str = payload.get("type")

        if email is None or token_type != "password_reset":
            logger.warning("密码重置令牌格式无效")
            return None
        return email
    except JWTError as e:
        logger.warning(f"密码重置令牌验证失败: {e}")
        return None
    except Exception as e:
        logger.error(f"密码重置令牌验证过程中发生错误: {e}")
        return None