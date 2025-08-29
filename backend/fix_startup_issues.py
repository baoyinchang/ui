#!/usr/bin/env python3
"""
修复启动问题脚本
自动检测和修复常见的启动问题
"""

import os
import sys
from pathlib import Path

def create_missing_init_files():
    """创建缺失的__init__.py文件"""
    print("🔧 检查并创建__init__.py文件...")
    
    directories = [
        "app",
        "app/api",
        "app/api/v1", 
        "app/core",
        "app/crud",
        "app/models",
        "app/schemas",
        "app/services",
        "app/utils"
    ]
    
    for directory in directories:
        init_file = Path(directory) / "__init__.py"
        if not init_file.exists():
            init_file.write_text('"""Package initialization file"""\n')
            print(f"   ✅ 创建: {init_file}")
        else:
            print(f"   ✓ 存在: {init_file}")

def fix_requirements():
    """修复requirements.txt中的依赖问题"""
    print("\n🔧 检查requirements.txt...")
    
    required_packages = [
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "sqlalchemy>=2.0.23",
        "alembic>=1.12.1",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.6",
        "python-dateutil>=2.8.2",
        "email-validator>=2.1.0"
    ]
    
    # 检查SQLite支持
    try:
        import sqlite3
        print("   ✅ SQLite支持可用")
    except ImportError:
        print("   ❌ SQLite支持不可用")
    
    # 检查关键包
    missing_packages = []
    for package in required_packages:
        package_name = package.split(">=")[0].split("[")[0]
        try:
            __import__(package_name.replace("-", "_"))
            print(f"   ✅ {package_name}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package_name}")
    
    if missing_packages:
        print(f"\n⚠️  缺失的包: {missing_packages}")
        print("请运行: pip install " + " ".join(missing_packages))

def create_minimal_env():
    """创建最小化的.env文件"""
    print("\n🔧 检查.env文件...")
    
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# H-System EDR 配置文件
DATABASE_URL=sqlite:///./hsystem.db
SECRET_KEY=your-secret-key-change-in-production
DEBUG=true
LOG_LEVEL=INFO
ACCESS_TOKEN_EXPIRE_MINUTES=120
"""
        env_file.write_text(env_content)
        print("   ✅ 创建了.env文件")
    else:
        print("   ✓ .env文件已存在")

def fix_import_issues():
    """修复常见的导入问题"""
    print("\n🔧 修复导入问题...")
    
    # 检查core/dependencies.py是否存在
    deps_file = Path("app/core/dependencies.py")
    if not deps_file.exists():
        deps_content = '''"""
依赖注入模块
"""

from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.db import SessionLocal
from app.core.config import settings
from app.models.postgres import User

security = HTTPBearer()

def get_db() -> Generator[Session, None, None]:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.SECRET_KEY, 
            algorithms=["HS256"]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
'''
        deps_file.write_text(deps_content)
        print("   ✅ 创建了dependencies.py")
    else:
        print("   ✓ dependencies.py已存在")

def create_simple_main():
    """创建简化的main.py用于测试"""
    print("\n🔧 创建简化的main.py...")
    
    simple_main = Path("simple_main.py")
    content = '''"""
简化的FastAPI应用 - 用于测试
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="H-System EDR 蜜罐安全管理平台"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "H-System EDR API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    simple_main.write_text(content)
    print("   ✅ 创建了simple_main.py")

def main():
    """主函数"""
    print("🔧 H-System EDR 启动问题修复工具")
    print("=" * 50)
    
    # 切换到backend目录
    os.chdir(Path(__file__).parent)
    
    # 执行修复步骤
    create_missing_init_files()
    fix_requirements()
    create_minimal_env()
    fix_import_issues()
    create_simple_main()
    
    print("\n🎉 修复完成！")
    print("\n测试步骤:")
    print("1. 运行诊断: python test_startup.py")
    print("2. 测试简化版本: python -m uvicorn simple_main:app --reload")
    print("3. 运行完整版本: python -m uvicorn app.main:app --reload")

if __name__ == "__main__":
    main()
