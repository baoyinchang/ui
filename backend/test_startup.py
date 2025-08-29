#!/usr/bin/env python3
"""
简化的启动测试脚本
用于诊断启动问题
"""

import sys
import os
import traceback

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试各个模块的导入"""
    print("🔍 测试模块导入...")
    
    try:
        print("1. 测试基础配置...")
        from app.core.config import settings
        print(f"   ✅ 配置加载成功: {settings.PROJECT_NAME}")
        print(f"   📊 数据库URL: {settings.database_url}")
        print(f"   🐛 调试模式: {settings.DEBUG}")
    except Exception as e:
        print(f"   ❌ 配置加载失败: {e}")
        traceback.print_exc()
        return False
    
    try:
        print("2. 测试数据库连接...")
        from app.core.db import engine, Base
        print("   ✅ 数据库引擎创建成功")
        
        # 测试连接
        with engine.connect() as conn:
            print("   ✅ 数据库连接测试成功")
    except Exception as e:
        print(f"   ❌ 数据库连接失败: {e}")
        traceback.print_exc()
        return False
    
    try:
        print("3. 测试模型导入...")
        from app.models.postgres import User, Alert, Asset
        print("   ✅ 模型导入成功")
    except Exception as e:
        print(f"   ❌ 模型导入失败: {e}")
        traceback.print_exc()
        return False
    
    try:
        print("4. 测试路由导入...")
        from app.api.v1.auth import router as auth_router
        print("   ✅ 认证路由导入成功")
        
        from app.api.v1.dashboard import router as dashboard_router
        print("   ✅ 仪表板路由导入成功")
    except Exception as e:
        print(f"   ❌ 路由导入失败: {e}")
        traceback.print_exc()
        return False
    
    try:
        print("5. 测试FastAPI应用...")
        from app.main import app
        print("   ✅ FastAPI应用创建成功")
    except Exception as e:
        print(f"   ❌ FastAPI应用创建失败: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_database_tables():
    """测试数据库表创建"""
    print("\n🗄️ 测试数据库表...")
    
    try:
        from app.core.db import engine, Base
        from app.models.postgres import User, Alert, Asset
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("   ✅ 数据库表创建成功")
        
        # 检查表是否存在
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"   📋 已创建的表: {tables}")
        
        return True
    except Exception as e:
        print(f"   ❌ 数据库表创建失败: {e}")
        traceback.print_exc()
        return False

def test_basic_crud():
    """测试基本的CRUD操作"""
    print("\n🔧 测试基本CRUD操作...")
    
    try:
        from app.core.db import SessionLocal
        from app.models.postgres import User
        from passlib.context import CryptContext
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        db = SessionLocal()
        
        # 检查是否已有用户
        existing_user = db.query(User).filter(User.username == "admin").first()
        if existing_user:
            print("   ✅ 测试用户已存在")
        else:
            # 创建测试用户
            test_user = User(
                username="admin",
                password_hash=pwd_context.hash("admin123"),
                email="admin@hsystem.com",
                full_name="系统管理员",
                is_active=True,
                is_superuser=True
            )
            db.add(test_user)
            db.commit()
            print("   ✅ 测试用户创建成功")
        
        db.close()
        return True
    except Exception as e:
        print(f"   ❌ CRUD操作失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🚀 H-System EDR 后端启动诊断")
    print("=" * 50)
    
    # 测试导入
    if not test_imports():
        print("\n❌ 模块导入测试失败，请检查依赖和配置")
        return 1
    
    # 测试数据库
    if not test_database_tables():
        print("\n❌ 数据库表创建失败，请检查数据库配置")
        return 1
    
    # 测试CRUD
    if not test_basic_crud():
        print("\n❌ CRUD操作失败，请检查数据库权限")
        return 1
    
    print("\n🎉 所有测试通过！可以尝试启动服务器")
    print("\n启动命令:")
    print("python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    
    return 0

if __name__ == "__main__":
    exit(main())
