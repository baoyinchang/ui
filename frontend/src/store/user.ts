import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { User, LoginRequest } from '@/types/api'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref<string>('')
  const refreshToken = ref<string>('')
  const user = ref<User | null>(null)
  const permissions = ref<string[]>([])

  // 计算属性
  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const userRoles = computed(() => user.value?.roles || [])
  const userName = computed(() => user.value?.full_name || user.value?.username || '')

  // 登录
  const login = async (loginData: LoginRequest) => {
    try {
      const response = await authApi.login(loginData)
      
      // 保存token和用户信息
      token.value = response.access_token
      refreshToken.value = response.refresh_token
      user.value = response.user
      
      // 提取权限
      const allPermissions = response.user.roles.flatMap(role => 
        role.permissions?.map(p => p.name) || []
      )
      permissions.value = [...new Set(allPermissions)]
      
      return response
    } catch (error) {
      throw error
    }
  }

  // 登出
  const logout = async () => {
    try {
      if (token.value) {
        await authApi.logout()
      }
    } catch (error) {
      console.error('登出请求失败:', error)
    } finally {
      // 清除本地状态
      token.value = ''
      refreshToken.value = ''
      user.value = null
      permissions.value = []
    }
  }

  // 刷新用户信息
  const refreshUserInfo = async () => {
    try {
      if (!token.value) return
      
      const userInfo = await authApi.getCurrentUser()
      user.value = userInfo
      
      // 更新权限
      const allPermissions = userInfo.roles.flatMap(role => 
        role.permissions?.map(p => p.name) || []
      )
      permissions.value = [...new Set(allPermissions)]
      
      return userInfo
    } catch (error) {
      console.error('刷新用户信息失败:', error)
      throw error
    }
  }

  // 刷新token
  const refreshAccessToken = async () => {
    try {
      if (!refreshToken.value) {
        throw new Error('没有刷新令牌')
      }
      
      const response = await authApi.refreshToken(refreshToken.value)
      token.value = response.access_token
      
      return response
    } catch (error) {
      // 刷新失败，清除所有状态
      await logout()
      throw error
    }
  }

  // 检查权限
  const hasPermission = (permission: string): boolean => {
    // 开发环境下禁用权限检查时，允许所有权限
    const ENABLE_AUTH = import.meta.env.VITE_ENABLE_AUTH === 'true'
    if (!ENABLE_AUTH) {
      return true
    }

    return permissions.value.includes(permission)
  }

  // 检查角色
  const hasRole = (roleName: string): boolean => {
    return userRoles.value.some(role => role.name === roleName)
  }

  // 检查是否为管理员
  const isAdmin = computed(() => {
    return hasRole('admin') || hasRole('administrator') || hasRole('系统管理员')
  })

  return {
    // 状态
    token,
    refreshToken,
    user,
    permissions,
    
    // 计算属性
    isLoggedIn,
    userRoles,
    userName,
    isAdmin,
    
    // 方法
    login,
    logout,
    refreshUserInfo,
    refreshAccessToken,
    hasPermission,
    hasRole
  }
}, {
  persist: {
    key: 'hsystem-user',
    storage: localStorage,
    paths: ['token', 'refreshToken', 'user', 'permissions']
  }
})
