#!/usr/bin/env python3
"""
后端服务启动脚本
用于开发环境启动FastAPI服务器
"""

import os
import sys
import uvicorn
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """启动服务器"""
    # 设置环境变量
    os.environ.setdefault("PYTHONPATH", str(project_root))
    
    # 启动服务器
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式，文件变化时自动重载
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
