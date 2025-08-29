#!/usr/bin/env python3
"""
数据库管理脚本
用于数据库迁移、初始化等操作
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.core.db import engine, Base
from app.db_init import init_db
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_command(command: list, cwd: str = None) -> bool:
    """运行命令"""
    try:
        result = subprocess.run(
            command,
            cwd=cwd or str(project_root),
            check=True,
            capture_output=True,
            text=True
        )
        logger.info(f"命令执行成功: {' '.join(command)}")
        if result.stdout:
            logger.info(f"输出: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"命令执行失败: {' '.join(command)}")
        logger.error(f"错误: {e.stderr}")
        return False

def init_alembic():
    """初始化Alembic"""
    logger.info("初始化Alembic...")
    
    # 检查是否已经初始化
    versions_dir = project_root / "migrations" / "versions"
    if versions_dir.exists():
        logger.info("Alembic已经初始化")
        return True
    
    # 创建versions目录
    versions_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成初始迁移
    return run_command(["alembic", "revision", "--autogenerate", "-m", "Initial migration"])

def create_migration(message: str):
    """创建新的迁移"""
    logger.info(f"创建迁移: {message}")
    return run_command(["alembic", "revision", "--autogenerate", "-m", message])

def upgrade_database(revision: str = "head"):
    """升级数据库"""
    logger.info(f"升级数据库到版本: {revision}")
    return run_command(["alembic", "upgrade", revision])

def downgrade_database(revision: str):
    """降级数据库"""
    logger.info(f"降级数据库到版本: {revision}")
    return run_command(["alembic", "downgrade", revision])

def show_current_revision():
    """显示当前数据库版本"""
    logger.info("显示当前数据库版本")
    return run_command(["alembic", "current"])

def show_migration_history():
    """显示迁移历史"""
    logger.info("显示迁移历史")
    return run_command(["alembic", "history"])

def create_tables():
    """直接创建所有表（开发环境使用）"""
    logger.info("创建数据库表...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")
        return True
    except Exception as e:
        logger.error(f"创建数据库表失败: {e}")
        return False

def drop_tables():
    """删除所有表（谨慎使用）"""
    logger.warning("删除所有数据库表...")
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("数据库表删除成功")
        return True
    except Exception as e:
        logger.error(f"删除数据库表失败: {e}")
        return False

def reset_database():
    """重置数据库（删除所有表并重新创建）"""
    logger.warning("重置数据库...")
    
    # 删除所有表
    if not drop_tables():
        return False
    
    # 重新创建表
    if not create_tables():
        return False
    
    # 初始化数据
    try:
        init_db()
        logger.info("数据库重置完成")
        return True
    except Exception as e:
        logger.error(f"初始化数据失败: {e}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="数据库管理工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 初始化Alembic
    subparsers.add_parser("init", help="初始化Alembic")
    
    # 创建迁移
    migrate_parser = subparsers.add_parser("migrate", help="创建新的迁移")
    migrate_parser.add_argument("message", help="迁移描述")
    
    # 升级数据库
    upgrade_parser = subparsers.add_parser("upgrade", help="升级数据库")
    upgrade_parser.add_argument("revision", nargs="?", default="head", help="目标版本")
    
    # 降级数据库
    downgrade_parser = subparsers.add_parser("downgrade", help="降级数据库")
    downgrade_parser.add_argument("revision", help="目标版本")
    
    # 显示当前版本
    subparsers.add_parser("current", help="显示当前数据库版本")
    
    # 显示历史
    subparsers.add_parser("history", help="显示迁移历史")
    
    # 创建表
    subparsers.add_parser("create-tables", help="直接创建所有表")
    
    # 删除表
    subparsers.add_parser("drop-tables", help="删除所有表")
    
    # 重置数据库
    subparsers.add_parser("reset", help="重置数据库")
    
    # 初始化数据
    subparsers.add_parser("init-data", help="初始化基础数据")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    success = True
    
    if args.command == "init":
        success = init_alembic()
    elif args.command == "migrate":
        success = create_migration(args.message)
    elif args.command == "upgrade":
        success = upgrade_database(args.revision)
    elif args.command == "downgrade":
        success = downgrade_database(args.revision)
    elif args.command == "current":
        success = show_current_revision()
    elif args.command == "history":
        success = show_migration_history()
    elif args.command == "create-tables":
        success = create_tables()
    elif args.command == "drop-tables":
        success = drop_tables()
    elif args.command == "reset":
        success = reset_database()
    elif args.command == "init-data":
        try:
            init_db()
            success = True
        except Exception as e:
            logger.error(f"初始化数据失败: {e}")
            success = False
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
