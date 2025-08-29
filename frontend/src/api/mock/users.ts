/**
 * 模拟用户API - 开发模式使用
 */

import type {
  User,
  UserStatistics,
  CreateUserRequest,
  UpdateUserRequest,
  PaginatedResponse,
  UserQueryParams,
  BatchOperation,
  BatchResponse
} from '@/types/api'

// 模拟用户数据
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

// 模拟统计数据
const mockStatistics: UserStatistics = {
  total: 4,
  active: 3,
  inactive: 1,
  admins: 1
}

// 模拟网络延迟
const delay = (ms: number = 500) => new Promise(resolve => setTimeout(resolve, ms))

/**
 * 模拟用户API接口
 */
export const mockUsersApi = {
  /**
   * 获取用户列表
   */
  async getUsers(params?: UserQueryParams): Promise<PaginatedResponse<User>> {
    await delay(500)
    
    let filteredUsers = [...mockUsers]
    
    // 应用搜索过滤
    if (params?.search) {
      filteredUsers = filteredUsers.filter(user => 
        user.username.includes(params.search!) || 
        user.email.includes(params.search!) ||
        user.full_name?.includes(params.search!)
      )
    }
    
    if (params?.role) {
      filteredUsers = filteredUsers.filter(user => user.role === params.role)
    }
    
    if (params?.is_active !== undefined) {
      filteredUsers = filteredUsers.filter(user => user.is_active === params.is_active)
    }
    
    // 分页处理
    const page = params?.page || 1
    const size = params?.size || 20
    const start = (page - 1) * size
    const end = start + size
    const paginatedUsers = filteredUsers.slice(start, end)
    
    return {
      items: paginatedUsers,
      total: filteredUsers.length,
      page,
      size,
      pages: Math.ceil(filteredUsers.length / size)
    }
  },

  /**
   * 获取用户详情
   */
  async getUserById(id: number): Promise<User> {
    await delay(300)
    const user = mockUsers.find(u => u.id === id)
    if (!user) {
      throw new Error('用户不存在')
    }
    return user
  },

  /**
   * 创建用户
   */
  async createUser(data: CreateUserRequest): Promise<User> {
    await delay(800)
    const newUser: User = {
      id: Math.max(...mockUsers.map(u => u.id)) + 1,
      username: data.username,
      email: data.email,
      full_name: data.full_name || '',
      role: data.role,
      is_active: data.is_active ?? true,
      avatar: '',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      last_login: null,
      notes: data.notes || ''
    }
    mockUsers.push(newUser)
    return newUser
  },

  /**
   * 更新用户信息
   */
  async updateUser(id: number, data: UpdateUserRequest): Promise<User> {
    await delay(800)
    const userIndex = mockUsers.findIndex(u => u.id === id)
    if (userIndex === -1) {
      throw new Error('用户不存在')
    }
    
    const updatedUser = {
      ...mockUsers[userIndex],
      ...data,
      updated_at: new Date().toISOString()
    }
    mockUsers[userIndex] = updatedUser
    return updatedUser
  },

  /**
   * 删除用户
   */
  async deleteUser(id: number): Promise<void> {
    await delay(600)
    const userIndex = mockUsers.findIndex(u => u.id === id)
    if (userIndex === -1) {
      throw new Error('用户不存在')
    }
    mockUsers.splice(userIndex, 1)
  },

  /**
   * 启用/禁用用户
   */
  async toggleUserStatus(id: number, is_active: boolean): Promise<User> {
    await delay(400)
    const userIndex = mockUsers.findIndex(u => u.id === id)
    if (userIndex === -1) {
      throw new Error('用户不存在')
    }
    
    mockUsers[userIndex].is_active = is_active
    mockUsers[userIndex].updated_at = new Date().toISOString()
    return mockUsers[userIndex]
  },

  /**
   * 重置用户密码
   */
  async resetUserPassword(id: number): Promise<{ new_password: string }> {
    await delay(600)
    const user = mockUsers.find(u => u.id === id)
    if (!user) {
      throw new Error('用户不存在')
    }
    
    return {
      new_password: 'temp123456'
    }
  },

  /**
   * 获取用户统计信息
   */
  async getUserStatistics(): Promise<UserStatistics> {
    await delay(300)
    
    // 动态计算统计数据
    const total = mockUsers.length
    const active = mockUsers.filter(u => u.is_active).length
    const inactive = total - active
    const admins = mockUsers.filter(u => u.role === 'admin').length
    
    return {
      total,
      active,
      inactive,
      admins
    }
  },

  /**
   * 批量操作用户
   */
  async batchOperation(operation: BatchOperation): Promise<BatchResponse> {
    await delay(1000)
    
    return {
      success: true,
      affected_count: operation.user_ids.length,
      message: `批量${operation.action}操作完成`
    }
  }
}
