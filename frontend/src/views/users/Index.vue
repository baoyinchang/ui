<template>
  <div class="users-container">
    <div class="page-header">
      <h1 class="page-title">用户管理</h1>
      <p class="page-description">管理系统用户账户和权限，控制访问级别</p>
    </div>

    <!-- 用户统计 -->
    <div class="stats-grid">
      <div class="stat-card" v-for="stat in userStats" :key="stat.key">
        <div class="stat-icon" :class="stat.iconClass">
          <el-icon><component :is="stat.icon" /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-title">{{ stat.title }}</div>
          <div class="stat-value">{{ stat.value }}</div>
        </div>
      </div>
    </div>

    <!-- 搜索和过滤 -->
    <el-card class="filter-card" shadow="never">
      <el-form :model="searchForm" inline>
        <el-form-item label="搜索">
          <el-input
            v-model="searchForm.search"
            placeholder="搜索用户名或邮箱"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="角色">
          <el-select
            v-model="searchForm.role"
            placeholder="全部"
            clearable
            style="width: 120px"
          >
            <el-option label="管理员" value="admin" />
            <el-option label="分析师" value="analyst" />
            <el-option label="运维" value="operator" />
            <el-option label="查看者" value="viewer" />
          </el-select>
        </el-form-item>

        <el-form-item label="状态">
          <el-select
            v-model="searchForm.is_active"
            placeholder="全部"
            clearable
            style="width: 100px"
          >
            <el-option label="启用" :value="true" />
            <el-option label="禁用" :value="false" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 用户列表 -->
    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>用户列表</span>
          <div class="header-actions">
            <el-button
              type="primary"
              :disabled="selectedUsers.length === 0"
              @click="showBatchDialog"
            >
              批量操作 ({{ selectedUsers.length }})
            </el-button>
            <el-button type="primary" @click="showAddDialog">
              <el-icon><Plus /></el-icon>
              添加用户
            </el-button>
            <el-button @click="refreshData">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="userList"
        @selection-change="handleSelectionChange"
        stripe
        style="width: 100%"
      >
        <el-table-column type="selection" width="55" />

        <el-table-column prop="username" label="用户名" min-width="120">
          <template #default="{ row }">
            <div class="user-info">
              <el-avatar :size="32" :src="row.avatar">
                {{ row.username.charAt(0).toUpperCase() }}
              </el-avatar>
              <div class="user-details">
                <div class="username">{{ row.username }}</div>
                <div class="user-id">ID: {{ row.id }}</div>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="email" label="邮箱" min-width="180">
          <template #default="{ row }">
            <el-link type="primary" :href="`mailto:${row.email}`">
              {{ row.email }}
            </el-link>
          </template>
        </el-table-column>

        <el-table-column prop="role" label="角色" width="120">
          <template #default="{ row }">
            <el-tag :type="getRoleType(row.role)" size="small">
              {{ getRoleText(row.role) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="last_login" label="最后登录" width="180">
          <template #default="{ row }">
            {{ row.last_login ? formatTime(row.last_login) : '从未登录' }}
          </template>
        </el-table-column>

        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="editUser(row)">
              编辑
            </el-button>
            <el-dropdown @command="(command) => handleAction(command, row)">
              <el-button size="small">
                更多
                <el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="resetPassword">重置密码</el-dropdown-item>
                  <el-dropdown-item
                    :command="row.is_active ? 'disable' : 'enable'"
                  >
                    {{ row.is_active ? '禁用用户' : '启用用户' }}
                  </el-dropdown-item>
                  <el-dropdown-item command="delete" class="danger-item">
                    删除用户
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 添加/编辑用户对话框 -->
    <el-dialog
      v-model="userDialogVisible"
      :title="isEdit ? '编辑用户' : '添加用户'"
      width="600px"
    >
      <el-form
        ref="userFormRef"
        :model="userForm"
        :rules="userFormRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="userForm.username"
            :disabled="isEdit"
            placeholder="请输入用户名"
          />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="userForm.email"
            placeholder="请输入邮箱地址"
          />
        </el-form-item>

        <el-form-item label="真实姓名">
          <el-input
            v-model="userForm.full_name"
            placeholder="请输入真实姓名（可选）"
          />
        </el-form-item>

        <el-form-item v-if="!isEdit" label="密码" prop="password">
          <el-input
            v-model="userForm.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>

        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" placeholder="请选择角色">
            <el-option label="系统管理员" value="admin" />
            <el-option label="安全分析师" value="analyst" />
            <el-option label="安全运维" value="operator" />
            <el-option label="只读用户" value="viewer" />
          </el-select>
        </el-form-item>

        <el-form-item label="状态">
          <el-switch
            v-model="userForm.is_active"
            active-text="启用"
            inactive-text="禁用"
          />
        </el-form-item>

        <el-form-item label="备注">
          <el-input
            v-model="userForm.notes"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息（可选）"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="userDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          :loading="userFormLoading"
          @click="handleUserSubmit"
        >
          {{ isEdit ? '更新' : '创建' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 批量操作对话框 -->
    <el-dialog
      v-model="batchDialogVisible"
      title="批量操作"
      width="500px"
    >
      <el-form :model="batchForm" label-width="100px">
        <el-form-item label="操作类型">
          <el-select v-model="batchForm.action" placeholder="请选择操作">
            <el-option label="启用用户" value="enable" />
            <el-option label="禁用用户" value="disable" />
            <el-option label="删除用户" value="delete" />
          </el-select>
        </el-form-item>

        <el-form-item label="确认操作">
          <el-alert
            :title="`将对 ${selectedUsers.length} 个用户执行${getBatchActionText(batchForm.action)}操作`"
            type="warning"
            show-icon
            :closable="false"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="batchDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          :loading="batchLoading"
          @click="handleBatchSubmit"
        >
          确定执行
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Search,
  Refresh,
  ArrowDown,
  User as UserIcon,
  UserFilled,
  Warning,
  CheckCircle
} from '@element-plus/icons-vue'
import { usersApi } from '@/api/usersWrapper'
import { USER_ROLE_LABELS } from '@/utils/constants'
import { formatTime } from '@/utils'
import type { User, PaginatedResponse } from '@/types/api'

// 数据状态
const loading = ref(false)
const userList = ref<User[]>([])
const selectedUsers = ref<User[]>([])

// 用户统计
const userStatistics = ref({
  total: 0,
  active: 0,
  inactive: 0,
  admins: 0
})

// 搜索表单
const searchForm = reactive({
  search: '',
  role: '',
  is_active: undefined as boolean | undefined
})

// 分页
const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 用户表单
const userDialogVisible = ref(false)
const userFormLoading = ref(false)
const userFormRef = ref()
const isEdit = ref(false)
const userForm = reactive({
  id: 0,
  username: '',
  email: '',
  full_name: '',
  password: '',
  role: 'analyst',
  is_active: true,
  notes: ''
})

const userFormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码长度不能少于8位', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
}

// 批量操作
const batchDialogVisible = ref(false)
const batchLoading = ref(false)
const batchForm = reactive({
  action: ''
})

// 统计数据
const userStats = computed(() => [
  {
    key: 'total',
    title: '总用户数',
    value: userStatistics.value.total,
    icon: UserIcon,
    iconClass: 'primary'
  },
  {
    key: 'active',
    title: '活跃用户',
    value: userStatistics.value.active,
    icon: CheckCircle,
    iconClass: 'success'
  },
  {
    key: 'inactive',
    title: '禁用用户',
    value: userStatistics.value.inactive,
    icon: Warning,
    iconClass: 'warning'
  },
  {
    key: 'admins',
    title: '管理员',
    value: userStatistics.value.admins,
    icon: UserFilled,
    iconClass: 'danger'
  }
])

// 检查是否为开发模式且禁用认证
const isDevelopmentMode = import.meta.env.VITE_ENABLE_AUTH !== 'true'

// 模拟数据
const mockUsers: User[] = [
  {
    id: 1,
    username: 'admin',
    email: 'admin@hsystem.com',
    full_name: '系统管理员',
    role: 'admin',
    is_active: true,
    avatar: '',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
    last_login: '2024-01-15T10:30:00Z',
    notes: '系统默认管理员账户'
  },
  {
    id: 2,
    username: 'analyst',
    email: 'analyst@hsystem.com',
    full_name: '安全分析师',
    role: 'analyst',
    is_active: true,
    avatar: '',
    created_at: '2024-01-02T00:00:00Z',
    updated_at: '2024-01-02T00:00:00Z',
    last_login: '2024-01-15T09:15:00Z',
    notes: '负责威胁分析和事件响应'
  },
  {
    id: 3,
    username: 'operator',
    email: 'operator@hsystem.com',
    full_name: '安全运维',
    role: 'operator',
    is_active: true,
    avatar: '',
    created_at: '2024-01-03T00:00:00Z',
    updated_at: '2024-01-03T00:00:00Z',
    last_login: '2024-01-14T16:45:00Z',
    notes: '负责系统运维和监控'
  },
  {
    id: 4,
    username: 'viewer',
    email: 'viewer@hsystem.com',
    full_name: '只读用户',
    role: 'viewer',
    is_active: false,
    avatar: '',
    created_at: '2024-01-04T00:00:00Z',
    updated_at: '2024-01-04T00:00:00Z',
    last_login: '2024-01-10T14:20:00Z',
    notes: '只读权限用户'
  }
]

const mockStatistics = {
  total: 4,
  active: 3,
  inactive: 1,
  admins: 1
}

// 初始化
onMounted(() => {
  loadData()
  loadStatistics()
})

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    if (isDevelopmentMode) {
      // 开发模式使用模拟数据
      console.log('🔧 开发模式：使用模拟用户数据')

      // 模拟网络延迟
      await new Promise(resolve => setTimeout(resolve, 500))

      // 应用搜索过滤
      let filteredUsers = [...mockUsers]

      if (searchForm.search) {
        filteredUsers = filteredUsers.filter(user =>
          user.username.includes(searchForm.search) ||
          user.email.includes(searchForm.search) ||
          user.full_name?.includes(searchForm.search)
        )
      }

      if (searchForm.role) {
        filteredUsers = filteredUsers.filter(user => user.role === searchForm.role)
      }

      if (searchForm.is_active !== undefined) {
        filteredUsers = filteredUsers.filter(user => user.is_active === searchForm.is_active)
      }

      // 分页处理
      const start = (pagination.page - 1) * pagination.size
      const end = start + pagination.size
      const paginatedUsers = filteredUsers.slice(start, end)

      userList.value = paginatedUsers
      pagination.total = filteredUsers.length
    } else {
      // 生产模式使用真实API
      const params = {
        page: pagination.page,
        size: pagination.size,
        ...searchForm
      }

      const response: PaginatedResponse<User> = await usersApi.getUsers(params)
      userList.value = response.items
      pagination.total = response.total
    }
  } catch (error) {
    console.error('加载用户列表失败:', error)
    ElMessage.error('加载用户列表失败')
  } finally {
    loading.value = false
  }
}

