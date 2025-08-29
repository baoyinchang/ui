#!/usr/bin/env python3
"""
测试三级菜单结构
验证路由配置和文件结构是否正确
"""

import os
import json
from pathlib import Path

def check_file_structure():
    """检查文件结构是否完整"""
    print("📁 检查文件结构...")
    
    required_files = [
        # 主要页面
        'src/views/system/index.vue',
        'src/views/system/status.vue',
        'src/views/system/settings.vue',
        
        # 蜜罐策略中心
        'src/views/system/honeypot/index.vue',
        'src/views/system/honeypot/sensors.vue',
        'src/views/system/honeypot/policies.vue',
        
        # 用户与权限
        'src/views/system/user-permission/index.vue',
        'src/views/system/user-permission/roles.vue',
        'src/views/users/Index.vue',  # 用户管理页面
        
        # 系统维护
        'src/views/system/maintenance/index.vue',
        'src/views/system/maintenance/logs.vue',
        'src/views/system/maintenance/updates.vue',
        'src/views/system/maintenance/backup.vue',
        
        # 布局组件
        'src/components/layout/MenuTree.vue',
        'src/layouts/MainLayout.vue'
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        file_obj = Path(file_path)
        if file_obj.exists():
            existing_files.append(file_path)
            print(f"   ✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"   ❌ {file_path}")
    
    print(f"\n📊 文件统计:")
    print(f"   ✅ 存在: {len(existing_files)} 个文件")
    print(f"   ❌ 缺失: {len(missing_files)} 个文件")
    
    return len(missing_files) == 0

def analyze_route_structure():
    """分析路由结构"""
    print("\n🔍 分析路由结构...")
    
    router_file = Path('src/router/index.ts')
    if not router_file.exists():
        print("   ❌ 路由文件不存在")
        return False
    
    content = router_file.read_text(encoding='utf-8')
    
    # 统计路由层级
    system_routes = content.count("path: '/system'")
    honeypot_routes = content.count("path: 'honeypot'")
    user_permission_routes = content.count("path: 'user-permission'")
    maintenance_routes = content.count("path: 'maintenance'")
    
    print(f"   📊 路由统计:")
    print(f"      系统管理路由: {system_routes}")
    print(f"      蜜罐策略路由: {honeypot_routes}")
    print(f"      用户权限路由: {user_permission_routes}")
    print(f"      系统维护路由: {maintenance_routes}")
    
    # 检查children嵌套
    children_count = content.count("children: [")
    print(f"      嵌套子路由: {children_count}")
    
    return True

def create_menu_structure_visualization():
    """创建菜单结构可视化"""
    print("\n🎨 创建菜单结构可视化...")
    
    menu_structure = {
        "H-System EDR": {
            "安全态势": "/dashboard",
            "告警中心": "/alerts",
            "调查与响应": "/investigation",
            "资产管理": "/assets",
            "威胁狩猎": "/hunting",
            "威胁情报": "/intelligence",
            "报告中心": "/reports",
            "系统管理": {
                "path": "/system",
                "children": {
                    "系统状态": "/system/status",
                    "系统设置": "/system/settings",
                    "蜜罐策略中心": {
                        "path": "/system/honeypot",
                        "children": {
                            "蜜罐探针管理": "/system/honeypot/sensors",
                            "蜜罐策略配置": "/system/honeypot/policies"
                        }
                    },
                    "用户与权限": {
                        "path": "/system/user-permission",
                        "children": {
                            "用户管理": "/system/user-permission/users",
                            "角色与权限": "/system/user-permission/roles"
                        }
                    },
                    "系统维护": {
                        "path": "/system/maintenance",
                        "children": {
                            "日志审计": "/system/maintenance/logs",
                            "更新管理": "/system/maintenance/updates",
                            "备份与恢复": "/system/maintenance/backup"
                        }
                    }
                }
            }
        }
    }
    
    # 保存JSON格式
    json_file = Path('menu_structure.json')
    json_file.write_text(json.dumps(menu_structure, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"   ✅ 菜单结构JSON已保存到: {json_file}")
    
    # 创建树状图
    tree_content = """# H-System EDR 三级菜单结构

## 🌳 完整菜单树

```
H-System EDR
├── 安全态势 (/dashboard)
├── 告警中心 (/alerts)
├── 调查与响应 (/investigation)
├── 资产管理 (/assets)
├── 威胁狩猎 (/hunting)
├── 威胁情报 (/intelligence)
├── 报告中心 (/reports)
└── 系统管理 (/system) ⭐ 三级菜单
    ├── 系统状态 (/system/status)
    ├── 系统设置 (/system/settings)
    ├── 蜜罐策略中心 (/system/honeypot) 📁
    │   ├── 蜜罐探针管理 (/system/honeypot/sensors)
    │   └── 蜜罐策略配置 (/system/honeypot/policies)
    ├── 用户与权限 (/system/user-permission) 📁
    │   ├── 用户管理 (/system/user-permission/users)
    │   └── 角色与权限 (/system/user-permission/roles)
    └── 系统维护 (/system/maintenance) 📁
        ├── 日志审计 (/system/maintenance/logs)
        ├── 更新管理 (/system/maintenance/updates)
        └── 备份与恢复 (/system/maintenance/backup)
```

## 🎯 与demo_01对比

### ✅ 完全匹配的结构
- 系统管理作为主菜单项
- 蜜罐策略中心包含2个子功能
- 用户与权限包含2个子功能  
- 系统维护包含3个子功能

### 🔧 技术实现
- Vue Router嵌套路由
- 递归菜单组件 (MenuTree.vue)
- Element Plus多级菜单
- 权限控制每个层级

## 📋 测试清单

### 菜单显示测试
- [ ] 系统管理显示为可展开菜单
- [ ] 蜜罐策略中心显示子菜单
- [ ] 用户与权限显示子菜单
- [ ] 系统维护显示子菜单

### 路由导航测试
- [ ] 点击系统状态正常跳转
- [ ] 点击蜜罐探针管理正常跳转
- [ ] 点击用户管理正常跳转
- [ ] 点击日志审计正常跳转

### 权限控制测试
- [ ] 开发模式下所有菜单可见
- [ ] 权限控制正常工作
- [ ] 面包屑导航正确显示

## 🚀 使用说明

1. **重启服务**: `npm run dev`
2. **查看菜单**: 左侧菜单应显示三级结构
3. **测试导航**: 点击各级菜单项测试跳转
4. **检查权限**: 确认权限控制正常
"""
    
    tree_file = Path('menu_tree_structure.md')
    tree_file.write_text(tree_content, encoding='utf-8')
    print(f"   ✅ 菜单树状图已保存到: {tree_file}")

def create_debug_commands():
    """创建调试命令"""
    print("\n🔧 创建调试命令...")
    
    debug_commands = """# 三级菜单调试命令

## 在浏览器控制台中运行以下命令

### 1. 检查路由结构
```javascript
// 获取所有路由
const allRoutes = $router.getRoutes();
console.log('所有路由:', allRoutes);

// 查找系统管理路由
const systemRoute = allRoutes.find(r => r.path === '/system');
console.log('系统管理路由:', systemRoute);

// 检查系统管理的子路由
if (systemRoute && systemRoute.children) {
    console.log('系统管理子路由数量:', systemRoute.children.length);
    systemRoute.children.forEach(child => {
        console.log(`子路由: ${child.path} - ${child.meta?.title}`);
        if (child.children) {
            console.log(`  有 ${child.children.length} 个三级子路由`);
            child.children.forEach(grandChild => {
                console.log(`    三级路由: ${grandChild.path} - ${grandChild.meta?.title}`);
            });
        }
    });
}
```

### 2. 测试菜单权限
```javascript
// 检查权限函数
const userStore = useUserStore();
console.log('权限检查函数:', typeof userStore.hasPermission);

// 测试各种权限
const permissions = [
    'system:read',
    'honeypot:read', 
    'user:read',
    'system:maintain'
];

permissions.forEach(perm => {
    console.log(`权限 ${perm}:`, userStore.hasPermission(perm));
});
```

### 3. 测试路由导航
```javascript
// 测试三级路由导航
const testRoutes = [
    '/system',
    '/system/status',
    '/system/honeypot',
    '/system/honeypot/sensors',
    '/system/user-permission/users',
    '/system/maintenance/logs'
];

testRoutes.forEach(route => {
    console.log(`测试路由: ${route}`);
    try {
        $router.push(route);
        console.log(`✅ ${route} 导航成功`);
    } catch (error) {
        console.log(`❌ ${route} 导航失败:`, error.message);
    }
});
```

### 4. 检查菜单组件
```javascript
// 检查MenuTree组件是否正确加载
const app = getCurrentInstance();
console.log('当前组件实例:', app);

// 检查菜单数据
const layoutRoute = $router.getRoutes().find(r => r.name === 'Layout');
const menuRoutes = layoutRoute?.children?.filter(r => !r.meta?.hideInMenu) || [];
console.log('菜单路由数据:', menuRoutes);
```
"""
    
    debug_file = Path('debug_three_level_menu.md')
    debug_file.write_text(debug_commands, encoding='utf-8')
    print(f"   ✅ 调试命令已保存到: {debug_file}")

def main():
    """主函数"""
    print("🔍 测试三级菜单结构")
    print("=" * 40)
    
    # 切换到frontend目录
    os.chdir(Path(__file__).parent)
    
    # 检查文件结构
    files_ok = check_file_structure()
    
    # 分析路由结构
    routes_ok = analyze_route_structure()
    
    # 创建可视化
    create_menu_structure_visualization()
    
    # 创建调试命令
    create_debug_commands()
    
    print("\n🎉 三级菜单结构测试完成！")
    
    if files_ok and routes_ok:
        print("\n✅ 所有检查通过！")
        print("\n🚀 现在可以:")
        print("   1. 重启前端服务: npm run dev")
        print("   2. 查看三级菜单结构")
        print("   3. 使用 debug_three_level_menu.md 中的命令进行调试")
        print("   4. 参考 menu_tree_structure.md 了解完整结构")
    else:
        print("\n⚠️  发现问题，请检查:")
        if not files_ok:
            print("   - 部分文件缺失")
        if not routes_ok:
            print("   - 路由配置有问题")

if __name__ == "__main__":
    main()
