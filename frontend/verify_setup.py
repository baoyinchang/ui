#!/usr/bin/env python3
"""
验证前端设置脚本
检查所有必需的文件和依赖是否正确配置
"""

import os
import json
from pathlib import Path

def check_package_json():
    """检查package.json和依赖"""
    print("📦 检查package.json...")
    
    package_file = Path("package.json")
    if not package_file.exists():
        print("   ❌ package.json不存在")
        return False
    
    try:
        with open(package_file, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
        
        print(f"   ✅ 项目名称: {package_data.get('name', 'N/A')}")
        print(f"   ✅ 项目版本: {package_data.get('version', 'N/A')}")
        
        # 检查关键依赖
        dependencies = package_data.get('dependencies', {})
        dev_dependencies = package_data.get('devDependencies', {})
        all_deps = {**dependencies, **dev_dependencies}
        
        required_deps = [
            'vue', 'vue-router', 'pinia', 'element-plus',
            'axios', 'echarts', 'vite', '@vitejs/plugin-vue',
            'typescript', 'unplugin-auto-import', 'unplugin-vue-components'
        ]
        
        missing_deps = []
        for dep in required_deps:
            if dep in all_deps:
                print(f"   ✅ {dep}: {all_deps[dep]}")
            else:
                missing_deps.append(dep)
                print(f"   ❌ {dep}: 缺失")
        
        if missing_deps:
            print(f"   ⚠️  缺失依赖: {missing_deps}")
            return False
        
        return True
    except Exception as e:
        print(f"   ❌ 解析package.json失败: {e}")
        return False

def check_vue_files():
    """检查Vue文件"""
    print("\n📄 检查Vue文件...")
    
    vue_files = [
        "src/App.vue",
        "src/main.ts",
        "src/views/dashboard/Index.vue",
        "src/views/assets/Index.vue",
        "src/views/assets/Detail.vue",
        "src/views/hunting/Detail.vue",
        "src/views/intelligence/Index.vue",
        "src/views/investigation/Index.vue",
        "src/views/investigation/Detail.vue",
        "src/views/reports/Index.vue",
        "src/views/system/Index.vue",
        "src/views/login/index.vue",
    ]
    
    missing_files = []
    for file_path in vue_files:
        file_obj = Path(file_path)
        if file_obj.exists():
            print(f"   ✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"   ❌ {file_path}")
    
    return len(missing_files) == 0

def check_style_files():
    """检查样式文件"""
    print("\n🎨 检查样式文件...")
    
    style_files = [
        "src/styles/index.scss",
        "src/styles/mixins.scss",
        "src/assets/css/variables.scss",
    ]
    
    missing_files = []
    for file_path in style_files:
        file_obj = Path(file_path)
        if file_obj.exists():
            print(f"   ✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"   ❌ {file_path}")
    
    return len(missing_files) == 0

def check_config_files():
    """检查配置文件"""
    print("\n⚙️ 检查配置文件...")
    
    config_files = [
        "vite.config.ts",
        "tsconfig.json",
        "index.html",
        ".env.development",
    ]
    
    missing_files = []
    for file_path in config_files:
        file_obj = Path(file_path)
        if file_obj.exists():
            print(f"   ✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"   ❌ {file_path}")
    
    return len(missing_files) == 0

def check_router_config():
    """检查路由配置"""
    print("\n🛣️ 检查路由配置...")
    
    router_file = Path("src/router/index.ts")
    if not router_file.exists():
        print("   ❌ 路由配置文件不存在")
        return False
    
    try:
        content = router_file.read_text(encoding='utf-8')
        
        # 检查是否包含基本路由
        required_routes = [
            'dashboard', 'assets', 'hunting', 'intelligence',
            'investigation', 'reports', 'system', 'login'
        ]
        
        missing_routes = []
        for route in required_routes:
            if route in content:
                print(f"   ✅ {route} 路由")
            else:
                missing_routes.append(route)
                print(f"   ❌ {route} 路由")
        
        return len(missing_routes) == 0
    except Exception as e:
        print(f"   ❌ 读取路由配置失败: {e}")
        return False

def check_node_modules():
    """检查node_modules"""
    print("\n📚 检查node_modules...")
    
    node_modules = Path("node_modules")
    if not node_modules.exists():
        print("   ❌ node_modules不存在，需要运行 npm install")
        return False
    
    # 检查关键包是否存在
    key_packages = [
        'vue', 'vue-router', 'pinia', 'element-plus',
        'vite', '@vitejs/plugin-vue', 'typescript'
    ]
    
    missing_packages = []
    for package in key_packages:
        package_dir = node_modules / package
        if package_dir.exists():
            print(f"   ✅ {package}")
        else:
            missing_packages.append(package)
            print(f"   ❌ {package}")
    
    if missing_packages:
        print(f"   ⚠️  缺失包: {missing_packages}")
        print("   💡 运行 npm install 安装缺失的包")
        return False
    
    return True

def main():
    """主函数"""
    print("🔍 H-System EDR 前端设置验证")
    print("=" * 50)
    
    # 切换到frontend目录
    os.chdir(Path(__file__).parent)
    
    # 执行所有检查
    checks = [
        ("Package.json", check_package_json),
        ("Vue文件", check_vue_files),
        ("样式文件", check_style_files),
        ("配置文件", check_config_files),
        ("路由配置", check_router_config),
        ("Node模块", check_node_modules),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ {name}检查失败: {e}")
            results.append((name, False))
    
    # 总结结果
    print("\n" + "=" * 50)
    print("📊 验证结果总结")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for name, result in results:
        if result:
            print(f"✅ {name}: 通过")
            passed += 1
        else:
            print(f"❌ {name}: 失败")
            failed += 1
    
    print(f"\n总计: {passed}个通过, {failed}个失败")
    
    if failed == 0:
        print("\n🎉 所有检查都通过了！可以启动开发服务器:")
        print("   npm run dev")
        print("   或者 ./start.sh")
        return 0
    else:
        print(f"\n⚠️  发现 {failed} 个问题，请先修复后再启动")
        return 1

if __name__ == "__main__":
    exit(main())
