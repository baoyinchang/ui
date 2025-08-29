#!/usr/bin/env python3
"""
修复主题存储引用问题
将所有 @/stores/theme 引用替换为 @/store/app
"""

import os
import re
from pathlib import Path

def find_theme_store_references():
    """查找所有主题存储引用"""
    print("🔍 查找主题存储引用...")
    
    references = []
    
    # 搜索所有Vue和TypeScript文件
    for pattern in ['**/*.vue', '**/*.ts', '**/*.js']:
        for file_path in Path('../src').rglob(pattern.replace('**/', '')):
            if file_path.is_file():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    
                    # 查找 @/stores/theme 引用
                    if '@/stores/theme' in content:
                        references.append({
                            'file': str(file_path),
                            'type': 'import_path',
                            'content': content
                        })
                    
                    # 查找 useThemeStore 引用
                    if 'useThemeStore' in content:
                        references.append({
                            'file': str(file_path),
                            'type': 'function_call',
                            'content': content
                        })
                    
                    # 查找 themeStore.isDark 引用
                    if 'themeStore.isDark' in content:
                        references.append({
                            'file': str(file_path),
                            'type': 'property_access',
                            'content': content
                        })
                        
                except Exception as e:
                    print(f"   ⚠️  读取文件失败: {file_path} - {e}")
    
    return references

def fix_theme_store_references():
    """修复主题存储引用"""
    print("\n🔧 修复主题存储引用...")
    
    fixed_files = []
    
    # 搜索并修复所有文件
    for pattern in ['**/*.vue', '**/*.ts', '**/*.js']:
        for file_path in Path('../src').rglob(pattern.replace('**/', '')):
            if file_path.is_file():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    original_content = content
                    
                    # 替换导入路径
                    content = content.replace(
                        "import { useThemeStore } from '@/stores/theme'",
                        "import { useAppStore } from '@/store/app'"
                    )
                    
                    # 替换函数调用
                    content = content.replace('useThemeStore()', 'useAppStore()')
                    content = content.replace('const themeStore = useThemeStore()', 'const appStore = useAppStore()')
                    
                    # 替换属性访问
                    content = content.replace('themeStore.isDark', "appStore.theme === 'dark'")
                    content = content.replace('(themeStore.isDark ? \'dark\' : \'light\')', 'appStore.theme')
                    
                    # 如果内容有变化，写回文件
                    if content != original_content:
                        file_path.write_text(content, encoding='utf-8')
                        fixed_files.append(str(file_path))
                        print(f"   ✅ 修复: {file_path}")
                        
                except Exception as e:
                    print(f"   ❌ 修复失败: {file_path} - {e}")
    
    return fixed_files

def verify_fixes():
    """验证修复结果"""
    print("\n✅ 验证修复结果...")
    
    # 检查是否还有未修复的引用
    remaining_refs = find_theme_store_references()
    
    if not remaining_refs:
        print("   ✅ 所有主题存储引用已修复")
        return True
    else:
        print(f"   ⚠️  仍有 {len(remaining_refs)} 个未修复的引用:")
        for ref in remaining_refs:
            print(f"      - {ref['file']} ({ref['type']})")
        return False

def check_app_store_usage():
    """检查app存储的使用情况"""
    print("\n📊 检查app存储使用情况...")
    
    app_store_files = []
    
    for pattern in ['**/*.vue', '**/*.ts', '**/*.js']:
        for file_path in Path('../src').rglob(pattern.replace('**/', '')):
            if file_path.is_file():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    
                    if 'useAppStore' in content and 'theme' in content:
                        app_store_files.append(str(file_path))
                        
                except Exception as e:
                    continue
    
    print(f"   📄 找到 {len(app_store_files)} 个使用app存储主题的文件:")
    for file in app_store_files:
        print(f"      - {file}")

