/**
 * 认证相关的组合式函数
 */

import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { authApi } from '@/api/auth'
import type { LoginForm, User } from '@/types/api'

export function useAuth() {
  const router = useRouter()
  const userStore = useUserStore()
  
  const loading = ref(false)
  const error = ref('')
  
  // 计算属性
  const isAuthenticated = computed(() => userStore.isAuthenticated)
  const currentUser = computed(() => userStore.currentUser)
  
  /**
   * 登录
   */
  const login = async (loginForm: LoginForm) => {
    try {
      loading.value = true
      error.value = ''
      
      const response = await authApi.login(loginForm)
      
      // 保存用户信息和token
      userStore.setUser(response.data.user)
      userStore.setToken(response.data.access_token)
      
      // 跳转到首页
      router.push('/')
      
      return response
    } catch (err: any) {
      error.value = err.message || '登录失败'
      throw err
    } finally {
      loading.value = false
    }
  }
  
  /**
   * 登出
   */
  const logout = async () => {
    try {
      loading.value = true
      
      // 调用登出API
      await authApi.logout()
      
      // 清除本地状态
      userStore.clearUser()
      
      // 跳转到登录页
      router.push('/login')
    } catch (err: any) {
      console.error('登出失败:', err)
    } finally {
      loading.value = false
    }
  }
  
  /**
   * 检查权限
   */
  const hasPermission = (permission: string): boolean => {
    return userStore.hasPermission(permission)
  }
  
  /**
   * 检查角色
   */
  const hasRole = (role: string): boolean => {
    return userStore.hasRole(role)
  }
  
  return {
    // 状态
    loading,
    error,
    isAuthenticated,
    currentUser,
    
    // 方法
    login,
    logout,
    hasPermission,
    hasRole
  }
}
