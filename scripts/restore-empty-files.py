#!/usr/bin/env python3
"""
批量恢复空文件脚本
根据文件类型和路径，为空文件填充基础内容
"""

import os
from pathlib import Path
from typing import Dict, List

class FileRestorer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.restored_count = 0
        
    def get_file_template(self, file_path: Path) -> str:
        """根据文件路径和类型返回模板内容"""
        file_name = file_path.name
        relative_path = str(file_path.relative_to(self.project_root))
        
        # Python __init__.py 文件
        if file_name == "__init__.py":
            return '"""Package initialization file"""\n'
        
        # Vue组件文件
        if file_path.suffix == ".vue":
            component_name = file_path.stem.replace("-", "").replace("_", "").title()
            return f'''<template>
  <div class="{file_path.stem}-container">
    <h2>{component_name}</h2>
    <p>此页面正在开发中...</p>
  </div>
</template>

<script setup lang="ts">
import {{ ref, onMounted }} from 'vue'

// 组件逻辑
onMounted(() => {{
  console.log('{component_name} 组件已挂载')
}})
</script>

<style scoped>
.{file_path.stem}-container {{
  padding: 20px;
}}
</style>
'''
        
        # TypeScript文件
        if file_path.suffix == ".ts":
            if "api" in relative_path:
                return f'''/**
 * {file_path.stem} API接口
 */

import {{ http }} from '../request'

export const {file_path.stem}Api = {{
  // API方法将在此处定义
}}
'''
            elif "store" in relative_path or "modules" in relative_path:
                return f'''/**
 * {file_path.stem} 状态管理模块
 */

import {{ defineStore }} from 'pinia'

export const use{file_path.stem.title()}Store = defineStore('{file_path.stem}', () => {{
  // 状态和方法将在此处定义
  
  return {{
    // 导出的状态和方法
  }}
}})
'''
            else:
                return f'''/**
 * {file_path.stem} 模块
 */

// 模块内容将在此处定义
'''
        
        # SCSS样式文件
        if file_path.suffix == ".scss":
            return f'''/**
 * {file_path.stem} 样式文件
 */

// 样式定义将在此处添加
'''
        
        # Python服务文件
        if file_path.suffix == ".py" and "service" in relative_path:
            service_name = file_path.stem.replace("_service", "").title()
            return f'''"""
{service_name} 服务模块
提供{service_name}相关的业务逻辑处理
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.core.logger import get_logger

logger = get_logger(__name__)

class {service_name}Service:
    """
    {service_name}服务类
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_list(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        获取{service_name}列表
        """
        # 实现将在此处添加
        return []
    
    async def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """
        根据ID获取{service_name}
        """
        # 实现将在此处添加
        return None
    
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建{service_name}
        """
        # 实现将在此处添加
        return {{}}
    
    async def update(self, item_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        更新{service_name}
        """
        # 实现将在此处添加
        return None
    
    async def delete(self, item_id: int) -> bool:
        """
        删除{service_name}
        """
        # 实现将在此处添加
        return False

# 创建服务实例的工厂函数
def get_{file_path.stem}(db: Session) -> {service_name}Service:
    """获取{service_name}服务实例"""
    return {service_name}Service(db)
'''
        
        # Python CRUD文件
        if file_path.suffix == ".py" and "crud" in relative_path:
            model_name = file_path.stem.replace("_crud", "").title()
            return f'''"""
{model_name} CRUD操作模块
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.core.logger import get_logger

logger = get_logger(__name__)

class {model_name}CRUD:
    """
    {model_name} CRUD操作类
    """
    
    def get(self, db: Session, id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取记录"""
        # 实现将在此处添加
        return None
    
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """获取多条记录"""
        # 实现将在此处添加
        return []
    
    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> Dict[str, Any]:
        """创建记录"""
        # 实现将在此处添加
        return {{}}
    
    def update(self, db: Session, *, db_obj: Dict[str, Any], obj_in: Dict[str, Any]) -> Dict[str, Any]:
        """更新记录"""
        # 实现将在此处添加
        return {{}}
    
    def remove(self, db: Session, *, id: int) -> Dict[str, Any]:
        """删除记录"""
        # 实现将在此处添加
        return {{}}

# 创建CRUD实例
{file_path.stem} = {model_name}CRUD()
'''
        
        # Python测试文件
        if file_path.suffix == ".py" and "test" in relative_path:
            test_name = file_path.stem.replace("test_", "")
            return f'''"""
{test_name} 模块测试
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class Test{test_name.title()}:
    """
    {test_name} 测试类
    """
    
    def test_{test_name}_example(self):
        """
        示例测试方法
        """
        # 测试实现将在此处添加
        assert True
    
    @pytest.mark.asyncio
    async def test_{test_name}_async_example(self):
        """
        异步测试示例
        """
        # 异步测试实现将在此处添加
        assert True
'''
        
        # Docker文件
        if file_name == "Dockerfile":
            if "frontend" in relative_path:
                return '''# 前端Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
'''
            else:
                return '''# 后端Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
        
        # Docker Compose文件
        if file_name == "docker-compose.yml":
            return '''version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./hsystem.db
    volumes:
      - ./data:/app/data
    
  frontend:
    build: ../frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  data:
'''
        
        # 环境变量文件
        if file_name == ".env":
            return '''# 环境变量配置
DATABASE_URL=sqlite:///./hsystem.db
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=120

# 开发环境配置
DEBUG=true
LOG_LEVEL=INFO
'''
        
        # 配置文件
        if file_name in [".eslintrc.js", ".prettierrc.js"]:
            return f'// {file_name} 配置文件\n// 配置内容将在此处添加\n'
        
        # 默认模板
        return f'// {file_name}\n// 文件内容将在此处添加\n'
    
    def restore_file(self, file_path: Path) -> bool:
        """恢复单个文件"""
        try:
            if file_path.stat().st_size == 0:  # 只处理空文件
                template = self.get_file_template(file_path)
                file_path.write_text(template, encoding='utf-8')
                self.restored_count += 1
                print(f"✅ 已恢复: {file_path.relative_to(self.project_root)}")
                return True
        except Exception as e:
            print(f"❌ 恢复失败: {file_path.relative_to(self.project_root)} - {e}")
            return False
        return False
    
    def restore_all_empty_files(self):
        """恢复所有空文件"""
        print("🔧 开始批量恢复空文件...")
        
        # 遍历前端目录
        frontend_dir = self.project_root / "frontend"
        if frontend_dir.exists():
            for file_path in frontend_dir.rglob("*"):
                if file_path.is_file():
                    self.restore_file(file_path)
        
        # 遍历后端目录
        backend_dir = self.project_root / "backend"
        if backend_dir.exists():
            for file_path in backend_dir.rglob("*"):
                if file_path.is_file():
                    self.restore_file(file_path)
        
        print(f"\n🎉 恢复完成! 共恢复了 {self.restored_count} 个文件")

def main():
    """主函数"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    restorer = FileRestorer(project_root)
    restorer.restore_all_empty_files()

if __name__ == "__main__":
    main()
