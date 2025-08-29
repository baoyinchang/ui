#!/usr/bin/env python3
"""
检查空文件和空目录脚本
分析前后端项目中的空文件和空目录，判断是否正常
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple

class EmptyFileChecker:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.frontend_dir = self.project_root / "frontend"
        self.backend_dir = self.project_root / "backend"
        
        # 应该为空的文件（正常情况）
        self.expected_empty_files = {
            # Python __init__.py 文件通常为空
            "backend/app/__init__.py",
            "backend/tests/__init__.py",
            "backend/app/api/__init__.py",
            "backend/app/core/__init__.py",
            "backend/app/crud/__init__.py",
            "backend/app/models/__init__.py",
            "backend/app/schemas/__init__.py",
            "backend/app/services/__init__.py",
            "backend/app/tasks/__init__.py",
            "backend/app/utils/__init__.py",
            
            # 前端可能为空的文件
            "frontend/.gitkeep",
            "frontend/src/assets/.gitkeep",
            "frontend/src/assets/css/.gitkeep",
            "frontend/src/assets/images/.gitkeep",
            "frontend/src/composables/.gitkeep",
            "frontend/src/hooks/.gitkeep",
        }
        
        # 应该为空的目录（正常情况）
        self.expected_empty_dirs = {
            # 前端资源目录（开发阶段可能为空）
            "frontend/src/assets/css",
            "frontend/src/assets/images", 
            "frontend/src/assets/icons",
            "frontend/src/composables",
            "frontend/src/hooks",
            
            # 后端可能为空的目录
            "backend/logs",
            "backend/uploads",
            "backend/temp",
        }
        
        # 应该有内容的重要文件
        self.important_files = {
            # 前端重要文件
            "frontend/package.json": "包配置文件",
            "frontend/vite.config.ts": "Vite配置文件", 
            "frontend/tsconfig.json": "TypeScript配置",
            "frontend/src/main.ts": "应用入口文件",
            "frontend/src/App.vue": "根组件",
            "frontend/src/router/index.ts": "路由配置",
            "frontend/src/store/index.ts": "状态管理",
            
            # 后端重要文件
            "backend/requirements.txt": "Python依赖",
            "backend/app/main.py": "FastAPI应用入口",
            "backend/app/core/config.py": "配置文件",
            "backend/app/core/db.py": "数据库配置",
            "backend/app/api/v1/router.py": "API路由",
        }

    def check_file_size(self, file_path: Path) -> int:
        """检查文件大小"""
        try:
            return file_path.stat().st_size
        except (OSError, FileNotFoundError):
            return -1

    def is_directory_empty(self, dir_path: Path) -> bool:
        """检查目录是否为空"""
        try:
            return not any(dir_path.iterdir())
        except (OSError, FileNotFoundError):
            return True

    def find_empty_files(self, directory: Path) -> List[Tuple[Path, str]]:
        """查找空文件"""
        empty_files = []
        
        for file_path in directory.rglob("*"):
            if file_path.is_file():
                size = self.check_file_size(file_path)
                if size == 0:
                    rel_path = file_path.relative_to(self.project_root)
                    status = "正常" if str(rel_path) in self.expected_empty_files else "异常"
                    empty_files.append((rel_path, status))
                elif size == -1:
                    rel_path = file_path.relative_to(self.project_root)
                    empty_files.append((rel_path, "无法访问"))
        
        return empty_files

    def find_empty_directories(self, directory: Path) -> List[Tuple[Path, str]]:
        """查找空目录"""
        empty_dirs = []
        
        for dir_path in directory.rglob("*"):
            if dir_path.is_dir() and self.is_directory_empty(dir_path):
                rel_path = dir_path.relative_to(self.project_root)
                status = "正常" if str(rel_path) in self.expected_empty_dirs else "可能异常"
                empty_dirs.append((rel_path, status))
        
        return empty_dirs

    def check_important_files(self) -> List[Tuple[str, str, str]]:
        """检查重要文件是否存在且有内容"""
        missing_or_empty = []
        
        for file_path, description in self.important_files.items():
            full_path = self.project_root / file_path
            
            if not full_path.exists():
                missing_or_empty.append((file_path, description, "文件不存在"))
            elif self.check_file_size(full_path) == 0:
                missing_or_empty.append((file_path, description, "文件为空"))
            elif self.check_file_size(full_path) < 10:
                missing_or_empty.append((file_path, description, "文件内容过少"))
        
        return missing_or_empty

    def analyze_project_structure(self) -> Dict:
        """分析项目结构"""
        results = {
            "frontend_empty_files": [],
            "backend_empty_files": [],
            "frontend_empty_dirs": [],
            "backend_empty_dirs": [],
            "missing_important_files": [],
            "summary": {}
        }
        
        # 检查前端
        if self.frontend_dir.exists():
            results["frontend_empty_files"] = self.find_empty_files(self.frontend_dir)
            results["frontend_empty_dirs"] = self.find_empty_directories(self.frontend_dir)
        
        # 检查后端
        if self.backend_dir.exists():
            results["backend_empty_files"] = self.find_empty_files(self.backend_dir)
            results["backend_empty_dirs"] = self.find_empty_directories(self.backend_dir)
        
        # 检查重要文件
        results["missing_important_files"] = self.check_important_files()
        
        # 生成摘要
        results["summary"] = {
            "total_empty_files": len(results["frontend_empty_files"]) + len(results["backend_empty_files"]),
            "total_empty_dirs": len(results["frontend_empty_dirs"]) + len(results["backend_empty_dirs"]),
            "missing_important": len(results["missing_important_files"]),
            "abnormal_empty_files": len([f for f, s in results["frontend_empty_files"] + results["backend_empty_files"] if s == "异常"]),
            "abnormal_empty_dirs": len([d for d, s in results["frontend_empty_dirs"] + results["backend_empty_dirs"] if s == "可能异常"])
        }
        
        return results

    def generate_report(self, results: Dict):
        """生成检查报告"""
        print("🔍 空文件和空目录检查报告")
        print("=" * 60)
        
        summary = results["summary"]
        print(f"\n📊 总体统计:")
        print(f"   空文件总数: {summary['total_empty_files']}")
        print(f"   空目录总数: {summary['total_empty_dirs']}")
        print(f"   缺失重要文件: {summary['missing_important']}")
        print(f"   异常空文件: {summary['abnormal_empty_files']}")
        print(f"   异常空目录: {summary['abnormal_empty_dirs']}")
        
        # 前端空文件
        if results["frontend_empty_files"]:
            print(f"\n📁 前端空文件 ({len(results['frontend_empty_files'])}个):")
            for file_path, status in results["frontend_empty_files"]:
                icon = "✅" if status == "正常" else "⚠️" if status == "异常" else "❌"
                print(f"   {icon} {file_path} ({status})")
        
        # 后端空文件
        if results["backend_empty_files"]:
            print(f"\n🐍 后端空文件 ({len(results['backend_empty_files'])}个):")
            for file_path, status in results["backend_empty_files"]:
                icon = "✅" if status == "正常" else "⚠️" if status == "异常" else "❌"
                print(f"   {icon} {file_path} ({status})")
        
        # 前端空目录
        if results["frontend_empty_dirs"]:
            print(f"\n📂 前端空目录 ({len(results['frontend_empty_dirs'])}个):")
            for dir_path, status in results["frontend_empty_dirs"]:
                icon = "✅" if status == "正常" else "⚠️"
                print(f"   {icon} {dir_path} ({status})")
        
        # 后端空目录
        if results["backend_empty_dirs"]:
            print(f"\n🗂️  后端空目录 ({len(results['backend_empty_dirs'])}个):")
            for dir_path, status in results["backend_empty_dirs"]:
                icon = "✅" if status == "正常" else "⚠️"
                print(f"   {icon} {dir_path} ({status})")
        
        # 缺失重要文件
        if results["missing_important_files"]:
            print(f"\n❌ 缺失或异常的重要文件 ({len(results['missing_important_files'])}个):")
            for file_path, description, issue in results["missing_important_files"]:
                print(f"   🚨 {file_path} - {description} ({issue})")
        
        # 建议
        print(f"\n💡 建议:")
        if summary["abnormal_empty_files"] > 0:
            print("   - 检查异常的空文件，可能需要添加内容")
        if summary["abnormal_empty_dirs"] > 0:
            print("   - 检查异常的空目录，可能需要添加文件或删除目录")
        if summary["missing_important"] > 0:
            print("   - 立即修复缺失的重要文件，这些文件对项目运行至关重要")
        
        if summary["abnormal_empty_files"] == 0 and summary["missing_important"] == 0:
            print("   ✅ 项目结构正常，空文件和空目录都在预期范围内")

def main():
    """主函数"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    checker = EmptyFileChecker(project_root)
    results = checker.analyze_project_structure()
    checker.generate_report(results)
    
    # 返回退出码
    if results["summary"]["missing_important"] > 0:
        sys.exit(1)  # 有重要文件缺失
    elif results["summary"]["abnormal_empty_files"] > 3:
        sys.exit(1)  # 异常空文件过多
    else:
        sys.exit(0)  # 正常

if __name__ == "__main__":
    main()
