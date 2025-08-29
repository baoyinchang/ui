from typing import Optional, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.postgres import User, Role
from app.core.security import get_password_hash, verify_password
import logging

# 配置日志
logger = logging.getLogger(__name__)

class CRUDUser(CRUDBase[User, dict, dict]):
    """用户CRUD操作类"""

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """
        根据用户名获取用户

        Args:
            db: 数据库会话
            username: 用户名

        Returns:
            Optional[User]: 用户对象或None
        """
        try:
            return db.query(User).filter(User.username == username).first()
        except Exception as e:
            logger.error(f"根据用户名获取用户失败 ({username}): {e}")
            return None

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        根据邮箱获取用户

        Args:
            db: 数据库会话
            email: 邮箱地址

        Returns:
            Optional[User]: 用户对象或None
        """
        try:
            return db.query(User).filter(User.email == email).first()
        except Exception as e:
            logger.error(f"根据邮箱获取用户失败 ({email}): {e}")
            return None

    def create_user(
        self,
        db: Session,
        *,
        username: str,
        password: str,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        is_active: bool = True
    ) -> User:
        """
        创建新用户

        Args:
            db: 数据库会话
            username: 用户名
            password: 明文密码
            full_name: 全名
            email: 邮箱
            is_active: 是否激活

        Returns:
            User: 创建的用户对象
        """
        try:
            # 检查用户名是否已存在
            if self.get_by_username(db, username=username):
                raise ValueError(f"用户名 {username} 已存在")

            # 检查邮箱是否已存在
            if email and self.get_by_email(db, email=email):
                raise ValueError(f"邮箱 {email} 已存在")

            # 创建用户
            hashed_password = get_password_hash(password)
            db_user = User(
                username=username,
                password_hash=hashed_password,
                full_name=full_name,
                email=email,
                is_active=is_active
            )

            db.add(db_user)
            db.commit()
            db.refresh(db_user)

            logger.info(f"创建用户成功: {username}")
            return db_user

        except Exception as e:
            logger.error(f"创建用户失败 ({username}): {e}")
            db.rollback()
            raise

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        """
        用户认证

        Args:
            db: 数据库会话
            username: 用户名
            password: 明文密码

        Returns:
            Optional[User]: 认证成功返回用户对象，否则返回None
        """
        try:
            user = self.get_by_username(db, username=username)
            if not user:
                logger.warning(f"用户不存在: {username}")
                return None

            if not verify_password(password, user.password_hash):
                logger.warning(f"用户密码错误: {username}")
                return None

            if not user.is_active:
                logger.warning(f"用户已被禁用: {username}")
                return None

            logger.info(f"用户认证成功: {username}")
            return user

        except Exception as e:
            logger.error(f"用户认证失败 ({username}): {e}")
            return None

    def update_password(self, db: Session, *, user: User, new_password: str) -> User:
        """
        更新用户密码

        Args:
            db: 数据库会话
            user: 用户对象
            new_password: 新密码

        Returns:
            User: 更新后的用户对象
        """
        try:
            hashed_password = get_password_hash(new_password)
            user.password_hash = hashed_password

            db.add(user)
            db.commit()
            db.refresh(user)

            logger.info(f"更新用户密码成功: {user.username}")
            return user

        except Exception as e:
            logger.error(f"更新用户密码失败 ({user.username}): {e}")
            db.rollback()
            raise

    def activate_user(self, db: Session, *, user: User) -> User:
        """
        激活用户

        Args:
            db: 数据库会话
            user: 用户对象

        Returns:
            User: 更新后的用户对象
        """
        try:
            user.is_active = True
            db.add(user)
            db.commit()
            db.refresh(user)

            logger.info(f"激活用户成功: {user.username}")
            return user

        except Exception as e:
            logger.error(f"激活用户失败 ({user.username}): {e}")
            db.rollback()
            raise

    def deactivate_user(self, db: Session, *, user: User) -> User:
        """
        禁用用户

        Args:
            db: 数据库会话
            user: 用户对象

        Returns:
            User: 更新后的用户对象
        """
        try:
            user.is_active = False
            db.add(user)
            db.commit()
            db.refresh(user)

            logger.info(f"禁用用户成功: {user.username}")
            return user

        except Exception as e:
            logger.error(f"禁用用户失败 ({user.username}): {e}")
            db.rollback()
            raise

    def assign_role(self, db: Session, *, user: User, role: Role) -> User:
        """
        为用户分配角色

        Args:
            db: 数据库会话
            user: 用户对象
            role: 角色对象

        Returns:
            User: 更新后的用户对象
        """
        try:
            if role not in user.roles:
                user.roles.append(role)
                db.add(user)
                db.commit()
                db.refresh(user)
                logger.info(f"为用户 {user.username} 分配角色 {role.name} 成功")
            else:
                logger.info(f"用户 {user.username} 已拥有角色 {role.name}")

            return user

        except Exception as e:
            logger.error(f"为用户分配角色失败 ({user.username}, {role.name}): {e}")
            db.rollback()
            raise

    def remove_role(self, db: Session, *, user: User, role: Role) -> User:
        """
        移除用户角色

        Args:
            db: 数据库会话
            user: 用户对象
            role: 角色对象

        Returns:
            User: 更新后的用户对象
        """
        try:
            if role in user.roles:
                user.roles.remove(role)
                db.add(user)
                db.commit()
                db.refresh(user)
                logger.info(f"移除用户 {user.username} 的角色 {role.name} 成功")
            else:
                logger.info(f"用户 {user.username} 没有角色 {role.name}")

            return user

        except Exception as e:
            logger.error(f"移除用户角色失败 ({user.username}, {role.name}): {e}")
            db.rollback()
            raise

    def get_active_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        获取活跃用户列表

        Args:
            db: 数据库会话
            skip: 跳过记录数
            limit: 限制记录数

        Returns:
            List[User]: 活跃用户列表
        """
        try:
            return (db.query(User)
                   .filter(User.is_active == True)
                   .offset(skip)
                   .limit(limit)
                   .all())
        except Exception as e:
            logger.error(f"获取活跃用户列表失败: {e}")
            return []

# 创建用户CRUD实例
user = CRUDUser(User)

# 便捷函数
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """根据用户名获取用户的便捷函数"""
    return user.get_by_username(db, username=username)

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """用户认证的便捷函数"""
    return user.authenticate(db, username=username, password=password)