def create_test_commands():
    """创建测试命令"""
    print("\n📋 创建测试命令...")
    
    test_commands = '''# 主题存储修复测试

## 🔧 修复内容

### 修复的问题
1. `@/stores/theme` 导入路径不存在
2. `useThemeStore` 函数不存在
3. `themeStore.isDark` 属性访问错误

### 修复方案
1. 将 `@/stores/theme` 替换为 `@/store/app`
2. 将 `useThemeStore()` 替换为 `useAppStore()`
3. 将 `themeStore.isDark` 替换为 `appStore.theme === 'dark'`
4. 将 `(themeStore.isDark ? 'dark' : 'light')` 替换为 `appStore.theme`

## 🚀 测试步骤

### 1. 重启前端服务
```bash
npm run dev
```

### 2. 检查控制台错误
- 打开浏览器开发者工具
- 查看Console标签页
- 确认没有主题存储相关的错误

### 3. 测试主题功能
在浏览器控制台运行：

```javascript
// 1. 检查app存储
const appStore = window.$pinia?.state?.value?.app
console.log('App Store:', appStore)
console.log('当前主题:', appStore?.theme)

// 2. 测试主题切换
if (appStore) {
    // 切换主题
    appStore.theme = appStore.theme === 'light' ? 'dark' : 'light'
    console.log('主题已切换为:', appStore.theme)
}

// 3. 检查图表组件
const charts = document.querySelectorAll('.echarts')
console.log('图表数量:', charts.length)
```

### 4. 访问安全态势页面
- 点击左侧菜单的"安全态势"
- 确认页面能正常加载
- 确认图表能正常显示

## ✅ 预期结果

### 控制台输出
- [ ] 没有 "Failed to resolve import @/stores/theme" 错误
- [ ] 没有 "useThemeStore is not defined" 错误
- [ ] 没有 "themeStore.isDark" 相关错误

### 页面功能
- [ ] 安全态势页面正常加载
- [ ] 图表组件正常显示
- [ ] 主题切换功能正常工作

### 组件状态
- [ ] EchartsChart组件正常工作
- [ ] BaseChart组件正常工作
- [ ] 所有图表都能正确应用主题

## 🔧 故障排除

### 如果仍有导入错误
1. 检查是否有遗漏的文件未修复
2. 清除浏览器缓存并刷新
3. 重启前端服务

### 如果主题不生效
1. 检查app存储是否正确初始化
2. 确认主题值是否正确传递给组件
3. 检查CSS样式是否正确应用

### 如果图表不显示
1. 检查echarts库是否正确加载
2. 确认图表数据是否正确
3. 检查图表容器是否存在

## 📞 获取帮助

如果问题仍然存在，请提供：
1. 浏览器控制台的完整错误信息
2. 网络请求的状态
3. 当前的主题设置
4. 前端服务的启动日志
'''
    
    test_file = Path('theme_store_fix_test.md')
    test_file.write_text(test_commands, encoding='utf-8')
    print(f"   ✅ 测试命令已保存到: {test_file}")

def main():
    """主函数"""
    print("🔧 修复主题存储引用问题")
    print("=" * 40)
    
    # 切换到scripts目录
    os.chdir(Path(__file__).parent)
    
    # 查找问题
    references = find_theme_store_references()
    if references:
        print(f"   📊 找到 {len(references)} 个需要修复的引用")
    else:
        print("   ✅ 没有找到需要修复的引用")
    
    # 执行修复
    fixed_files = fix_theme_store_references()
    
    # 验证修复结果
    success = verify_fixes()
    
    # 检查使用情况
    check_app_store_usage()
    
    # 创建测试命令
    create_test_commands()
    
    print("\n🎉 主题存储引用修复完成！")
    
    if success:
        print("\n✅ 修复成功！")
        print(f"\n📋 修复了 {len(fixed_files)} 个文件:")
        for file in fixed_files:
            print(f"   - {file}")
        
        print("\n🚀 现在可以:")
        print("   1. 重启前端服务: npm run dev")
        print("   2. 访问安全态势页面测试")
        print("   3. 使用 theme_store_fix_test.md 进行详细测试")
        
        print("\n🎯 预期效果:")
        print("   - 没有主题存储相关的错误")
        print("   - 图表组件正常工作")
        print("   - 主题切换功能正常")
        
    else:
        print("\n⚠️  修复可能不完整，请检查剩余的引用")

if __name__ == "__main__":
    main()
