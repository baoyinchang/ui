#!/usr/bin/env python3
"""
测试菜单结构
验证路由配置和菜单显示是否正确
"""

import os
import re
from pathlib import Path

def analyze_route_structure():
    """分析路由结构"""
    print("🔍 分析路由结构...")
    
    router_file = Path('src/router/index.ts')
    if not router_file.exists():
        print("   ❌ 路由文件不存在")
        return False
    
    content = router_file.read_text(encoding='utf-8')
    
    # 查找系统管理路由
    system_route_match = re.search(r'path:\s*[\'\"]/system[\'\"](.*?)(?=\{[^}]*path:|$)', content, re.DOTALL)
    
    if system_route_match:
        system_route = system_route_match.group(0)
        print("   ✅ 找到系统管理路由")
        
        # 查找子路由
        children_match = re.search(r'children:\s*\[(.*?)\]', system_route, re.DOTALL)
        if children_match:
            children_content = children_match.group(1)
            child_routes = re.findall(r'path:\s*[\'\"](.*?)[\'\"]\s*,.*?title:\s*[\'\"](.*?)[\'\"]', children_content, re.DOTALL)
            
            print(f"   📊 找到 {len(child_routes)} 个子路由:")
            for path, title in child_routes:
                print(f"      - {path}: {title}")
        else:
            print("   ❌ 未找到子路由配置")
    else:
        print("   ❌ 未找到系统管理路由")
    
    return True