// 加载统计数据
const loadStatistics = async () => {
  try {
    if (isDevelopmentMode) {
      // 开发模式使用模拟数据
      console.log('🔧 开发模式：使用模拟统计数据')

      // 模拟网络延迟
      await new Promise(resolve => setTimeout(resolve, 300))

      userStatistics.value = mockStatistics
    } else {
      // 生产模式使用真实API
      const stats = await usersApi.getUserStatistics()
      userStatistics.value = stats
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

// 搜索和操作方法
const handleSearch = () => {
  pagination.page = 1
  loadData()
}

const handleReset = () => {
  Object.assign(searchForm, {
    search: '',
    role: '',
    is_active: undefined
  })
  pagination.page = 1
  loadData()
}

const refreshData = () => {
  loadData()
  loadStatistics()
}

const handleSizeChange = (size: number) => {
  pagination.size = size
  pagination.page = 1
  loadData()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  loadData()
}

const handleSelectionChange = (selection: User[]) => {
  selectedUsers.value = selection
}

// 工具函数
const getRoleText = (role: string) => {
  return USER_ROLE_LABELS[role as keyof typeof USER_ROLE_LABELS] || role
}

const getRoleType = (role: string) => {
  const typeMap: Record<string, string> = {
    admin: 'danger',
    analyst: 'primary',
    operator: 'warning',
    viewer: 'info'
  }
  return typeMap[role] || 'info'
}

const getBatchActionText = (action: string) => {
  const actionMap: Record<string, string> = {
    enable: '启用',
    disable: '禁用',
    delete: '删除'
  }
  return actionMap[action] || action
}

// 用户操作方法
const showAddDialog = () => {
  isEdit.value = false
  userDialogVisible.value = true
  resetUserForm()
}

const editUser = (user: User) => {
  isEdit.value = true
  userDialogVisible.value = true

  // 填充表单数据
  userForm.id = user.id
  userForm.username = user.username
  userForm.email = user.email
  userForm.full_name = user.full_name || ''
  userForm.role = user.role
  userForm.is_active = user.is_active
  userForm.notes = user.notes || ''
}

const resetUserForm = () => {
  userForm.id = 0
  userForm.username = ''
  userForm.email = ''
  userForm.full_name = ''
  userForm.password = ''
  userForm.role = 'analyst'
  userForm.is_active = true
  userForm.notes = ''
}

const handleUserSubmit = () => {
  if (!userFormRef.value) return

  userFormRef.value.validate((valid: boolean) => {
    if (!valid) return

    userFormLoading.value = true

    const action = isEdit.value ? '更新' : '创建'

    if (isDevelopmentMode) {
      // 开发模式：模拟API调用
      console.log(`🔧 开发模式：模拟${action}用户`, userForm)
      setTimeout(() => {
        ElMessage.success(`${action}用户成功`)
        userDialogVisible.value = false
        userFormLoading.value = false
        loadData()
        loadStatistics()
      }, 1000)
    } else {
      // 生产模式：真实API调用
      const apiCall = isEdit.value
        ? usersApi.updateUser(userForm.id, userForm)
        : usersApi.createUser(userForm)

      apiCall.then(() => {
        ElMessage.success(`${action}用户成功`)
        userDialogVisible.value = false
        userFormLoading.value = false
        loadData()
        loadStatistics()
      }).catch((error) => {
        console.error(`${action}用户失败:`, error)
        ElMessage.error(`${action}用户失败`)
        userFormLoading.value = false
      })
    }
  })
}

const handleAction = (command: string, user: User) => {
  switch (command) {
    case 'resetPassword':
      handleResetPassword(user)
      break
    case 'enable':
    case 'disable':
      handleToggleStatus(user, command === 'enable')
      break
    case 'delete':
      handleDeleteUser(user)
      break
  }
}

const handleResetPassword = (user: User) => {
  ElMessageBox.confirm(
    `确定要重置用户 "${user.username}" 的密码吗？`,
    '重置密码',
    {
      type: 'warning'
    }
  ).then(() => {
    ElMessage.success('密码重置成功，新密码已发送到用户邮箱')
  }).catch(() => {
    // 用户取消
  })
}

const handleToggleStatus = (user: User, enable: boolean) => {
  const action = enable ? '启用' : '禁用'
  ElMessageBox.confirm(
    `确定要${action}用户 "${user.username}" 吗？`,
    `${action}用户`,
    {
      type: 'warning'
    }
  ).then(() => {
    ElMessage.success(`${action}用户成功`)
    loadData()
    loadStatistics()
  }).catch(() => {
    // 用户取消
  })
}

const handleDeleteUser = (user: User) => {
  ElMessageBox.confirm(
    `确定要删除用户 "${user.username}" 吗？此操作不可恢复！`,
    '删除用户',
    {
      type: 'error'
    }
  ).then(() => {
    ElMessage.success('删除用户成功')
    loadData()
    loadStatistics()
  }).catch(() => {
    // 用户取消
  })
}

// 批量操作方法
const showBatchDialog = () => {
  if (selectedUsers.value.length === 0) {
    ElMessage.warning('请先选择要操作的用户')
    return
  }
  batchDialogVisible.value = true
  batchForm.action = ''
}

const handleBatchSubmit = () => {
  if (!batchForm.action) {
    ElMessage.warning('请选择操作类型')
    return
  }

  batchLoading.value = true

  // 模拟批量操作
  setTimeout(() => {
    const actionText = getBatchActionText(batchForm.action)
    ElMessage.success(`批量${actionText}操作完成`)
    batchDialogVisible.value = false
    batchLoading.value = false
    selectedUsers.value = []
    loadData()
    loadStatistics()
  }, 1500)
}
</script>

<style lang="scss" scoped>
.users-container {
  padding: 20px;

  .page-header {
    margin-bottom: 24px;

    .page-title {
      font-size: 24px;
      font-weight: 600;
      color: #303133;
      margin-bottom: 8px;
    }

    .page-description {
      color: #606266;
      font-size: 14px;
      margin: 0;
    }
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 24px;

    .stat-card {
      background: white;
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
      display: flex;
      align-items: center;

      .stat-icon {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 16px;
        font-size: 20px;

        &.primary { background: #ecf5ff; color: #409eff; }
        &.success { background: #f0f9ff; color: #67c23a; }
        &.warning { background: #fdf6ec; color: #e6a23c; }
        &.danger { background: #fef0f0; color: #f56c6c; }
      }

      .stat-content {
        .stat-title {
          font-size: 14px;
          color: #909399;
          margin-bottom: 4px;
        }

        .stat-value {
          font-size: 20px;
          font-weight: 600;
          color: #303133;
        }
      }
    }
  }

  .filter-card {
    margin-bottom: 16px;

    :deep(.el-card__body) {
      padding: 16px 20px;
    }
  }

  .table-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;

      .header-actions {
        display: flex;
        gap: 8px;
      }
    }

    .user-info {
      display: flex;
      align-items: center;

      .user-details {
        margin-left: 12px;

        .username {
          font-weight: 500;
          color: #303133;
        }

        .user-id {
          font-size: 12px;
          color: #909399;
          margin-top: 2px;
        }
      }
    }

    .pagination-container {
      display: flex;
      justify-content: center;
      margin-top: 20px;
    }
  }
}

:deep(.danger-item) {
  color: #f56c6c;
}

@media (max-width: 768px) {
  .users-container {
    padding: 16px;

    .stats-grid {
      grid-template-columns: 1fr;
    }

    .filter-card {
      :deep(.el-form--inline .el-form-item) {
        display: block;
        margin-right: 0;
        margin-bottom: 16px;
      }
    }
  }
}
</style>
