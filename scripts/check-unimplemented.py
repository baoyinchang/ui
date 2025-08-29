#!/usr/bin/env python3
"""
检查未实现功能脚本
扫描项目中的TODO、FIXME、未实现的函数等
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

class UnimplementedChecker:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.frontend_dir = self.project_root / "frontend"
        self.backend_dir = self.project_root / "backend"
        
        # 未实现标记的正则表达式
        self.unimplemented_patterns = [
            r'# 实现将在此处添加',
            r'# 实现将在此处.*',
            r'// 实现将在此处.*',
            r'// TODO:.*',
            r'# TODO:.*',
            r'// FIXME:.*',
            r'# FIXME:.*',
            r'// 功能将在此处.*',
            r'# 功能将在此处.*',
            r'// 方法将在此处.*',
            r'# 方法将在此处.*',
            r'// 组件逻辑.*',
            r'// 模块内容将在此处.*',
            r'# 模块内容将在此处.*',
            r'return \[\].*# 空实现',
            r'return \{\}.*# 空实现',
            r'return None.*# 空实现',
            r'pass.*# 占位符',
            r'console\.log\(.*正在开发中.*\)',
            r'<p>.*正在开发中.*</p>',
            r'<p>.*此页面正在开发中.*</p>',
        ]
        
        # 空实现模式
        self.empty_implementation_patterns = [
            r'def \w+\(.*\):\s*""".*"""\s*# 实现将在此处添加\s*return',
            r'async def \w+\(.*\):\s*""".*"""\s*# 实现将在此处添加\s*return',
            r'function \w+\(.*\) \{\s*// 实现将在此处添加\s*\}',
            r'const \w+ = \(.*\) => \{\s*// 实现将在此处添加\s*\}',
        ]
        
        self.issues = []

    def scan_file(self, file_path: Path) -> List[Dict]:
        """扫描单个文件中的未实现功能"""
        issues = []
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                line_stripped = line.strip()
                
                # 检查未实现标记
                for pattern in self.unimplemented_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append({
                            'file': file_path.relative_to(self.project_root),
                            'line': line_num,
                            'content': line_stripped,
                            'type': 'unimplemented',
                            'severity': 'high' if '实现将在此处' in line else 'medium'
                        })
                
                # 检查空函数/方法
                if re.search(r'def \w+.*:\s*$', line) or re.search(r'function \w+.*\{\s*$', line):
                    # 检查接下来几行是否只有注释和return
                    next_lines = lines[line_num:line_num+5] if line_num < len(lines) else []
                    function_body = '\n'.join(next_lines)
                    
                    if ('实现将在此处' in function_body or 
                        '功能将在此处' in function_body or
                        re.search(r'return \[\]\s*$', function_body) or
                        re.search(r'return \{\}\s*$', function_body) or
                        re.search(r'return None\s*$', function_body)):
                        
                        issues.append({
                            'file': file_path.relative_to(self.project_root),
                            'line': line_num,
                            'content': line_stripped,
                            'type': 'empty_function',
                            'severity': 'high'
                        })
                
                # 检查Vue组件中的占位内容
                if file_path.suffix == '.vue':
                    if ('正在开发中' in line or 
                        '此页面正在开发中' in line or
                        '组件逻辑' in line):
                        issues.append({
                            'file': file_path.relative_to(self.project_root),
                            'line': line_num,
                            'content': line_stripped,
                            'type': 'placeholder_content',
                            'severity': 'medium'
                        })
                
                # 检查API接口中的空实现
                if 'api' in str(file_path).lower() and file_path.suffix in ['.ts', '.js']:
                    if ('API方法将在此处定义' in line or
                        '接口将在此处定义' in line):
                        issues.append({
                            'file': file_path.relative_to(self.project_root),
                            'line': line_num,
                            'content': line_stripped,
                            'type': 'empty_api',
                            'severity': 'high'
                        })
        
        except Exception as e:
            print(f"扫描文件失败: {file_path} - {e}")
        
        return issues

    def scan_directory(self, directory: Path) -> List[Dict]:
        """扫描目录中的所有文件"""
        all_issues = []
        
        if not directory.exists():
            return all_issues
        
        # 扫描的文件类型
        file_extensions = {'.py', '.ts', '.js', '.vue', '.tsx', '.jsx'}
        
        for file_path in directory.rglob("*"):
            if (file_path.is_file() and 
                file_path.suffix in file_extensions and
                'node_modules' not in str(file_path) and
                '.git' not in str(file_path)):
                
                issues = self.scan_file(file_path)
                all_issues.extend(issues)
        
        return all_issues

    def analyze_project(self) -> Dict:
        """分析整个项目"""
        print("🔍 扫描未实现功能...")
        
        # 扫描前端
        frontend_issues = self.scan_directory(self.frontend_dir)
        
        # 扫描后端
        backend_issues = self.scan_directory(self.backend_dir)
        
        all_issues = frontend_issues + backend_issues
        
        # 按类型分组
        issues_by_type = {}
        for issue in all_issues:
            issue_type = issue['type']
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append(issue)
        
        # 按严重程度分组
        issues_by_severity = {'high': [], 'medium': [], 'low': []}
        for issue in all_issues:
            severity = issue.get('severity', 'medium')
            issues_by_severity[severity].append(issue)
        
        # 按文件分组
        issues_by_file = {}
        for issue in all_issues:
            file_path = str(issue['file'])
            if file_path not in issues_by_file:
                issues_by_file[file_path] = []
            issues_by_file[file_path].append(issue)
        
        return {
            'total_issues': len(all_issues),
            'frontend_issues': len(frontend_issues),
            'backend_issues': len(backend_issues),
            'issues_by_type': issues_by_type,
            'issues_by_severity': issues_by_severity,
            'issues_by_file': issues_by_file,
            'all_issues': all_issues
        }

    def generate_report(self, analysis: Dict):
        """生成详细报告"""
        print("\n" + "="*80)
        print("🚨 未实现功能检查报告")
        print("="*80)
        
        total = analysis['total_issues']
        frontend = analysis['frontend_issues']
        backend = analysis['backend_issues']
        
        print(f"\n📊 总体统计:")
        print(f"   总未实现项目: {total}")
        print(f"   前端未实现: {frontend}")
        print(f"   后端未实现: {backend}")
        
        # 按严重程度统计
        severity_stats = analysis['issues_by_severity']
        print(f"\n🚨 按严重程度分类:")
        print(f"   高优先级: {len(severity_stats['high'])} 个")
        print(f"   中优先级: {len(severity_stats['medium'])} 个")
        print(f"   低优先级: {len(severity_stats['low'])} 个")
        
        # 按类型统计
        type_stats = analysis['issues_by_type']
        print(f"\n📋 按类型分类:")
        for issue_type, issues in type_stats.items():
            type_name = {
                'unimplemented': '未实现标记',
                'empty_function': '空函数/方法',
                'placeholder_content': '占位内容',
                'empty_api': '空API接口'
            }.get(issue_type, issue_type)
            print(f"   {type_name}: {len(issues)} 个")
        
        # 详细问题列表
        if total > 0:
            print(f"\n📝 详细问题列表:")
            print("-" * 80)
            
            # 按文件分组显示
            for file_path, issues in analysis['issues_by_file'].items():
                print(f"\n📁 {file_path} ({len(issues)}个问题):")
                
                for issue in issues[:5]:  # 每个文件最多显示5个问题
                    severity_icon = {
                        'high': '🔴',
                        'medium': '🟡', 
                        'low': '🟢'
                    }.get(issue['severity'], '⚪')
                    
                    print(f"   {severity_icon} 第{issue['line']}行: {issue['content'][:80]}...")
                
                if len(issues) > 5:
                    print(f"   ... 还有 {len(issues) - 5} 个问题")
        
        # 修复建议
        print(f"\n💡 修复建议:")
        if len(severity_stats['high']) > 0:
            print("   🔴 高优先级问题需要立即修复:")
            print("      - 实现核心业务逻辑")
            print("      - 完善API接口功能")
            print("      - 补充数据库操作")
        
        if len(severity_stats['medium']) > 0:
            print("   🟡 中优先级问题建议尽快修复:")
            print("      - 完善页面内容")
            print("      - 添加错误处理")
            print("      - 优化用户体验")
        
        if total == 0:
            print("   ✅ 恭喜！没有发现未实现的功能")
        else:
            print(f"\n📈 完成度评估:")
            # 简单的完成度计算
            total_files = len(analysis['issues_by_file'])
            if total_files > 0:
                completion_rate = max(0, 100 - (total * 2))  # 每个未实现项目扣2分
                print(f"   项目完成度: {completion_rate:.1f}%")
                
                if completion_rate >= 80:
                    print("   🎉 项目基本完成，可以进入测试阶段")
                elif completion_rate >= 60:
                    print("   🚧 项目大部分功能已完成，需要补充细节")
                elif completion_rate >= 40:
                    print("   ⚠️  项目框架已搭建，需要实现核心功能")
                else:
                    print("   🚨 项目还在早期阶段，需要大量开发工作")

def main():
    """主函数"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    checker = UnimplementedChecker(project_root)
    analysis = checker.analyze_project()
    checker.generate_report(analysis)
    
    # 返回退出码
    high_priority_issues = len(analysis['issues_by_severity']['high'])
    if high_priority_issues > 20:
        return 1  # 高优先级问题太多
    elif high_priority_issues > 0:
        return 2  # 有高优先级问题但数量可控
    else:
        return 0  # 没有高优先级问题

if __name__ == "__main__":
    exit(main())
