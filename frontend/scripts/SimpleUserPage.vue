<template>
  <div class="users-container">
    <div class="page-header">
      <h1>用户管理</h1>
      <p>开发模式 - 使用模拟数据</p>
    </div>
    
    <el-card>
      <div v-if="loading" style="text-align: center; padding: 40px;">
        <el-icon class="is-loading"><Loading /></el-icon>
        <p>加载中...</p>
      </div>
      
      <div v-else>
        <el-table :data="users" style="width: 100%">
          <el-table-column prop="username" label="用户名" />
          <el-table-column prop="email" label="邮箱" />
          <el-table-column prop="full_name" label="姓名" />
          <el-table-column prop="role" label="角色" />
          <el-table-column prop="is_active" label="状态">
            <template #default="{ row }">
              <el-tag :type="row.is_active ? 'success' : 'danger'">
                {{ row.is_active ? '活跃' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Loading } from '@element-plus/icons-vue'

const loading = ref(true)
const users = ref([])

// 模拟数据
const mockUsers = [
  {
    id: 1,
    username: 'admin',
    email: 'admin@hsystem.com',
    full_name: '系统管理员',
    role: 'admin',
    is_active: true
  },
  {
    id: 2,
    username: 'analyst',
    email: 'analyst@hsystem.com',
    full_name: '安全分析师',
    role: 'analyst',
    is_active: true
  },
  {
    id: 3,
    username: 'operator',
    email: 'operator@hsystem.com',
    full_name: '安全运维',
    role: 'operator',
    is_active: true
  }
]

onMounted(async () => {
  console.log('🔧 简化版用户管理页面加载')
  
  // 模拟加载延迟
  setTimeout(() => {
    users.value = mockUsers
    loading.value = false
    console.log('✅ 用户数据加载完成')
  }, 1000)
})
</script>

<style scoped>
.users-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: #303133;
}

.page-header p {
  margin: 0;
  color: #909399;
}
</style>