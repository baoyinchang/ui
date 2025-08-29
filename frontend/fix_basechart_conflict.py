#!/usr/bin/env python3
"""
修复BaseChart.vue命名冲突问题
将BaseChart.vue重命名为EchartsChart.vue并更新所有引用
"""

import os
import re
from pathlib import Path

def find_basechart_references():
    """查找所有BaseChart的引用"""
    print("🔍 查找BaseChart引用...")
    
    references = []
    
    # 搜索所有Vue和TypeScript文件
    for pattern in ['**/*.vue', '**/*.ts', '**/*.js']:
        for file_path in Path('src').rglob(pattern.replace('**/', '')):
            if file_path.is_file():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    
                    # 查找import语句
                    import_matches = re.findall(r'import\s+.*BaseChart.*from\s+[\'"]([^\'"]+)[\'"]', content)
                    for match in import_matches:
                        references.append({
                            'file': str(file_path),
                            'type': 'import',
                            'line': match,
                            'content': content
                        })
                    
                    # 查找组件使用
                    if 'BaseChart' in content and file_path.suffix == '.vue':
                        references.append({
                            'file': str(file_path),
                            'type': 'usage',
                            'content': content
                        })
                        
                except Exception as e:
                    print(f"   ⚠️  读取文件失败: {file_path} - {e}")
    
    return references

def rename_basechart_file():
    """重命名BaseChart.vue文件"""
    print("\n📝 重命名BaseChart.vue文件...")
    
    old_path = Path('src/components/common/BaseChart.vue')
    new_path = Path('src/components/common/EchartsChart.vue')
    
    if old_path.exists():
        if new_path.exists():
            print(f"   ⚠️  目标文件已存在: {new_path}")
            # 备份现有文件
            backup_path = Path('src/components/common/EchartsChart.vue.backup')
            new_path.rename(backup_path)
            print(f"   📦 备份现有文件: {backup_path}")
        
        old_path.rename(new_path)
        print(f"   ✅ 重命名: {old_path} -> {new_path}")
        return True
    else:
        print(f"   ❌ 源文件不存在: {old_path}")
        return False

def update_file_references():
    """更新所有文件中的引用"""
    print("\n🔧 更新文件引用...")
    
    # 需要更新的文件
    files_to_update = [
        'src/views/assets/AssetList.vue',
        'src/views/dashboard/SecurityOverview.vue'
    ]
    
    updated_count = 0
    
    for file_path in files_to_update:
        file_obj = Path(file_path)
        if not file_obj.exists():
            print(f"   ❌ 文件不存在: {file_path}")
            continue
        
        try:
            content = file_obj.read_text(encoding='utf-8')
            original_content = content
            
            # 更新import语句
            content = re.sub(
                r'import\s+BaseChart\s+from\s+[\'"]@/components/common/BaseChart\.vue[\'"]',
                "import EchartsChart from '@/components/common/EchartsChart.vue'",
                content
            )
            
            # 更新组件使用（在template中）
            content = re.sub(r'<BaseChart\b', '<EchartsChart', content)
            content = re.sub(r'</BaseChart>', '</EchartsChart>', content)
            
            # 更新组件注册（在script中）
            content = re.sub(r'\bBaseChart\b', 'EchartsChart', content)
            
            if content != original_content:
                file_obj.write_text(content, encoding='utf-8')
                print(f"   ✅ 更新: {file_path}")
                updated_count += 1
            else:
                print(f"   ✓ 无需更新: {file_path}")
                
        except Exception as e:
            print(f"   ❌ 更新失败: {file_path} - {e}")
    
    return updated_count

def verify_updates():
    """验证更新结果"""
    print("\n🔍 验证更新结果...")
    
    # 检查新文件是否存在
    new_file = Path('src/components/common/EchartsChart.vue')
    if new_file.exists():
        print("   ✅ EchartsChart.vue文件存在")
    else:
        print("   ❌ EchartsChart.vue文件不存在")
        return False
    
    # 检查旧文件是否已删除
    old_file = Path('src/components/common/BaseChart.vue')
    if not old_file.exists():
        print("   ✅ BaseChart.vue文件已删除")
    else:
        print("   ⚠️  BaseChart.vue文件仍然存在")
    
    # 检查引用是否已更新
    references = find_basechart_references()
    if not references:
        print("   ✅ 没有发现BaseChart引用")
        return True
    else:
        print(f"   ⚠️  仍有 {len(references)} 个BaseChart引用")
        for ref in references:
            print(f"      - {ref['file']}")
        return False

def create_component_alias():
    """创建组件别名以保持向后兼容"""
    print("\n📝 创建组件别名...")
    
    alias_content = '''<!-- 
  BaseChart.vue - 兼容性别名
  实际组件已重命名为EchartsChart.vue
  此文件仅为保持向后兼容性
-->
<script setup lang="ts">
import EchartsChart from './EchartsChart.vue'

// 重新导出所有props和emits
defineOptions({
  name: 'BaseChart'
})

// 透传所有props
const props = defineProps<{
  option?: any
  width?: string
  height?: string
  loading?: boolean
  theme?: string
  autoResize?: boolean
}>()

// 透传所有emits
const emit = defineEmits<{
  chartReady: [chart: any]
  chartClick: [params: any]
  chartDblClick: [params: any]
}>()
</script>

<template>
  <EchartsChart
    v-bind="props"
    @chart-ready="emit('chartReady', $event)"
    @chart-click="emit('chartClick', $event)"
    @chart-dbl-click="emit('chartDblClick', $event)"
  />
</template>
'''
    
    alias_file = Path('src/components/common/BaseChart.vue')
    alias_file.write_text(alias_content, encoding='utf-8')
    print("   ✅ 创建BaseChart.vue别名文件")

def main():
    """主函数"""
    print("🔧 修复BaseChart.vue命名冲突")
    print("=" * 40)
    
    # 切换到frontend目录
    os.chdir(Path(__file__).parent)
    
    # 查找当前引用
    references = find_basechart_references()
    if references:
        print(f"   📊 找到 {len(references)} 个BaseChart引用")
        for ref in references[:5]:  # 只显示前5个
            print(f"      - {ref['file']}")
    
    # 重命名文件
    if not rename_basechart_file():
        print("\n❌ 文件重命名失败")
        return 1
    
    # 更新引用
    updated_count = update_file_references()
    print(f"\n📊 更新了 {updated_count} 个文件")
    
    # 创建兼容性别名
    create_component_alias()
    
    # 验证结果
    if verify_updates():
        print("\n🎉 BaseChart命名冲突修复完成！")
        print("\n📋 修改总结:")
        print("   ✅ BaseChart.vue -> EchartsChart.vue")
        print("   ✅ 更新了所有引用文件")
        print("   ✅ 创建了兼容性别名")
        print("\n💡 建议:")
        print("   - 新代码请使用 EchartsChart 组件")
        print("   - BaseChart 别名仅为兼容性保留")
        return 0
    else:
        print("\n⚠️  修复过程中发现问题，请检查")
        return 1

if __name__ == "__main__":
    exit(main())
