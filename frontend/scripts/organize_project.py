#!/usr/bin/env python3
"""
整理项目结构
1. 将测试脚本和工具移动到scripts目录
2. 创建缺失的图标文件
3. 清理根目录
"""

import os
import shutil
from pathlib import Path

def create_scripts_directory():
    """创建scripts目录并移动文件"""
    print("📁 整理项目目录结构...")

    # 创建scripts目录
    scripts_dir = Path('scripts')
    scripts_dir.mkdir(exist_ok=True)

    # 需要移动的文件列表
    files_to_move = [
        'test_menu_fix.py',
        'create_system_pages.py',
        'test_menu_structure.py',
        'create_complete_system_structure.py',
        'test_three_level_menu.py',
        'create_complete_system_structure.py',
        'debug-menu.html',
        'menu-structure-test.html',
        'menu_debug_info.md',
        'menu_structure.md',
        'complete_menu_structure.md',
        'menu_tree_structure.md',
        'debug_three_level_menu.md',
        'menu_structure.json'
    ]

    moved_count = 0
    for file_name in files_to_move:
        file_path = Path(file_name)
        if file_path.exists():
            target_path = scripts_dir / file_name
            try:
                shutil.move(str(file_path), str(target_path))
                print(f"   ✅ 移动: {file_name} -> scripts/{file_name}")
                moved_count += 1
            except Exception as e:
                print(f"   ❌ 移动失败 {file_name}: {e}")
        else:
            print(f"   ⚠️  文件不存在: {file_name}")

    print(f"\n📊 移动了 {moved_count} 个文件到 scripts/ 目录")
    return moved_count

def create_missing_icons():
    """创建缺失的图标文件"""
    print("\n🎨 创建缺失的图标文件...")

    # 创建public目录（如果不存在）
    public_dir = Path('public')
    public_dir.mkdir(exist_ok=True)

    # 需要创建的图标文件
    icon_files = [
        'public/favicon.ico',
        'public/logo.svg',
        'public/logo.png',
        'public/icon-192x192.png',
        'public/icon-512x512.png'
    ]

    created_count = 0

    for icon_path in icon_files:
        icon_file = Path(icon_path)

        if icon_file.exists():
            print(f"   ✓ {icon_path} 已存在")
            continue

        # 创建目录
        icon_file.parent.mkdir(parents=True, exist_ok=True)

        # 根据文件类型创建不同的内容
        if icon_path.endswith('.svg'):
            create_svg_icon(icon_file)
        elif icon_path.endswith('.ico'):
            create_ico_placeholder(icon_file)
        elif icon_path.endswith('.png'):
            create_png_placeholder(icon_file)

        created_count += 1

    print(f"\n📊 创建了 {created_count} 个图标文件")
    return created_count

def create_svg_icon(file_path: Path):
    """创建SVG图标"""
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#3498db;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#2c3e50;stop-opacity:1" />
    </linearGradient>
  </defs>

  <!-- 背景圆形 -->
  <circle cx="32" cy="32" r="30" fill="url(#grad1)" stroke="#2c3e50" stroke-width="2"/>

  <!-- 盾牌形状 -->
  <path d="M32 8 L48 16 L48 32 Q48 48 32 56 Q16 48 16 32 L16 16 Z"
        fill="#ffffff" opacity="0.9"/>

  <!-- 内部图案 -->
  <circle cx="32" cy="28" r="6" fill="#3498db"/>
  <rect x="28" y="36" width="8" height="12" rx="2" fill="#3498db"/>

  <!-- 文字 -->
  <text x="32" y="52" text-anchor="middle" font-family="Arial, sans-serif"
        font-size="8" font-weight="bold" fill="#2c3e50">EDR</text>
