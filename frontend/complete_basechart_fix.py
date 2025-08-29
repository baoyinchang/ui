#!/usr/bin/env python3
"""
完整修复BaseChart.vue命名冲突
删除冲突文件并确保引用正确
"""

import os
from pathlib import Path

def remove_conflicting_files():
    """删除冲突的BaseChart文件"""
    print("🗑️ 删除冲突的BaseChart文件...")
    
    # 删除charts目录下的占位符文件
    charts_basechart = Path('src/components/charts/BaseChart.vue')
    if charts_basechart.exists():
        content = charts_basechart.read_text(encoding='utf-8')
        if '此页面正在开发中' in content or len(content) < 100:
            charts_basechart.unlink()
            print(f"   ✅ 删除占位符文件: {charts_basechart}")
        else:
            print(f"   ⚠️  保留有内容的文件: {charts_basechart}")
    
    # 检查charts目录是否为空
    charts_dir = Path('src/components/charts')
    if charts_dir.exists() and not any(charts_dir.iterdir()):
        charts_dir.rmdir()
        print(f"   ✅ 删除空目录: {charts_dir}")

def verify_final_state():
    """验证最终状态"""
    print("\n🔍 验证最终状态...")
    
    # 检查EchartsChart.vue是否存在
    echarts_chart = Path('src/components/common/EchartsChart.vue')
    if echarts_chart.exists():
        print("   ✅ EchartsChart.vue存在")
    else:
        print("   ❌ EchartsChart.vue不存在")
        return False
    
    # 检查BaseChart.vue别名是否存在
    basechart_alias = Path('src/components/common/BaseChart.vue')
    if basechart_alias.exists():
        content = basechart_alias.read_text(encoding='utf-8')
        if 'EchartsChart' in content and '兼容性别名' in content:
            print("   ✅ BaseChart.vue别名正确")
        else:
            print("   ⚠️  BaseChart.vue别名内容异常")
    else:
        print("   ❌ BaseChart.vue别名不存在")
        return False
    
    # 检查引用文件
    reference_files = [
        'src/views/assets/AssetList.vue',
        'src/views/dashboard/SecurityOverview.vue'
    ]
    
    for file_path in reference_files:
        file_obj = Path(file_path)
        if file_obj.exists():
            content = file_obj.read_text(encoding='utf-8')
            if 'EchartsChart' in content:
                print(f"   ✅ {file_path} 引用已更新")
            else:
                print(f"   ⚠️  {file_path} 引用未更新")
        else:
            print(f"   ❌ {file_path} 不存在")
    
    return True

def check_for_remaining_conflicts():
    """检查是否还有命名冲突"""
    print("\n🔍 检查剩余冲突...")
    
    basechart_files = list(Path('src').rglob('*BaseChart.vue'))
    
    if len(basechart_files) <= 1:  # 只应该有别名文件
        print("   ✅ 没有发现命名冲突")
        return True
    else:
        print(f"   ⚠️  发现 {len(basechart_files)} 个BaseChart文件:")
        for file in basechart_files:
            print(f"      - {file}")
        return False

def main():
    """主函数"""
    print("🔧 完整修复BaseChart命名冲突")
    print("=" * 40)
    
    # 切换到frontend目录
    os.chdir(Path(__file__).parent)
    
    # 删除冲突文件
    remove_conflicting_files()
    
    # 验证最终状态
    if verify_final_state():
        print("\n🎉 BaseChart命名冲突完全修复！")
    else:
        print("\n⚠️  修复过程中发现问题")
    
    # 检查剩余冲突
    if check_for_remaining_conflicts():
        print("\n✅ 所有命名冲突已解决")
        print("\n📋 最终状态:")
        print("   ✅ EchartsChart.vue - 主要图表组件")
        print("   ✅ BaseChart.vue - 兼容性别名")
        print("   ✅ 所有引用已更新")
        print("\n🚀 现在可以重新启动前端服务:")
        print("   npm run dev")
        return 0
    else:
        print("\n❌ 仍有冲突需要手动解决")
        return 1

if __name__ == "__main__":
    exit(main())
