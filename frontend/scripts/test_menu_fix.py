#!/usr/bin/env python3
"""
测试菜单修复效果
检查路由配置和权限设置
"""

import os
import re
from pathlib import Path

def check_route_permissions():
    """检查路由配置中的权限设置"""
    print("🔍 检查路由权限配置...")
    
    router_file = Path('src/router/index.ts')
    if not router_file.exists():
        print("   ❌ 路由文件不存在")
        return False
    
    content = router_file.read_text(encoding='utf-8')
    
    # 查找所有带权限的路由
    permission_routes = re.findall(r'permission:\s*[\'"]([^\'"]+)[\'"]', content)
    
    print(f"   📊 找到 {len(permission_routes)} 个需要权限的路由:")
    for perm in permission_routes:
        print(f"      - {perm}")
    
    # 检查是否有hideInMenu设置
    hidden_routes = re.findall(r'hideInMenu:\s*true', content)
    print(f"   📊 找到 {len(hidden_routes)} 个隐藏菜单项")
    
    return True

def check_env_config():
    """检查环境配置"""
    print("\n⚙️ 检查环境配置...")
    
    env_file = Path('.env.development')
    if env_file.exists():
        content = env_file.read_text(encoding='utf-8')
        
        if 'VITE_ENABLE_AUTH=false' in content:
            print("   ✅ 认证已禁用")
        elif 'VITE_ENABLE_AUTH=true' in content:
            print("   ⚠️  认证已启用")
        else:
            print("   ❌ 认证配置未找到")
        
        print("   📋 当前环境配置:")
        for line in content.split('\n'):
            if line.strip() and not line.startswith('#'):
                print(f"      {line}")
    else:
        print("   ❌ 环境配置文件不存在")

def analyze_menu_structure():
    """分析菜单结构"""
    print("\n📋 分析菜单结构...")
    
    router_file = Path('src/router/index.ts')
    content = router_file.read_text(encoding='utf-8')
    
    # 提取路由定义
    route_pattern = r'{\s*path:\s*[\'"]([^\'"]+)[\'"].*?meta:\s*{([^}]+)}'
    routes = re.findall(route_pattern, content, re.DOTALL)
    
    print(f"   📊 找到 {len(routes)} 个路由定义:")
    
    for path, meta in routes:
        # 提取meta信息
        title_match = re.search(r'title:\s*[\'"]([^\'"]+)[\'"]', meta)
        permission_match = re.search(r'permission:\s*[\'"]([^\'"]+)[\'"]', meta)
        hide_match = re.search(r'hideInMenu:\s*true', meta)
        
        title = title_match.group(1) if title_match else '无标题'
        permission = permission_match.group(1) if permission_match else '无权限要求'
        hidden = '是' if hide_match else '否'
        
        print(f"      路径: {path}")
        print(f"         标题: {title}")
        print(f"         权限: {permission}")
        print(f"         隐藏: {hidden}")
        print()

def create_debug_info():
    """创建调试信息文件"""
    print("📝 创建调试信息...")
    
    debug_info = """# 菜单调试信息

## 问题描述
页面右边菜单只显示"安全态势"，其他菜单项不显示。

## 可能原因
1. 路由权限检查失败
2. 用户权限未正确初始化
3. 菜单过滤逻辑问题

## 修复措施
1. 在MainLayout.vue中修改hasPermission函数，开发模式下返回true
2. 在user.ts中修改hasPermission方法，开发模式下返回true
3. 确保VITE_ENABLE_AUTH=false

## 调试步骤
1. 打开浏览器开发者工具
2. 在Console中输入：
   ```javascript
   // 检查环境变量
   console.log('VITE_ENABLE_AUTH:', import.meta.env.VITE_ENABLE_AUTH)
   
   // 检查路由
   console.log('所有路由:', $router.getRoutes())
   
   // 检查菜单路由
   const layoutRoute = $router.getRoutes().find(r => r.name === 'Layout')
   console.log('菜单路由:', layoutRoute?.children)
   
   // 检查用户store
   console.log('用户store:', useUserStore())
   ```

## 预期结果
所有菜单项都应该显示，包括：
- 仪表板
- 告警管理
- 资产管理
- 威胁狩猎
- 威胁情报
- 事件调查
- 报表分析
- 系统管理
"""
    
    debug_file = Path('menu_debug_info.md')
    debug_file.write_text(debug_info, encoding='utf-8')
    print(f"   ✅ 调试信息已保存到: {debug_file}")

def main():
    """主函数"""
    print("🔍 测试菜单修复效果")
    print("=" * 40)
    
    # 切换到frontend目录
    os.chdir(Path(__file__).parent)
    
    # 检查路由权限
    check_route_permissions()
    
    # 检查环境配置
    check_env_config()
    
    # 分析菜单结构
    analyze_menu_structure()
    
    # 创建调试信息
    create_debug_info()
    
    print("\n💡 解决建议:")
    print("1. 重启前端服务: npm run dev")
    print("2. 清除浏览器缓存并刷新页面")
    print("3. 检查浏览器控制台是否有错误")
    print("4. 如果问题仍存在，查看 menu_debug_info.md 文件")

if __name__ == "__main__":
    main()
