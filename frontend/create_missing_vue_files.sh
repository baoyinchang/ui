#!/bin/bash

# 创建缺失的Vue文件脚本
# 专门用于Ubuntu环境

set -e

echo "📄 创建缺失的Vue文件"
echo "===================="

# 创建dashboard/Index.vue
echo "创建 src/views/dashboard/Index.vue..."
mkdir -p src/views/dashboard
cat > src/views/dashboard/Index.vue << 'EOF'
<template>
  <div class="dashboard-container">
    <div class="page-header">
      <h1 class="page-title">仪表板</h1>
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
          <el-empty description="仪表板功能正在开发中">
            <el-button type="primary" @click="handleAction">开始使用</el-button>
          </el-empty>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'

// 页面状态
const loading = ref(false)

// 刷新页面数据
const handleRefresh = () => {
  ElMessage.success('刷新成功')
}

// 处理操作
const handleAction = () => {
  ElMessage.info('仪表板功能即将上线')
}

// 组件挂载
onMounted(() => {
  console.log('Dashboard 页面已加载')
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 500;
  color: #303133;
  margin: 0;
}

.page-actions {
  display: flex;
  gap: 12px;
}

.page-content {
  min-height: 400px;
}

.content-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}
</style>
EOF
echo "✅ dashboard/Index.vue 创建完成"

# 创建assets/Index.vue
echo "创建 src/views/assets/Index.vue..."
mkdir -p src/views/assets
cat > src/views/assets/Index.vue << 'EOF'
<template>
  <div class="assets-container">
    <div class="page-header">
      <h1 class="page-title">资产管理</h1>
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
          <el-empty description="资产管理功能正在开发中">
            <el-button type="primary" @click="handleAction">开始使用</el-button>
          </el-empty>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'

// 页面状态
const loading = ref(false)

// 刷新页面数据
const handleRefresh = () => {
  ElMessage.success('刷新成功')
}

// 处理操作
const handleAction = () => {
  ElMessage.info('资产管理功能即将上线')
}

// 组件挂载
onMounted(() => {
  console.log('Assets 页面已加载')
})
</script>

<style scoped>
.assets-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 500;
  color: #303133;
  margin: 0;
}

.page-actions {
  display: flex;
  gap: 12px;
}

.page-content {
  min-height: 400px;
}

.content-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}
</style>
EOF
echo "✅ assets/Index.vue 创建完成"

# 创建intelligence/Index.vue
echo "创建 src/views/intelligence/Index.vue..."
mkdir -p src/views/intelligence
cat > src/views/intelligence/Index.vue << 'EOF'
<template>
  <div class="intelligence-container">
    <div class="page-header">
      <h1 class="page-title">威胁情报</h1>
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
          <el-empty description="威胁情报功能正在开发中">
            <el-button type="primary" @click="handleAction">开始使用</el-button>
          </el-empty>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'

// 页面状态
const loading = ref(false)

// 刷新页面数据
const handleRefresh = () => {
  ElMessage.success('刷新成功')
}

// 处理操作
const handleAction = () => {
  ElMessage.info('威胁情报功能即将上线')
}

// 组件挂载
onMounted(() => {
  console.log('Intelligence 页面已加载')
})
</script>

<style scoped>
.intelligence-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 500;
  color: #303133;
  margin: 0;
}

.page-actions {
  display: flex;
  gap: 12px;
}

.page-content {
  min-height: 400px;
}

.content-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}
</style>
EOF
echo "✅ intelligence/Index.vue 创建完成"

# 创建investigation/Index.vue
echo "创建 src/views/investigation/Index.vue..."
mkdir -p src/views/investigation
cat > src/views/investigation/Index.vue << 'EOF'
<template>
  <div class="investigation-container">
    <div class="page-header">
      <h1 class="page-title">事件调查</h1>
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
          <el-empty description="事件调查功能正在开发中">
            <el-button type="primary" @click="handleAction">开始使用</el-button>
          </el-empty>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'

// 页面状态
const loading = ref(false)

// 刷新页面数据
const handleRefresh = () => {
  ElMessage.success('刷新成功')
}

// 处理操作
const handleAction = () => {
  ElMessage.info('事件调查功能即将上线')
}

// 组件挂载
onMounted(() => {
  console.log('Investigation 页面已加载')
})
</script>

<style scoped>
.investigation-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 500;
  color: #303133;
  margin: 0;
}

.page-actions {
  display: flex;
  gap: 12px;
}

.page-content {
  min-height: 400px;
}

.content-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}
</style>
EOF
echo "✅ investigation/Index.vue 创建完成"

# 创建reports/Index.vue
echo "创建 src/views/reports/Index.vue..."
mkdir -p src/views/reports
cat > src/views/reports/Index.vue << 'EOF'
<template>
  <div class="reports-container">
    <div class="page-header">
      <h1 class="page-title">报表分析</h1>
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
          <el-empty description="报表分析功能正在开发中">
            <el-button type="primary" @click="handleAction">开始使用</el-button>
          </el-empty>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'

// 页面状态
const loading = ref(false)

// 刷新页面数据
const handleRefresh = () => {
  ElMessage.success('刷新成功')
}

// 处理操作
const handleAction = () => {
  ElMessage.info('报表分析功能即将上线')
}

// 组件挂载
onMounted(() => {
  console.log('Reports 页面已加载')
})
</script>

<style scoped>
.reports-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 500;
  color: #303133;
  margin: 0;
}

.page-actions {
  display: flex;
  gap: 12px;
}

.page-content {
  min-height: 400px;
}

.content-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}
</style>
EOF
echo "✅ reports/Index.vue 创建完成"

# 创建system/Index.vue
echo "创建 src/views/system/Index.vue..."
mkdir -p src/views/system
cat > src/views/system/Index.vue << 'EOF'
<template>
  <div class="system-container">
    <div class="page-header">
      <h1 class="page-title">系统管理</h1>
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
          <el-empty description="系统管理功能正在开发中">
            <el-button type="primary" @click="handleAction">开始使用</el-button>
          </el-empty>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'

// 页面状态
const loading = ref(false)

// 刷新页面数据
const handleRefresh = () => {
  ElMessage.success('刷新成功')
}

// 处理操作
const handleAction = () => {
  ElMessage.info('系统管理功能即将上线')
}

// 组件挂载
onMounted(() => {
  console.log('System 页面已加载')
})
</script>

<style scoped>
.system-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 500;
  color: #303133;
  margin: 0;
}

.page-actions {
  display: flex;
  gap: 12px;
}

.page-content {
  min-height: 400px;
}

.content-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}
</style>
EOF
echo "✅ system/Index.vue 创建完成"

echo ""
echo "🎉 所有缺失的Vue文件已创建完成！"
echo ""
echo "现在可以重新验证:"
echo "   python3 verify_setup.py"
echo ""
echo "或者直接启动开发服务器:"
echo "   npm run dev"
