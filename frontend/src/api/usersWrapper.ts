/**
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