</svg>'''

    file_path.write_text(svg_content, encoding='utf-8')
    print(f"   ✅ 创建SVG图标: {file_path}")

def create_ico_placeholder(file_path: Path):
    """创建ICO占位符（实际上创建一个简单的二进制文件）"""
    # 创建一个最小的ICO文件头
    ico_header = bytes([
        0x00, 0x00,  # Reserved
        0x01, 0x00,  # Type (1 = ICO)
        0x01, 0x00,  # Number of images
        0x10,        # Width (16px)
        0x10,        # Height (16px)
        0x00,        # Color count
        0x00,        # Reserved
        0x01, 0x00,  # Color planes
        0x20, 0x00,  # Bits per pixel
        0x68, 0x04, 0x00, 0x00,  # Size of image data
        0x16, 0x00, 0x00, 0x00   # Offset to image data
    ])

    # 简单的16x16像素数据（蓝色图标）
    pixel_data = bytes([0x42, 0x85, 0xf4, 0xff] * 256)  # BGRA格式

    with open(file_path, 'wb') as f:
        f.write(ico_header + pixel_data)

    print(f"   ✅ 创建ICO图标: {file_path}")

def create_png_placeholder(file_path: Path):
    """创建PNG占位符"""
    # 创建一个最小的PNG文件（1x1像素，蓝色）
    png_data = bytes([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,  # PNG signature
        0x00, 0x00, 0x00, 0x0D,  # IHDR chunk length
        0x49, 0x48, 0x44, 0x52,  # IHDR
        0x00, 0x00, 0x00, 0x01,  # Width: 1
        0x00, 0x00, 0x00, 0x01,  # Height: 1
        0x08, 0x02, 0x00, 0x00, 0x00,  # Bit depth, color type, etc.
        0x90, 0x77, 0x53, 0xDE,  # CRC
        0x00, 0x00, 0x00, 0x0C,  # IDAT chunk length
        0x49, 0x44, 0x41, 0x54,  # IDAT
        0x08, 0x99, 0x01, 0x01, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x02, 0x00, 0x01,  # Compressed data
        0x00, 0x00, 0x00, 0x00,  # IEND chunk length
        0x49, 0x45, 0x4E, 0x44,  # IEND
        0xAE, 0x42, 0x60, 0x82   # CRC
    ])

    with open(file_path, 'wb') as f:
        f.write(png_data)

    print(f"   ✅ 创建PNG图标: {file_path}")

def check_vue_icon_usage():
    """检查Vue文件中使用的图标"""
    print("\n🔍 检查Vue文件中的图标使用...")

    vue_files = list(Path('src').rglob('*.vue'))
    icon_usage = set()

    for vue_file in vue_files:
        try:
            content = vue_file.read_text(encoding='utf-8')

            # 查找Element Plus图标
            import re
            icon_matches = re.findall(r'<([A-Z][a-zA-Z]*)\s*/?>', content)
            icon_usage.update(icon_matches)

            # 查找component :is 使用的图标
            component_matches = re.findall(r':is="([^"]+)"', content)
            icon_usage.update(component_matches)

        except Exception as e:
            print(f"   ⚠️  读取文件失败 {vue_file}: {e}")

    print(f"   📊 发现 {len(icon_usage)} 个不同的图标:")
    for icon in sorted(icon_usage):
        if icon and len(icon) > 1:  # 过滤掉单字符
            print(f"      - {icon}")

    return icon_usage

def create_icon_components():
    """创建图标组件文件"""
    print("\n🎨 创建图标组件...")

    # 创建图标组件目录
    icons_dir = Path('src/components/icons')
    icons_dir.mkdir(parents=True, exist_ok=True)

    # 常用的图标列表
    common_icons = [
        'Dashboard', 'Alert', 'User', 'Setting', 'Document',
        'Search', 'Shield', 'Desktop', 'Crosshairs', 'Refresh',
        'ArrowDown', 'SwitchButton', 'FullScreen', 'Fold', 'Expand'
    ]

    created_count = 0

    for icon_name in common_icons:
        icon_file = icons_dir / f'{icon_name}.vue'

        if icon_file.exists():
            print(f"   ✓ {icon_name}.vue 已存在")
            continue

        # 创建图标组件
        icon_content = f'''<template>
  <svg
    viewBox="0 0 1024 1024"
    width="1em"
    height="1em"
    fill="currentColor"
    aria-hidden="true"
    focusable="false"
  >
    <!-- {icon_name} 图标 - 占位符 -->
    <path d="M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64z"/>
    <text x="512" y="550" text-anchor="middle" font-size="200" fill="white">{icon_name[0]}</text>
  </svg>
