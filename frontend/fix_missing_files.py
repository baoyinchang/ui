#!/usr/bin/env python3
"""
修复缺失文件脚本
创建所有路由中引用但不存在的Vue文件和样式文件
"""

import os
from pathlib import Path

def create_missing_scss_files():
    """创建缺失的SCSS文件"""
    print("🎨 创建缺失的SCSS文件...")
    
    # 创建styles目录
    styles_dir = Path("src/styles")
    styles_dir.mkdir(exist_ok=True)
    
    # 创建mixins.scss
    mixins_file = styles_dir / "mixins.scss"
    mixins_content = '''/**
 * SCSS Mixins - 常用的样式混合器
 */

// 清除浮动
@mixin clearfix {
  &::after {
    content: "";
    display: table;
    clear: both;
  }
}

// 文本省略号
@mixin text-ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

// 多行文本省略号
@mixin text-ellipsis-multiline($lines: 2) {
  display: -webkit-box;
  -webkit-line-clamp: $lines;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

// 居中对齐
@mixin center-flex {
  display: flex;
  align-items: center;
  justify-content: center;
}

// 绝对居中
@mixin absolute-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

// 响应式断点
@mixin mobile {
  @media (max-width: 768px) {
    @content;
  }
}

@mixin tablet {
  @media (min-width: 769px) and (max-width: 1024px) {
    @content;
  }
}

@mixin desktop {
  @media (min-width: 1025px) {
    @content;
  }
}

// 卡片样式
@mixin card-style {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

// 按钮样式
@mixin button-style($bg-color: #409eff, $text-color: white) {
  background-color: $bg-color;
  color: $text-color;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    opacity: 0.8;
  }
  
  &:active {
    transform: translateY(1px);
  }
}

// 输入框样式
@mixin input-style {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 14px;
  transition: border-color 0.3s ease;
  
  &:focus {
    border-color: #409eff;
    outline: none;
  }
}

// 表格样式
@mixin table-style {
  width: 100%;
  border-collapse: collapse;
  
  th, td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ebeef5;
  }
  
  th {
    background-color: #f5f7fa;
    font-weight: 500;
  }
  
  tr:hover {
    background-color: #f5f7fa;
  }
}

// 加载动画
@mixin loading-spinner {
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  animation: spin 1s linear infinite;
}

// 渐入动画
@mixin fade-in($duration: 0.3s) {
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  animation: fadeIn $duration ease-in-out;
}

// 滑入动画
@mixin slide-in-up($duration: 0.3s) {
  @keyframes slideInUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  animation: slideInUp $duration ease-out;
}'''
    
    mixins_file.write_text(mixins_content, encoding='utf-8')
    print(f"   ✅ 创建: {mixins_file}")
    
    # 创建index.scss
    index_scss = styles_dir / "index.scss"
    index_content = '''/**
 * 全局样式文件
 */

@use "mixins.scss" as *;
@use "@/assets/css/variables.scss" as *;

// 全局重置样式
* {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 14px;
  line-height: 1.5;
  color: $text-color-primary;
  background-color: $background-color-base;
}

// 通用类
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.flex { display: flex; }
.flex-center { @include center-flex; }
.flex-column { flex-direction: column; }
.flex-wrap { flex-wrap: wrap; }

.mt-10 { margin-top: 10px; }
.mt-20 { margin-top: 20px; }
.mb-10 { margin-bottom: 10px; }
.mb-20 { margin-bottom: 20px; }

.p-10 { padding: 10px; }
.p-20 { padding: 20px; }

// 页面容器
.page-container {
  padding: 20px;
  min-height: calc(100vh - 60px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid $border-color-light;
}

.page-title {
  font-size: 24px;
  font-weight: 500;
  color: $text-color-primary;
  margin: 0;
}

.page-content {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

// 卡片样式
.card {
  @include card-style;
}

// 按钮样式
.btn {
  @include button-style;
}

.btn-primary {
  @include button-style($primary-color, white);
}

.btn-success {
  @include button-style($success-color, white);
}

.btn-warning {
  @include button-style($warning-color, white);
}

.btn-danger {
  @include button-style($danger-color, white);
}

// 表单样式
.form-item {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  margin-bottom: 4px;
  font-weight: 500;
  color: $text-color-regular;
}

.form-input {
  @include input-style;
  width: 100%;
}

// 表格样式
.table {
  @include table-style;
}

// 工具类
.loading {
  @include loading-spinner;
}

.fade-in {
  @include fade-in;
}

.slide-in-up {
  @include slide-in-up;
}

// 响应式
@include mobile {
  .page-container {
    padding: 10px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}'''
    
    index_scss.write_text(index_content, encoding='utf-8')
    print(f"   ✅ 创建: {index_scss}")

def create_missing_vue_files():
    """创建缺失的Vue文件"""
    print("\n📄 创建缺失的Vue文件...")
    
    # 需要创建的文件列表
    vue_files = [
        ("src/views/dashboard/Index.vue", "Dashboard", "仪表板"),
        ("src/views/assets/Index.vue", "Assets", "资产管理"),
        ("src/views/assets/Detail.vue", "AssetDetail", "资产详情"),
        ("src/views/hunting/Detail.vue", "HuntingDetail", "威胁狩猎详情"),
        ("src/views/intelligence/Index.vue", "Intelligence", "威胁情报"),
        ("src/views/investigation/Index.vue", "Investigation", "事件调查"),
        ("src/views/investigation/Detail.vue", "InvestigationDetail", "调查详情"),
        ("src/views/reports/Index.vue", "Reports", "报表分析"),
        ("src/views/system/Index.vue", "System", "系统管理"),
    ]
    
    for file_path, component_name, title in vue_files:
        create_vue_file(file_path, component_name, title)

def create_vue_file(file_path: str, component_name: str, title: str):
    """创建单个Vue文件"""
    file_path_obj = Path(file_path)
    
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

def main():
    """主函数"""
    print("🔧 修复缺失文件")
    print("=" * 40)
    
    # 切换到frontend目录
    os.chdir(Path(__file__).parent)
    
    # 创建缺失的SCSS文件
    create_missing_scss_files()
    
    # 创建缺失的Vue文件
    create_missing_vue_files()
    
    print("\n🎉 所有缺失文件已创建完成！")
    print("\n现在可以重新启动开发服务器:")
    print("   npm run dev")
    print("   或者 ./start.sh")

if __name__ == "__main__":
    main()
