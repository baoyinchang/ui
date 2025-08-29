#!/usr/bin/env python3
"""
规范化Vue文件名
1. 检查路由配置中的小写文件是否存在
2. 如果只有大写文件存在，重命名为小写
3. 如果都不存在，创建小写文件
"""

import os
import re
from pathlib import Path

def extract_route_imports():
    """从路由配置中提取所有导入路径"""
    print("🔍 提取路由配置中的导入路径...")
    
    router_file = Path("src/router/index.ts")
    if not router_file.exists():
        print("   ❌ 路由文件不存在")
        return []
    
    content = router_file.read_text(encoding='utf-8')
    
    # 提取所有import路径
    import_pattern = r"import\(['\"](@/views/[^'\"]+\.vue)['\"]"
    imports = re.findall(import_pattern, content)
    
    # 转换为实际文件路径
    file_paths = []
    for import_path in imports:
        file_path = import_path.replace('@/', 'src/')
        file_paths.append(file_path)
    
    print(f"   📊 找到 {len(file_paths)} 个路由导入")
    return file_paths

def create_vue_file_content(component_name: str, title: str):
    """生成Vue文件内容"""
    return f'''<template>
  <div class="{component_name.lower()}-container">
    <div class="page-header">
      <h1 class="page-title">{title}</h1>
      <div class="page-actions">
        <el-button type="primary" @click="handleRefresh">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>
    
    <div class="page-content">
      <el-card>
        <div class="content-wrapper">
          <el-empty description="{title}功能正在开发中">
            <el-button type="primary" @click="handleAction">开始使用</el-button>
          </el-empty>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import {{ ref, onMounted }} from 'vue'
import {{ ElMessage }} from 'element-plus'
import {{ Refresh }} from '@element-plus/icons-vue'

// 页面状态
const loading = ref(false)

// 刷新页面数据
const handleRefresh = () => {{
  ElMessage.success('刷新成功')
}}

// 处理操作
const handleAction = () => {{
  ElMessage.info('{title}功能即将上线')
}}

// 组件挂载
onMounted(() => {{
  console.log('{component_name} 页面已加载')
}})
</script>

<style scoped>
.{component_name.lower()}-container {{
  padding: 20px;
}}

.page-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}}

.page-title {{
  font-size: 24px;
  font-weight: 500;
  color: #303133;
  margin: 0;
}}

.page-actions {{
  display: flex;
  gap: 12px;
}}

.page-content {{
  min-height: 400px;
}}

.content-wrapper {{
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}}
</style>'''

def get_component_info(file_path: str):
    """根据文件路径获取组件信息"""
    path_parts = file_path.split('/')
    
    # 提取模块名和文件名
    if len(path_parts) >= 3:
        module = path_parts[-2]  # 倒数第二个部分是模块名
        filename = path_parts[-1].replace('.vue', '')  # 最后一个部分是文件名
        
        # 生成组件名和标题
        if filename == 'index':
            component_name = module.capitalize()
            title_map = {
                'dashboard': '仪表板',
                'assets': '资产管理', 
                'hunting': '威胁狩猎',
                'intelligence': '威胁情报',
                'investigation': '事件调查',
                'reports': '报表分析',
                'system': '系统管理'
            }
            title = title_map.get(module, f'{module.capitalize()}管理')
        elif filename == 'detail':
            component_name = f'{module.capitalize()}Detail'
            title_map = {
                'assets': '资产详情',
                'hunting': '威胁狩猎详情', 
                'investigation': '调查详情'
            }
            title = title_map.get(module, f'{module.capitalize()}详情')
        else:
            component_name = f'{module.capitalize()}{filename.capitalize()}'
            title = f'{module.capitalize()} {filename.capitalize()}'
        
        return component_name, title
    
    return 'Component', '页面'

def normalize_vue_files():
    """规范化Vue文件"""
    print("\n📄 规范化Vue文件...")
    
    # 获取所有路由导入路径
    route_files = extract_route_imports()
    
    stats = {
        'existing': 0,
        'renamed': 0, 
        'created': 0,
        'errors': 0
    }
    
    for file_path in route_files:
        lowercase_file = Path(file_path)
        
        # 生成对应的大写文件路径
        if file_path.endswith('/index.vue'):
            uppercase_file = Path(file_path.replace('/index.vue', '/Index.vue'))
        elif file_path.endswith('/detail.vue'):
            uppercase_file = Path(file_path.replace('/detail.vue', '/Detail.vue'))
        else:
            uppercase_file = None
        
        print(f"\n   🔍 处理: {file_path}")
        
        try:
            if lowercase_file.exists():
                # 小写文件已存在
                print(f"      ✅ 小写文件已存在")
                stats['existing'] += 1
                
                # 如果大写文件也存在，删除大写文件
                if uppercase_file and uppercase_file.exists():
                    uppercase_file.unlink()
                    print(f"      🗑️  删除重复的大写文件: {uppercase_file}")
                    
            elif uppercase_file and uppercase_file.exists():
                # 只有大写文件存在，重命名为小写
                lowercase_file.parent.mkdir(parents=True, exist_ok=True)
                uppercase_file.rename(lowercase_file)
                print(f"      📝 重命名: {uppercase_file} -> {lowercase_file}")
                stats['renamed'] += 1
                
            else:
                # 都不存在，创建小写文件
                lowercase_file.parent.mkdir(parents=True, exist_ok=True)
                
                # 获取组件信息
                component_name, title = get_component_info(file_path)
                
                # 创建文件内容
                content = create_vue_file_content(component_name, title)
                lowercase_file.write_text(content, encoding='utf-8')
                
                print(f"      ✨ 创建新文件: {lowercase_file}")
                print(f"         组件: {component_name}, 标题: {title}")
                stats['created'] += 1
                
        except Exception as e:
            print(f"      ❌ 处理失败: {e}")
            stats['errors'] += 1
    
    # 输出统计信息
    print(f"\n📊 处理统计:")
    print(f"   ✅ 已存在: {stats['existing']} 个")
    print(f"   📝 重命名: {stats['renamed']} 个") 
    print(f"   ✨ 新创建: {stats['created']} 个")
    print(f"   ❌ 错误: {stats['errors']} 个")
    
    return stats['errors'] == 0

def verify_all_files():
    """验证所有文件是否存在"""
    print("\n🔍 验证所有路由文件...")
    
    route_files = extract_route_imports()
    
    missing_files = []
    for file_path in route_files:
        file_obj = Path(file_path)
        if file_obj.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  仍有 {len(missing_files)} 个文件缺失")
        return False
    else:
        print(f"\n🎉 所有 {len(route_files)} 个路由文件都存在！")
        return True

def main():
    """主函数"""
    print("📄 规范化Vue文件名")
    print("=" * 40)
    
    # 切换到frontend目录
    os.chdir(Path(__file__).parent)
    
    # 规范化文件
    if not normalize_vue_files():
        print("\n❌ 处理过程中出现错误")
        return 1
    
    # 验证结果
    if verify_all_files():
        print("\n🎉 所有文件规范化完成！")
        print("\n现在可以启动开发服务器:")
        print("   npm run dev")
        return 0
    else:
        print("\n❌ 仍有文件问题")
        return 1

if __name__ == "__main__":
    exit(main())
