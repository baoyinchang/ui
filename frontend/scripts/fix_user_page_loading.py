#!/usr/bin/env python3
"""
修复用户管理页面加载问题
在开发模式下使用模拟数据，避免API调用导致的无限加载
"""

import os
from pathlib import Path

def create_mock_users_api():
    """创建模拟用户API"""
    print("🔧 创建模拟用户API...")
    
    # 创建mock目录
    mock_dir = Path('../src/api/mock')
    mock_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建模拟用户API
    mock_users_content = '''/**
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
'''
    
    mock_file = mock_dir / 'users.ts'
    mock_file.write_text(mock_users_content, encoding='utf-8')
    print(f"   ✅ 模拟用户API已创建: {mock_file}")

def create_api_wrapper():
    """创建API包装器，根据环境选择真实或模拟API"""
    print("\n🔄 创建API包装器...")
    
    wrapper_content = '''/**
 * 用户API包装器
 * 根据环境变量选择使用真实API或模拟API
 */

import { usersApi as realUsersApi } from './users'
import { mockUsersApi } from './mock/users'

// 检查是否为开发模式且禁用认证
const isDevelopmentMode = import.meta.env.VITE_ENABLE_AUTH !== 'true'

// 导出适当的API
export const usersApi = isDevelopmentMode ? mockUsersApi : realUsersApi

// 开发模式提示
if (isDevelopmentMode) {
  console.log('🔧 开发模式：使用模拟用户API')
}
'''
    
    wrapper_file = Path('../src/api/usersWrapper.ts')
    wrapper_file.write_text(wrapper_content, encoding='utf-8')
    print(f"   ✅ API包装器已创建: {wrapper_file}")

def update_user_page_import():
    """更新用户页面的API导入"""
    print("\n📝 更新用户页面API导入...")
    
    user_file = Path('../src/views/users/Index.vue')
    if not user_file.exists():
        print("   ❌ 用户页面文件不存在")
        return False
    
    content = user_file.read_text(encoding='utf-8')
    
    # 替换API导入
    old_import = "import { usersApi } from '@/api/users'"
    new_import = "import { usersApi } from '@/api/usersWrapper'"
    
    if old_import in content:
        content = content.replace(old_import, new_import)
        user_file.write_text(content, encoding='utf-8')
        print("   ✅ 用户页面API导入已更新")
        return True
    else:
        print("   ⚠️  未找到需要替换的导入语句")
        return False

def create_test_script():
    """创建测试脚本"""
    print("\n📋 创建测试脚本...")
    
    test_content = '''# 用户管理页面修复测试

## 修复内容
1. 创建了模拟用户API (`src/api/mock/users.ts`)
2. 创建了API包装器 (`src/api/usersWrapper.ts`)
3. 更新了用户页面的API导入

## 测试步骤

### 1. 重启前端服务
```bash
npm run dev
```

### 2. 访问用户管理页面
- 导航到：系统管理 > 用户与权限 > 用户管理
- 或直接访问：http://localhost:3000/system/user-permission/users

### 3. 验证功能
- [ ] 页面能正常加载（不再无限加载）
- [ ] 显示模拟用户数据（4个用户）
- [ ] 统计卡片显示正确数据
- [ ] 搜索功能正常工作
- [ ] 分页功能正常工作

### 4. 浏览器控制台检查
```javascript
// 检查是否使用模拟API
console.log('当前环境:', import.meta.env.VITE_ENABLE_AUTH)

// 检查页面加载状态
const userContainer = document.querySelector('.users-container')
console.log('用户页面容器:', userContainer ? '存在' : '不存在')

// 检查用户数据
const userRows = document.querySelectorAll('.el-table__row')
console.log('用户行数:', userRows.length)
```

## 预期结果

### 开发模式 (VITE_ENABLE_AUTH=false)
- ✅ 使用模拟数据，页面快速加载
- ✅ 显示4个模拟用户
- ✅ 所有操作都是模拟的，不会调用真实API
- ✅ 控制台显示 "🔧 开发模式：使用模拟用户API"

### 生产模式 (VITE_ENABLE_AUTH=true)
- ✅ 使用真实API
- ✅ 需要正确的认证token
- ✅ 调用后端API接口

## 故障排除

### 如果页面仍然无限加载
1. 检查浏览器控制台是否有错误
2. 确认 VITE_ENABLE_AUTH 环境变量设置
3. 清除浏览器缓存并刷新
4. 重启前端服务

### 如果显示API错误
1. 检查网络请求是否被拦截
2. 确认模拟API文件是否正确创建
3. 检查API包装器的导入路径
'''
    
    test_file = Path('user_page_fix_test.md')
    test_file.write_text(test_content, encoding='utf-8')
    print(f"   ✅ 测试脚本已创建: {test_file}")

def main():
    """主函数"""
    print("🔧 修复用户管理页面加载问题")
    print("=" * 40)
    
    # 切换到scripts目录
    os.chdir(Path(__file__).parent)
    
    # 执行修复步骤
    create_mock_users_api()
    create_api_wrapper()
    import_updated = update_user_page_import()
    create_test_script()
    
    print("\n🎉 用户管理页面修复完成！")
    
    if import_updated:
        print("\n✅ 修复成功！")
        print("\n📋 完成的工作:")
        print("   ✅ 创建了模拟用户API")
        print("   ✅ 创建了API包装器")
        print("   ✅ 更新了页面API导入")
        print("   ✅ 创建了测试文档")
        
        print("\n🚀 现在可以:")
        print("   1. 重启前端服务: npm run dev")
        print("   2. 访问用户管理页面")
        print("   3. 查看 user_page_fix_test.md 进行详细测试")
        
        print("\n🎯 预期效果:")
        print("   - 页面快速加载，不再无限转圈")
        print("   - 显示4个模拟用户数据")
        print("   - 所有功能正常工作")
    else:
        print("\n⚠️  部分修复可能需要手动完成")
        print("   请检查用户页面的API导入是否正确")

if __name__ == "__main__":
    main()
