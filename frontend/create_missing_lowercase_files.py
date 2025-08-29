#!/usr/bin/env python3
"""
创建缺失的小写Vue文件
基于路由配置创建实际需要的文件
"""

import os
from pathlib import Path

def create_vue_file(file_path: str, component_name: str, title: str):
    """创建单个Vue文件"""
    file_path_obj = Path(file_path)
    
    # 如果文件已存在，跳过
    if file_path_obj.exists():
        print(f"   ✓ {file_path} 已存在")
        return
    
    # 创建目录
    file_path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    # 生成Vue文件内容
    content = f'''<template>
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
    
    file_path_obj.write_text(content, encoding='utf-8')
    print(f"   ✅ 创建: {file_path}")

def create_missing_files():
    """创建所有缺失的文件"""
    print("📄 创建缺失的小写Vue文件...")
    
    # 需要创建的文件列表 (基于路由配置)
    files_to_create = [
        ("src/views/dashboard/index.vue", "Dashboard", "仪表板"),
        ("src/views/assets/index.vue", "Assets", "资产管理"),
        ("src/views/assets/detail.vue", "AssetDetail", "资产详情"),
        ("src/views/hunting/detail.vue", "HuntingDetail", "威胁狩猎详情"),
        ("src/views/intelligence/index.vue", "Intelligence", "威胁情报"),
        ("src/views/investigation/index.vue", "Investigation", "事件调查"),
        ("src/views/investigation/detail.vue", "InvestigationDetail", "调查详情"),
        ("src/views/reports/index.vue", "Reports", "报表分析"),
        ("src/views/system/index.vue", "System", "系统管理"),
    ]
    
    created_count = 0
    for file_path, component_name, title in files_to_create:
        if not Path(file_path).exists():
            create_vue_file(file_path, component_name, title)
            created_count += 1
        else:
            print(f"   ✓ {file_path} 已存在")
    
    print(f"\n🎉 创建了 {created_count} 个新文件")

def check_existing_files():
    """检查现有文件"""
    print("\n📁 检查现有文件结构...")
    
    # 检查各个目录
    directories = [
        "src/views/dashboard",
        "src/views/assets", 
        "src/views/hunting",
        "src/views/intelligence",
        "src/views/investigation",
        "src/views/reports",
        "src/views/system"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if dir_path.exists():
            files = list(dir_path.glob("*.vue"))
            print(f"   📂 {directory}: {len(files)} 个文件")
            for file in files:
                print(f"      - {file.name}")
        else:
            print(f"   📂 {directory}: 目录不存在")

def verify_all_routes():
    """验证所有路由文件是否存在"""
    print("\n🔍 验证路由文件...")
    
    # 从路由配置中提取的所有导入路径
    route_imports = [
        "src/views/auth/Login.vue",
        "src/views/dashboard/index.vue", 
        "src/views/alerts/Index.vue",
        "src/views/alerts/Detail.vue",
        "src/views/assets/index.vue",
        "src/views/assets/detail.vue",
        "src/views/hunting/index.vue",
        "src/views/hunting/detail.vue",
        "src/views/intelligence/index.vue",
        "src/views/investigation/index.vue",
        "src/views/investigation/detail.vue",
        "src/views/reports/index.vue",
        "src/views/system/index.vue",
        "src/views/users/Index.vue",
        "src/views/error/403.vue",
        "src/views/error/404.vue"
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in route_imports:
        file_obj = Path(file_path)
        if file_obj.exists():
            existing_files.append(file_path)
            print(f"   ✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"   ❌ {file_path}")
    
    print(f"\n📊 统计:")
    print(f"   ✅ 存在: {len(existing_files)} 个文件")
    print(f"   ❌ 缺失: {len(missing_files)} 个文件")
    
    if missing_files:
        print(f"\n⚠️  缺失的文件:")
        for file in missing_files:
            print(f"      - {file}")
        return False
    
    return True

def main():
    """主函数"""
    print("📄 创建缺失的小写Vue文件")
    print("=" * 40)
    
    # 切换到frontend目录
    os.chdir(Path(__file__).parent)
    
    # 检查现有文件
    check_existing_files()
    
    # 创建缺失文件
    create_missing_files()
    
    # 验证所有路由
    if verify_all_routes():
        print("\n🎉 所有路由文件都已存在！")
        print("\n现在可以启动开发服务器:")
        print("   npm run dev")
        return 0
    else:
        print("\n❌ 仍有文件缺失")
        return 1

if __name__ == "__main__":
    exit(main())
