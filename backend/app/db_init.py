"""
数据库初始化脚本
用于创建初始用户、角色和权限数据
"""

from sqlalchemy.orm import Session
from app.core.db import SessionLocal, engine
from app.models.postgres import User, Role, Permission, user_roles, role_permissions
from app.crud.user_crud import user
from app.core.security import get_password_hash
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_initial_permissions(db: Session) -> dict:
    """创建初始权限"""
    permissions_data = [
        # 用户管理权限
        {"name": "user:read", "description": "查看用户信息"},
        {"name": "user:create", "description": "创建用户"},
        {"name": "user:update", "description": "更新用户信息"},
        {"name": "user:delete", "description": "删除用户"},
        
        # 资产管理权限
        {"name": "asset:read", "description": "查看资产信息"},
        {"name": "asset:create", "description": "创建资产"},
        {"name": "asset:update", "description": "更新资产信息"},
        {"name": "asset:delete", "description": "删除资产"},
        
        # 告警管理权限
        {"name": "alert:read", "description": "查看告警信息"},
        {"name": "alert:handle", "description": "处理告警"},
        {"name": "alert:create", "description": "创建告警规则"},
        {"name": "alert:delete", "description": "删除告警"},
        
        # 威胁狩猎权限
        {"name": "hunting:read", "description": "查看狩猎任务"},
        {"name": "hunting:create", "description": "创建狩猎任务"},
        {"name": "hunting:execute", "description": "执行狩猎任务"},
        {"name": "hunting:delete", "description": "删除狩猎任务"},
        
        # 威胁情报权限
        {"name": "intelligence:read", "description": "查看威胁情报"},
        {"name": "intelligence:create", "description": "创建威胁情报"},
        {"name": "intelligence:update", "description": "更新威胁情报"},
        {"name": "intelligence:delete", "description": "删除威胁情报"},
        
        # 系统管理权限
        {"name": "system:read", "description": "查看系统信息"},
        {"name": "system:config", "description": "系统配置"},
        {"name": "system:update", "description": "系统更新"},
        {"name": "system:backup", "description": "系统备份"},
        
        # 报告权限
        {"name": "report:read", "description": "查看报告"},
        {"name": "report:create", "description": "创建报告"},
        {"name": "report:export", "description": "导出报告"},
        
        # 调查权限
        {"name": "investigation:read", "description": "查看调查会话"},
        {"name": "investigation:create", "description": "创建调查会话"},
        {"name": "investigation:update", "description": "更新调查会话"},
        {"name": "investigation:delete", "description": "删除调查会话"},
    ]
    
    permissions = {}
    for perm_data in permissions_data:
        # 检查权限是否已存在
        existing_perm = db.query(Permission).filter(
            Permission.name == perm_data["name"]
        ).first()
        
        if not existing_perm:
            permission = Permission(**perm_data)
            db.add(permission)
            db.commit()
            db.refresh(permission)
            permissions[perm_data["name"]] = permission
            logger.info(f"创建权限: {perm_data['name']}")
        else:
            permissions[perm_data["name"]] = existing_perm
            logger.info(f"权限已存在: {perm_data['name']}")
    
    return permissions

def create_initial_roles(db: Session, permissions: dict) -> dict:
    """创建初始角色"""
    roles_data = [
        {
            "name": "系统管理员",
            "description": "系统管理员，拥有所有权限",
            "permissions": list(permissions.keys())  # 所有权限
        },
        {
            "name": "安全分析师",
            "description": "安全分析师，负责告警处理和威胁分析",
            "permissions": [
                "alert:read", "alert:handle",
                "asset:read",
                "hunting:read", "hunting:create", "hunting:execute",
                "intelligence:read",
                "investigation:read", "investigation:create", "investigation:update",
                "report:read", "report:create"
            ]
        },
        {
            "name": "安全运维",
            "description": "安全运维人员，负责系统维护和资产管理",
            "permissions": [
                "asset:read", "asset:create", "asset:update",
                "alert:read",
                "system:read", "system:config",
                "report:read"
            ]
        },
        {
            "name": "只读用户",
            "description": "只读用户，只能查看信息",
            "permissions": [
                "alert:read",
                "asset:read", 
                "hunting:read",
                "intelligence:read",
                "investigation:read",
                "report:read"
            ]
        }
    ]
    
    roles = {}
    for role_data in roles_data:
        # 检查角色是否已存在
        existing_role = db.query(Role).filter(
            Role.name == role_data["name"]
        ).first()
        
        if not existing_role:
            role = Role(
                name=role_data["name"],
                description=role_data["description"]
            )
            db.add(role)
            db.commit()
            db.refresh(role)
            
            # 分配权限
            for perm_name in role_data["permissions"]:
                if perm_name in permissions:
                    role.permissions.append(permissions[perm_name])
            
            db.commit()
            roles[role_data["name"]] = role
            logger.info(f"创建角色: {role_data['name']}")
        else:
            roles[role_data["name"]] = existing_role
            logger.info(f"角色已存在: {role_data['name']}")
    
    return roles

def create_initial_users(db: Session, roles: dict) -> None:
    """创建初始用户"""
    users_data = [
        {
            "username": "admin",
            "password": "admin123456",
            "full_name": "系统管理员",
            "email": "admin@hsystem.com",
            "is_active": True,
            "roles": ["系统管理员"]
        },
        {
            "username": "analyst",
            "password": "analyst123456", 
            "full_name": "安全分析师",
            "email": "analyst@hsystem.com",
            "is_active": True,
            "roles": ["安全分析师"]
        },
        {
            "username": "operator",
            "password": "operator123456",
            "full_name": "安全运维",
            "email": "operator@hsystem.com", 
            "is_active": True,
            "roles": ["安全运维"]
        }
    ]
    
    for user_data in users_data:
        # 检查用户是否已存在
        existing_user = user.get_by_username(db, username=user_data["username"])
        
        if not existing_user:
            # 创建用户
            new_user = user.create_user(
                db,
                username=user_data["username"],
                password=user_data["password"],
                full_name=user_data["full_name"],
                email=user_data["email"],
                is_active=user_data["is_active"]
            )
            
            # 分配角色
            for role_name in user_data["roles"]:
                if role_name in roles:
                    new_user.roles.append(roles[role_name])
            
            db.commit()
            logger.info(f"创建用户: {user_data['username']}")
        else:
            logger.info(f"用户已存在: {user_data['username']}")

def init_db() -> None:
    """初始化数据库"""
    try:
        db = SessionLocal()
        
        logger.info("开始初始化数据库...")
        
        # 创建权限
        logger.info("创建初始权限...")
        permissions = create_initial_permissions(db)
        
        # 创建角色
        logger.info("创建初始角色...")
        roles = create_initial_roles(db, permissions)
        
        # 创建用户
        logger.info("创建初始用户...")
        create_initial_users(db, roles)
        
        logger.info("数据库初始化完成!")
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