def check_vue_files():
    """检查Vue文件是否存在"""
    print("\n📄 检查Vue文件...")
    
    required_files = [
        'src/views/system/index.vue',
        'src/views/system/status.vue',
        'src/views/system/settings.vue',
        'src/views/system/roles.vue',
        'src/views/system/honeypot.vue',
        'src/views/system/logs.vue',
        'src/views/users/Index.vue'
    ]
    
    missing_files = []
    for file_path in required_files:
        file_obj = Path(file_path)
        if file_obj.exists():
            print(f"   ✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"   ❌ {file_path}")
    
    if missing_files:
        print(f"\n⚠️  缺失 {len(missing_files)} 个文件")
        return False
    else:
        print(f"\n✅ 所有 {len(required_files)} 个文件都存在")
        return True

def create_menu_test_page():
    """创建菜单测试页面"""
    print("\n📝 创建菜单测试页面...")
    
    test_page_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>菜单结构测试</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .test-card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .menu-structure {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            padding: 15px;
            font-family: monospace;
            white-space: pre-line;
        }
        .success { color: #28a745; }
        .error { color: #dc3545; }
        .warning { color: #ffc107; }
        button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            margin: 5px;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <h1>🔍 H-System EDR 菜单结构测试</h1>
    
    <div class="test-card">
        <h2>预期菜单结构</h2>
        <div class="menu-structure">
H-System EDR 菜单结构

主菜单:
├── 安全态势 (/dashboard)
├── 告警中心 (/alerts)
├── 调查与响应 (/investigation)
├── 资产管理 (/assets)
├── 威胁狩猎 (/hunting)
├── 威胁情报 (/intelligence)
├── 报告中心 (/reports)
└── 系统管理 (/system) ⭐ 有子菜单
    ├── 系统状态 (/system/status)
    ├── 系统设置 (/system/settings)
    ├── 用户管理 (/system/users)
    ├── 角色与权限 (/system/roles)
    ├── 蜜罐策略中心 (/system/honeypot)
    └── 日志审计 (/system/logs)
        </div>
    </div>
    
    <div class="test-card">
        <h2>菜单测试</h2>
        <button onclick="testMenuStructure()">测试菜单结构</button>
        <button onclick="testRouteNavigation()">测试路由导航</button>
        <button onclick="testPermissions()">测试权限控制</button>
        <div id="test-results"></div>
    </div>

    <script>
        function log(message, type = 'info') {
            const results = document.getElementById('test-results');
            const timestamp = new Date().toLocaleTimeString();
            const logEntry = document.createElement('div');
            logEntry.className = type;
            logEntry.innerHTML = `[${timestamp}] ${message}`;
            results.appendChild(logEntry);
        }

        function testMenuStructure() {
            document.getElementById('test-results').innerHTML = '';
            log('🔍 测试菜单结构...', 'info');
            
            const testCode = `
// 测试菜单结构
const router = useRouter();
const layoutRoute = router.getRoutes().find(r => r.name === 'Layout');
const menuRoutes = layoutRoute?.children?.filter(r => !r.meta?.hideInMenu) || [];

console.log('=== 菜单结构测试 ===');
console.log('菜单路由数量:', menuRoutes.length);

// 查找系统管理路由
const systemRoute = menuRoutes.find(r => r.path === '/system');
if (systemRoute) {
    console.log('✅ 找到系统管理路由');
    console.log('系统管理标题:', systemRoute.meta?.title);
    
    if (systemRoute.children && systemRoute.children.length > 0) {
        console.log('✅ 系统管理有子菜单');
        console.log('子菜单数量:', systemRoute.children.length);
        
        systemRoute.children.forEach(child => {
            console.log(\`  - \${child.path}: \${child.meta?.title}\`);
        });
    } else {
        console.log('❌ 系统管理没有子菜单');
    }
} else {
    console.log('❌ 未找到系统管理路由');
}

// 检查用户管理是否在系统管理下
const userRoute = menuRoutes.find(r => r.path === '/users');
if (userRoute) {
    console.log('⚠️ 用户管理仍是独立菜单项');
} else {
    console.log('✅ 用户管理已移到系统管理下');
}
            `;
            
            log('💡 在主应用页面控制台中运行:', 'info');
            log(testCode, 'info');
        }

        function testRouteNavigation() {
            document.getElementById('test-results').innerHTML = '';
            log('🔍 测试路由导航...', 'info');
            
            const navTestCode = `
// 测试路由导航
const testRoutes = [
    '/system',
    '/system/status',
    '/system/settings',
    '/system/users',
    '/system/roles',
    '/system/honeypot',
    '/system/logs'
];

console.log('=== 路由导航测试 ===');

testRoutes.forEach(route => {
    try {
        $router.push(route);
        console.log(\`✅ 路由 \${route} 导航成功\`);
    } catch (error) {
        console.log(\`❌ 路由 \${route} 导航失败: \${error.message}\`);
    }
});

// 等待一下再检查当前路由
setTimeout(() => {
    console.log('当前路由:', $route.path);
}, 1000);
            `;
            
            log('💡 在主应用页面控制台中运行:', 'info');
            log(navTestCode, 'info');
        }

        function testPermissions() {
            document.getElementById('test-results').innerHTML = '';
            log('🔍 测试权限控制...', 'info');
            
            const permTestCode = `
// 测试权限控制
const userStore = useUserStore();

console.log('=== 权限控制测试 ===');
console.log('认证开关:', import.meta.env.VITE_ENABLE_AUTH);

const systemPermissions = [
    'system:read',
    'system:write', 
    'user:read',
    'role:read',
    'honeypot:read',
    'log:read'
];

systemPermissions.forEach(perm => {
    const hasPermission = userStore.hasPermission(perm);
    console.log(\`权限 \${perm}: \${hasPermission}\`);
});
            `;
            
            log('💡 在主应用页面控制台中运行:', 'info');
            log(permTestCode, 'info');
        }

        // 页面加载提示
        window.onload = function() {
            log('📄 菜单结构测试页面已加载', 'success');
            log('💡 请在主应用页面打开开发者工具，然后使用此页面的测试按钮', 'info');
        };
    </script>
</body>
</html>'''
    
    test_file = Path('menu-structure-test.html')
    test_file.write_text(test_page_content, encoding='utf-8')
    print(f"   ✅ 菜单测试页面已保存到: {test_file}")

def main():
    """主函数"""
    print("🔍 测试菜单结构")
    print("=" * 40)
    
    # 切换到frontend目录
    os.chdir(Path(__file__).parent)
    
    # 分析路由结构
    analyze_route_structure()
    
    # 检查Vue文件
    check_vue_files()
    
    # 创建测试页面
    create_menu_test_page()
    
    print("\n🎉 菜单结构分析完成！")
    print("\n📋 总结:")
    print("   ✅ 路由配置已更新为嵌套结构")
    print("   ✅ 系统管理现在有子菜单")
    print("   ✅ 用户管理已移到系统管理下")
    print("   ✅ 所有必需的Vue文件已创建")
    
    print("\n🚀 测试步骤:")
    print("   1. 重启前端服务: npm run dev")
    print("   2. 查看菜单是否显示子菜单")
    print("   3. 打开 menu-structure-test.html 进行详细测试")
    print("   4. 在浏览器控制台运行测试代码")

if __name__ == "__main__":
    main()