</template>

<script setup lang="ts">
// {icon_name} 图标组件
// 这是一个占位符图标，可以替换为实际的SVG路径
</script>'''

        icon_file.write_text(icon_content, encoding='utf-8')
        print(f"   ✅ 创建图标组件: {icon_name}.vue")
        created_count += 1

    # 创建图标索引文件
    index_file = icons_dir / 'index.ts'
    if not index_file.exists():
        index_content = f'''// 图标组件导出
{chr(10).join([f"export {{ default as {icon} }} from './{icon}.vue'" for icon in common_icons])}

// 图标映射
export const iconMap = {{
{chr(10).join([f"  {icon}: () => import('./{icon}.vue')," for icon in common_icons])}
}}
'''
        index_file.write_text(index_content, encoding='utf-8')
        print(f"   ✅ 创建图标索引: index.ts")
        created_count += 1

    print(f"\n📊 创建了 {created_count} 个图标组件")
    return created_count

def clean_root_directory():
    """清理根目录"""
    print("\n🧹 清理根目录...")

    # 需要删除的临时文件
    temp_files = [
        'organize_project.py',  # 这个脚本本身也会被移动
    ]

    cleaned_count = 0
    for file_name in temp_files:
        file_path = Path(file_name)
        if file_path.exists() and file_name != 'organize_project.py':  # 不删除正在运行的脚本
            try:
                file_path.unlink()
                print(f"   ✅ 删除: {file_name}")
                cleaned_count += 1
            except Exception as e:
                print(f"   ❌ 删除失败 {file_name}: {e}")

    print(f"\n📊 清理了 {cleaned_count} 个临时文件")
    return cleaned_count

def create_project_structure_doc():
    """创建项目结构文档"""
    print("\n📝 创建项目结构文档...")

    doc_content = '''# H-System EDR Frontend 项目结构

## 📁 目录结构

```
frontend/
├── public/                     # 静态资源
│   ├── favicon.ico            # 网站图标
│   ├── logo.svg               # SVG Logo
│   ├── logo.png               # PNG Logo
│   ├── icon-192x192.png       # PWA图标
│   └── icon-512x512.png       # PWA图标
├── src/                       # 源代码
│   ├── components/            # 组件
│   │   ├── icons/            # 图标组件
│   │   └── layout/           # 布局组件
│   │       └── MenuTree.vue  # 递归菜单组件
│   ├── layouts/              # 布局
│   │   └── MainLayout.vue    # 主布局
│   ├── views/                # 页面视图
│   │   ├── dashboard/        # 仪表板
│   │   ├── alerts/           # 告警管理
│   │   ├── assets/           # 资产管理
│   │   ├── hunting/          # 威胁狩猎
│   │   ├── intelligence/     # 威胁情报
│   │   ├── investigation/    # 事件调查
│   │   ├── reports/          # 报表分析
│   │   ├── system/           # 系统管理
│   │   │   ├── honeypot/     # 蜜罐策略中心
│   │   │   ├── user-permission/ # 用户与权限
│   │   │   └── maintenance/  # 系统维护
│   │   └── users/            # 用户管理
│   ├── router/               # 路由配置
│   ├── store/                # 状态管理
│   ├── api/                  # API接口
│   └── types/                # 类型定义
├── scripts/                  # 工具脚本
│   ├── test_*.py            # 测试脚本
│   ├── create_*.py          # 创建脚本
│   ├── *.html               # 测试页面
│   └── *.md                 # 文档
└── package.json             # 项目配置
```

## 🎨 图标系统

