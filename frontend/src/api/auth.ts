/**
 * 认证相关API接口
 */

import { http } from './request'
import type {
  LoginRequest,
  LoginResponse,
  RefreshTokenRequest,
  ChangePasswordRequest,
  ResetPasswordRequest,
  User
} from '@/types/api'

/**
 * 认证API接口
 */
export const authApi = {
  /**
   * 用户登录
   */
  login(data: LoginRequest): Promise<LoginResponse> {
    return http.post('/auth/login', data)
  },

  /**
   * 刷新访问令牌
   */
  refreshToken(data: RefreshTokenRequest): Promise<{
    access_token: string
    refresh_token: string
    expires_in: number
  }> {
    return http.post('/auth/refresh', data)
  },

  /**
   * 用户登出
   */
  logout(): Promise<{ success: boolean; message: string }> {
    return http.post('/auth/logout')
  },

  /**
   * 获取当前用户信息
   */
  getCurrentUser(): Promise<User> {
    return http.get('/auth/me')
  },

  /**
   * 更新当前用户信息
   */
  updateCurrentUser(data: Partial<User>): Promise<User> {
    return http.put('/auth/me', data)
  },

  /**
   * 修改当前用户密码
   */
  changePassword(data: ChangePasswordRequest): Promise<{ success: boolean; message: string }> {
    return http.post('/auth/change-password', data)
  },

  /**
   * 请求密码重置
   */
  requestPasswordReset(data: ResetPasswordRequest): Promise<{ success: boolean; message: string }> {
    return http.post('/auth/password-reset', data)
  },

  /**
   * 确认密码重置
   */
  confirmPasswordReset(token: string, newPassword: string): Promise<{ success: boolean; message: string }> {
    return http.post('/auth/password-reset/confirm', {
      token,
      new_password: newPassword
    })
  },

  /**
   * 验证密码重置令牌
   */
  validateResetToken(token: string): Promise<{ valid: boolean; email?: string }> {
    return http.get(`/auth/password-reset/validate/${token}`)
  },

  /**
   * 获取登录验证码
   */
  getCaptcha(): Promise<{ captcha_id: string; captcha_image: string }> {
    return http.get('/auth/captcha')
  },

  /**
   * 验证登录验证码
   */
  verifyCaptcha(captchaId: string, captchaCode: string): Promise<{ valid: boolean }> {
    return http.post('/auth/captcha/verify', {
      captcha_id: captchaId,
      captcha_code: captchaCode
    })
  },

  /**
   * 启用双因子认证
   */
  enableTwoFactor(): Promise<{
    secret: string
    qr_code: string
    backup_codes: string[]
  }> {
    return http.post('/auth/2fa/enable')
  },

  /**
   * 确认启用双因子认证
   */
  confirmTwoFactor(code: string): Promise<{ success: boolean; message: string }> {
    return http.post('/auth/2fa/confirm', { code })
  },

  /**
   * 禁用双因子认证
   */
  disableTwoFactor(password: string): Promise<{ success: boolean; message: string }> {
    return http.post('/auth/2fa/disable', { password })
  },

  /**
   * 验证双因子认证码
   */
  verifyTwoFactor(code: string): Promise<{ valid: boolean }> {
    return http.post('/auth/2fa/verify', { code })
  },

  /**
   * 生成新的备份码
   */
  generateBackupCodes(): Promise<{ backup_codes: string[] }> {
    return http.post('/auth/2fa/backup-codes')
  },

  /**
   * 检查用户会话状态
   */
  checkSession(): Promise<{ valid: boolean; expires_at?: string }> {
    return http.get('/auth/session/check')
  },

  /**
   * 延长用户会话
   */
  extendSession(): Promise<{ success: boolean; expires_at: string }> {
    return http.post('/auth/session/extend')
  },

  /**
   * 获取用户登录历史
   */
  getLoginHistory(limit?: number): Promise<Array<{
    id: number
    ip_address: string
    user_agent: string
    login_time: string
    logout_time?: string
    status: string
  }>> {
    return http.get('/auth/login-history', { params: { limit } })
  },

  /**
   * 获取当前活跃会话
   */
  getActiveSessions(): Promise<Array<{
    id: string
    ip_address: string
    user_agent: string
    created_at: string
    last_activity: string
    is_current: boolean
  }>> {
    return http.get('/auth/sessions')
  },

  /**
   * 终止指定会话
   */
  terminateSession(sessionId: string): Promise<{ success: boolean; message: string }> {
    return http.delete(`/auth/sessions/${sessionId}`)
  },

  /**
   * 终止所有其他会话
   */
  terminateOtherSessions(): Promise<{ success: boolean; terminated_count: number }> {
    return http.post('/auth/sessions/terminate-others')
  }
}
