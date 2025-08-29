#!/usr/bin/env python3
"""
修复路由导入问题
将路由配置中的大写文件名改为小写，匹配实际存在的文件
"""

import os
import re
from pathlib import Path

def fix_router_imports():
    """修复路由文件中的导入路径"""
    print("🔧 修复路由导入路径...")
    
    router_file = Path("src/router/index.ts")
    if not router_file.exists():
        print("   ❌ 路由文件不存在")
        return False
    
    # 读取文件内容
    content = router_file.read_text(encoding='utf-8')
    
    # 需要修复的路径映射 (大写 -> 小写)
    path_fixes = {
        '@/views/dashboard/Index.vue': '@/views/dashboard/index.vue',
        '@/views/assets/Index.vue': '@/views/assets/index.vue', 
        '@/views/assets/Detail.vue': '@/views/assets/detail.vue',
        '@/views/hunting/Index.vue': '@/views/hunting/index.vue',
        '@/views/hunting/Detail.vue': '@/views/hunting/detail.vue',
        '@/views/intelligence/Index.vue': '@/views/intelligence/index.vue',
        '@/views/investigation/Index.vue': '@/views/investigation/index.vue',
        '@/views/investigation/Detail.vue': '@/views/investigation/detail.vue',
        '@/views/reports/Index.vue': '@/views/reports/index.vue',
        '@/views/system/Index.vue': '@/views/system/index.vue',
    }
    
    # 执行替换
    changes_made = 0
    for old_path, new_path in path_fixes.items():
        if old_path in content:
            content = content.replace(old_path, new_path)
            changes_made += 1
            print(f"   ✅ 修复: {old_path} -> {new_path}")
    
    if changes_made > 0:
        # 写回文件
        router_file.write_text(content, encoding='utf-8')
        print(f"   🎉 共修复了 {changes_made} 个路径")
        return True
    else:
        print("   ✓ 没有需要修复的路径")
        return True

def check_existing_files():
    """检查实际存在的文件"""
    print("\n📁 检查实际存在的文件...")
    
    # 检查views目录下的文件
    views_dir = Path("src/views")
    if not views_dir.exists():
        print("   ❌ views目录不存在")
        return False
    
    # 遍历所有Vue文件
    vue_files = list(views_dir.rglob("*.vue"))
    
    print(f"   📊 找到 {len(vue_files)} 个Vue文件:")
    for vue_file in sorted(vue_files):
        rel_path = vue_file.relative_to(Path("."))
        print(f"   ✅ {rel_path}")
    
    return True

def verify_route_imports():
    """验证路由导入是否正确"""
    print("\n🔍 验证路由导入...")
    
    router_file = Path("src/router/index.ts")
    if not router_file.exists():
        print("   ❌ 路由文件不存在")
        return False
    
    content = router_file.read_text(encoding='utf-8')
    
    # 提取所有import路径
    import_pattern = r"import\(['\"](@/views/[^'\"]+)['\"]"
    imports = re.findall(import_pattern, content)
    
    print(f"   📊 找到 {len(imports)} 个路由导入:")
    
    all_valid = True
    for import_path in imports:
        # 转换为实际文件路径
        file_path = Path(import_path.replace('@/', 'src/'))
        
        if file_path.exists():
            print(f"   ✅ {import_path}")
        else:
            print(f"   ❌ {import_path} (文件不存在)")
            all_valid = False
    
    return all_valid

def remove_duplicate_files():
    """删除重复创建的大写文件"""
    print("\n🧹 清理重复的大写文件...")
    
    # 可能重复的大写文件
    duplicate_files = [
        "src/views/dashboard/Index.vue",
        "src/views/assets/Index.vue",
        "src/views/assets/Detail.vue", 
        "src/views/hunting/Detail.vue",
        "src/views/intelligence/Index.vue",
        "src/views/investigation/Index.vue",
        "src/views/investigation/Detail.vue",
        "src/views/reports/Index.vue",
        "src/views/system/Index.vue",
    ]
    
    removed_count = 0
    for file_path in duplicate_files:
        file_obj = Path(file_path)
        if file_obj.exists():
            # 检查是否有对应的小写文件
            lowercase_path = file_path.replace('/Index.vue', '/index.vue').replace('/Detail.vue', '/detail.vue')
            lowercase_obj = Path(lowercase_path)
            
            if lowercase_obj.exists():
                # 如果小写文件存在，删除大写文件
                file_obj.unlink()
                removed_count += 1
                print(f"   🗑️  删除重复文件: {file_path}")
            else:
                # 如果小写文件不存在，重命名大写文件为小写
                file_obj.rename(lowercase_obj)
                print(f"   📝 重命名: {file_path} -> {lowercase_path}")
    
    if removed_count > 0:
        print(f"   🎉 清理了 {removed_count} 个重复文件")
    else:
        print("   ✓ 没有发现重复文件")

def main():
    """主函数"""
    print("🔧 修复路由导入问题")
    print("=" * 40)
    
    # 切换到frontend目录
    os.chdir(Path(__file__).parent)
    
    # 检查现有文件
    if not check_existing_files():
        return 1
    
    # 修复路由导入
    if not fix_router_imports():
        return 1
    
    # 清理重复文件
    remove_duplicate_files()
    
    # 验证修复结果
    if verify_route_imports():
        print("\n🎉 所有路由导入都已修复！")
        print("\n现在可以启动开发服务器:")
        print("   npm run dev")
        return 0
    else:
        print("\n❌ 仍有路由导入问题，请检查")
        return 1

if __name__ == "__main__":
    exit(main())