### 静态图标文件
- `public/favicon.ico` - 浏览器标签页图标
- `public/logo.svg` - 矢量Logo（推荐）
- `public/logo.png` - 位图Logo
- PWA图标用于移动端和桌面应用

### Vue图标组件
- `src/components/icons/` - 自定义图标组件
- 支持Element Plus图标系统
- 可扩展的图标映射

## 🔧 开发工具

### scripts/ 目录
- **测试脚本**: 用于验证功能和结构
- **创建脚本**: 用于生成代码和文件
- **调试工具**: 用于问题排查
- **文档**: 项目说明和使用指南

### 使用方法
```bash
# 运行测试脚本
cd scripts
python test_three_level_menu.py

# 查看调试信息
open debug_three_level_menu.md
```

## 🚀 部署说明

### 开发环境
```bash
npm run dev
```

### 生产构建
```bash
npm run build
```

### 图标优化
- SVG图标自动优化
- PNG图标压缩
- ICO图标多尺寸支持

## 📋 维护清单

### 定期检查
- [ ] 图标文件完整性
- [ ] 路由配置正确性
- [ ] 组件依赖关系
- [ ] 权限控制逻辑

### 更新流程
1. 修改源代码
2. 运行测试脚本验证
3. 更新文档
4. 提交代码

## 🎯 最佳实践

### 图标使用
- 优先使用SVG格式
- 保持图标风格一致
- 合理使用图标尺寸

### 组件开发
- 遵循Vue 3 Composition API
- 使用TypeScript类型检查
- 保持组件单一职责

### 目录管理
- 定期清理临时文件
- 保持目录结构清晰
- 及时更新文档
'''

    scripts_dir = Path('scripts')
    doc_file = scripts_dir / 'project_structure.md'
    doc_file.write_text(doc_content, encoding='utf-8')
    print(f"   ✅ 项目结构文档已保存到: scripts/project_structure.md")

def main():
    """主函数"""
    print("🔧 整理H-System EDR Frontend项目")
    print("=" * 50)

    # 切换到frontend目录
    os.chdir(Path(__file__).parent)

    # 1. 创建scripts目录并移动文件
    moved_files = create_scripts_directory()

    # 2. 创建缺失的图标
    created_icons = create_missing_icons()

    # 3. 检查Vue文件中的图标使用
    icon_usage = check_vue_icon_usage()

    # 4. 创建图标组件
    created_components = create_icon_components()

    # 5. 创建项目结构文档
    create_project_structure_doc()

    # 6. 清理根目录
    cleaned_files = clean_root_directory()

    print("\n🎉 项目整理完成！")
    print("\n📋 完成的工作:")
    print(f"   ✅ 移动了 {moved_files} 个文件到 scripts/ 目录")
    print(f"   ✅ 创建了 {created_icons} 个图标文件")
    print(f"   ✅ 创建了 {created_components} 个图标组件")
    print(f"   ✅ 发现了 {len(icon_usage)} 个图标使用")
    print(f"   ✅ 清理了 {cleaned_files} 个临时文件")

    print("\n📁 新的目录结构:")
    print("   📂 scripts/ - 所有测试和工具脚本")
    print("   📂 public/ - 静态图标文件")
    print("   📂 src/components/icons/ - Vue图标组件")
    print("   📄 scripts/project_structure.md - 完整项目结构说明")

    print("\n🚀 下一步:")
    print("   1. 检查图标是否正确显示")
    print("   2. 重启前端服务: npm run dev")
    print("   3. 验证所有功能正常")
    print("   4. 查看 scripts/project_structure.md 了解完整结构")

    # 最后移动这个脚本本身
    try:
        scripts_dir = Path('scripts')
        shutil.move('organize_project.py', str(scripts_dir / 'organize_project.py'))
        print(f"\n   ✅ 脚本已移动到: scripts/organize_project.py")
    except Exception as e:
        print(f"\n   ⚠️  脚本移动失败: {e}")

if __name__ == "__main__":
    main()