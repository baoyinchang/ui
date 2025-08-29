<template>
  <div class="settings-container">
    <div class="page-header">
      <h1 class="page-title">系统设置</h1>
      <p class="page-description">配置系统参数、安全策略和运行选项</p>
    </div>

    <!-- 设置导航 -->
    <div class="settings-nav">
      <el-tabs v-model="activeTab" type="card">
        <el-tab-pane label="基本设置" name="basic">
          <template #label>
            <span class="tab-label">
              <el-icon><Setting /></el-icon>
              基本设置
            </span>
          </template>
        </el-tab-pane>

        <el-tab-pane label="安全策略" name="security">
          <template #label>
            <span class="tab-label">
              <el-icon><Lock /></el-icon>
              安全策略
            </span>
          </template>
        </el-tab-pane>

        <el-tab-pane label="邮件配置" name="email">
          <template #label>
            <span class="tab-label">
              <el-icon><Message /></el-icon>
              邮件配置
            </span>
          </template>
        </el-tab-pane>

        <el-tab-pane label="系统监控" name="monitoring">
          <template #label>
            <span class="tab-label">
              <el-icon><Monitor /></el-icon>
              系统监控
            </span>
          </template>
        </el-tab-pane>

        <el-tab-pane label="备份恢复" name="backup">
          <template #label>
            <span class="tab-label">
              <el-icon><FolderOpened /></el-icon>
              备份恢复
            </span>
          </template>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 基本设置 -->
    <div v-show="activeTab === 'basic'" class="settings-content">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card class="settings-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <el-icon><InfoFilled /></el-icon>
                <span>系统信息</span>
              </div>
            </template>

            <el-form :model="basicSettings" label-width="120px">
              <el-form-item label="系统名称">
                <el-input
                  v-model="basicSettings.system_name"
                  placeholder="请输入系统名称"
                />
              </el-form-item>

              <el-form-item label="系统描述">
                <el-input
                  v-model="basicSettings.system_description"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入系统描述"
                />
              </el-form-item>

              <el-form-item label="系统版本">
                <el-input
                  v-model="basicSettings.system_version"
                  disabled
                />
              </el-form-item>

              <el-form-item label="管理员邮箱">
                <el-input
                  v-model="basicSettings.admin_email"
                  placeholder="请输入管理员邮箱"
                />
              </el-form-item>

              <el-form-item label="时区设置">
                <el-select v-model="basicSettings.timezone" style="width: 100%">
                  <el-option label="Asia/Shanghai (UTC+8)" value="Asia/Shanghai" />
                  <el-option label="UTC (UTC+0)" value="UTC" />
                  <el-option label="America/New_York (UTC-5)" value="America/New_York" />
                </el-select>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card class="settings-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <el-icon><Clock /></el-icon>
                <span>会话设置</span>
              </div>
            </template>

            <el-form :model="basicSettings" label-width="120px">
              <el-form-item label="会话超时">
                <el-input-number
                  v-model="basicSettings.session_timeout"
                  :min="5"
                  :max="1440"
                  :step="5"
                  style="width: 100%"
                />
                <div class="form-tip">单位：分钟，范围：5-1440</div>
              </el-form-item>

              <el-form-item label="记住登录">
                <el-switch
                  v-model="basicSettings.remember_login_enabled"
                  active-text="启用"
                  inactive-text="禁用"
                />
                <div class="form-tip">允许用户选择记住登录状态</div>
              </el-form-item>

              <el-form-item label="并发登录">
                <el-switch
                  v-model="basicSettings.concurrent_login_enabled"
                  active-text="允许"
                  inactive-text="禁止"
                />
                <div class="form-tip">是否允许同一用户多处登录</div>
              </el-form-item>

              <el-form-item label="强制登出">
                <el-switch
                  v-model="basicSettings.force_logout_enabled"
                  active-text="启用"
                  inactive-text="禁用"
                />
                <div class="form-tip">管理员可强制用户登出</div>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 安全策略 -->
    <div v-show="activeTab === 'security'" class="settings-content">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card class="settings-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <el-icon><Key /></el-icon>
                <span>密码策略</span>
              </div>
            </template>

            <el-form :model="securitySettings" label-width="140px">
              <el-form-item label="密码最小长度">
                <el-input-number
                  v-model="securitySettings.min_password_length"
                  :min="6"
                  :max="32"
                  style="width: 100%"
                />
                <div class="form-tip">建议设置为8位以上</div>
              </el-form-item>

              <el-form-item label="密码复杂度">
                <el-checkbox-group v-model="securitySettings.password_requirements">
                  <el-checkbox label="uppercase">包含大写字母</el-checkbox>
                  <el-checkbox label="lowercase">包含小写字母</el-checkbox>
                  <el-checkbox label="numbers">包含数字</el-checkbox>
                  <el-checkbox label="symbols">包含特殊字符</el-checkbox>
                </el-checkbox-group>
              </el-form-item>

              <el-form-item label="密码有效期">
                <el-input-number
                  v-model="securitySettings.password_expiry_days"
                  :min="0"
                  :max="365"
                  style="width: 100%"
                />
                <div class="form-tip">0表示永不过期，单位：天</div>
              </el-form-item>

              <el-form-item label="密码历史">
                <el-input-number
                  v-model="securitySettings.password_history_count"
                  :min="0"
                  :max="10"
                  style="width: 100%"
                />
                <div class="form-tip">禁止重复使用最近N个密码</div>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card class="settings-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <el-icon><Warning /></el-icon>
                <span>登录安全</span>
              </div>
            </template>

            <el-form :model="securitySettings" label-width="140px">
              <el-form-item label="登录失败锁定">
                <el-switch
                  v-model="securitySettings.login_lockout_enabled"
                  active-text="启用"
                  inactive-text="禁用"
                />
              </el-form-item>

              <el-form-item label="最大失败次数">
                <el-input-number
                  v-model="securitySettings.max_login_attempts"
                  :min="3"
                  :max="10"
                  :disabled="!securitySettings.login_lockout_enabled"
                  style="width: 100%"
                />
              </el-form-item>

              <el-form-item label="锁定时间">
                <el-input-number
                  v-model="securitySettings.lockout_duration"
                  :min="5"
                  :max="1440"
                  :disabled="!securitySettings.login_lockout_enabled"
                  style="width: 100%"
                />
                <div class="form-tip">单位：分钟</div>
              </el-form-item>

              <el-form-item label="验证码">
                <el-switch
                  v-model="securitySettings.captcha_enabled"
                  active-text="启用"
                  inactive-text="禁用"
                />
                <div class="form-tip">登录时显示验证码</div>
              </el-form-item>

              <el-form-item label="双因子认证">
                <el-switch
                  v-model="securitySettings.two_factor_enabled"
                  active-text="启用"
                  inactive-text="禁用"
                />
                <div class="form-tip">支持TOTP和短信验证</div>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 邮件配置 -->
    <div v-show="activeTab === 'email'" class="settings-content">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card class="settings-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <el-icon><Message /></el-icon>
                <span>SMTP配置</span>
              </div>
            </template>

            <el-form :model="emailSettings" label-width="120px">
              <el-form-item label="SMTP服务器">
                <el-input
                  v-model="emailSettings.smtp_host"
                  placeholder="smtp.example.com"
                />
              </el-form-item>

              <el-form-item label="端口">
                <el-input-number
                  v-model="emailSettings.smtp_port"
                  :min="1"
                  :max="65535"
                  style="width: 100%"
                />
              </el-form-item>

              <el-form-item label="加密方式">
                <el-select v-model="emailSettings.smtp_security" style="width: 100%">
                  <el-option label="无加密" value="none" />
                  <el-option label="SSL" value="ssl" />
                  <el-option label="TLS" value="tls" />
                </el-select>
              </el-form-item>

              <el-form-item label="用户名">
                <el-input
                  v-model="emailSettings.smtp_username"
                  placeholder="请输入SMTP用户名"
                />
              </el-form-item>

              <el-form-item label="密码">
                <el-input
                  v-model="emailSettings.smtp_password"
                  type="password"
                  placeholder="请输入SMTP密码"
                  show-password
                />
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card class="settings-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <el-icon><Bell /></el-icon>
                <span>邮件通知</span>
              </div>
            </template>

            <el-form :model="emailSettings" label-width="120px">
              <el-form-item label="发件人名称">
                <el-input
                  v-model="emailSettings.sender_name"
                  placeholder="H-System EDR平台"
                />
              </el-form-item>

              <el-form-item label="发件人邮箱">
                <el-input
                  v-model="emailSettings.sender_email"
                  placeholder="noreply@hsystem.com"
                />
              </el-form-item>

              <el-form-item label="通知类型">
                <el-checkbox-group v-model="emailSettings.notification_types">
                  <el-checkbox label="login">登录通知</el-checkbox>
                  <el-checkbox label="alert">告警通知</el-checkbox>
                  <el-checkbox label="report">报告通知</el-checkbox>
                  <el-checkbox label="system">系统通知</el-checkbox>
                </el-checkbox-group>
              </el-form-item>

              <el-form-item>
                <el-button type="primary" @click="testEmail">
                  <el-icon><Promotion /></el-icon>
                  发送测试邮件
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 系统监控 -->
    <div v-show="activeTab === 'monitoring'" class="settings-content">
      <el-row :gutter="20">
        <el-col :span="24">
          <el-card class="settings-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <el-icon><Monitor /></el-icon>
                <span>监控配置</span>
              </div>
            </template>

            <el-form :model="monitoringSettings" label-width="140px">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="日志级别">
                    <el-select v-model="monitoringSettings.log_level" style="width: 100%">
                      <el-option label="DEBUG" value="DEBUG" />
                      <el-option label="INFO" value="INFO" />
                      <el-option label="WARNING" value="WARNING" />
                      <el-option label="ERROR" value="ERROR" />
                    </el-select>
                  </el-form-item>

                  <el-form-item label="日志保留天数">
                    <el-input-number
                      v-model="monitoringSettings.log_retention_days"
                      :min="1"
                      :max="365"
                      style="width: 100%"
                    />
                  </el-form-item>

                  <el-form-item label="性能监控">
                    <el-switch
                      v-model="monitoringSettings.performance_monitoring"
                      active-text="启用"
                      inactive-text="禁用"
                    />
                  </el-form-item>
                </el-col>

                <el-col :span="12">
                  <el-form-item label="指标收集">
                    <el-switch
                      v-model="monitoringSettings.metrics_enabled"
                      active-text="启用"
                      inactive-text="禁用"
                    />
                  </el-form-item>

                  <el-form-item label="错误报告">
                    <el-switch
                      v-model="monitoringSettings.error_reporting"
                      active-text="启用"
                      inactive-text="禁用"
                    />
                  </el-form-item>

                  <el-form-item label="审计日志">
                    <el-switch
                      v-model="monitoringSettings.audit_log_enabled"
                      active-text="启用"
                      inactive-text="禁用"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 备份恢复 -->
    <div v-show="activeTab === 'backup'" class="settings-content">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card class="settings-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <el-icon><FolderOpened /></el-icon>
                <span>备份设置</span>
              </div>
            </template>

            <el-form :model="backupSettings" label-width="120px">
              <el-form-item label="自动备份">
                <el-switch
                  v-model="backupSettings.auto_backup_enabled"
                  active-text="启用"
                  inactive-text="禁用"
                />
              </el-form-item>

              <el-form-item label="备份频率">
                <el-select
                  v-model="backupSettings.backup_frequency"
                  :disabled="!backupSettings.auto_backup_enabled"
                  style="width: 100%"
                >
                  <el-option label="每小时" value="hourly" />
                  <el-option label="每天" value="daily" />
                  <el-option label="每周" value="weekly" />
                  <el-option label="每月" value="monthly" />
                </el-select>
              </el-form-item>

              <el-form-item label="保留天数">
                <el-input-number
                  v-model="backupSettings.backup_retention_days"
                  :min="1"
                  :max="365"
                  style="width: 100%"
                />
              </el-form-item>

              <el-form-item label="备份位置">
                <el-input
                  v-model="backupSettings.backup_location"
                  placeholder="请输入备份目录路径"
                />
              </el-form-item>

              <el-form-item label="包含日志">
                <el-switch
                  v-model="backupSettings.include_logs"
                  active-text="是"
                  inactive-text="否"
                />
              </el-form-item>

              <el-form-item label="压缩备份">
                <el-switch
                  v-model="backupSettings.compress_backups"
                  active-text="是"
                  inactive-text="否"
                />
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card class="settings-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <el-icon><Download /></el-icon>
                <span>备份操作</span>
              </div>
            </template>

            <div class="backup-actions">
              <el-button type="primary" size="large" @click="createBackup">
                <el-icon><Download /></el-icon>
                立即备份
              </el-button>

              <el-button type="success" size="large" @click="showRestoreDialog">
                <el-icon><Upload /></el-icon>
                恢复备份
              </el-button>

              <div class="backup-info">
                <p><strong>最近备份：</strong>2024-01-15 10:30:00</p>
                <p><strong>备份大小：</strong>256 MB</p>
                <p><strong>备份状态：</strong><el-tag type="success">成功</el-tag></p>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 操作按钮 -->
    <div class="settings-actions">
      <el-button
        type="primary"
        size="large"
        :loading="saving"
        @click="saveSettings"
      >
        <el-icon><Check /></el-icon>
        保存所有设置
      </el-button>

      <el-button size="large" @click="resetSettings">
        <el-icon><RefreshLeft /></el-icon>
        重置设置
      </el-button>

      <el-button size="large" @click="loadSettings">
        <el-icon><Refresh /></el-icon>
        重新加载
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Setting,
  Lock,
  Message,
  Monitor,
  FolderOpened,
  InfoFilled,
  Clock,
  Key,
  Warning,
  Bell,
  Promotion,
  Download,
  Upload,
  Check,
  RefreshLeft,
  Refresh
} from '@element-plus/icons-vue'
import { settingsApi } from '@/api/settings'
import type { SystemSettings } from '@/types/api'

// 当前激活的标签页
const activeTab = ref('basic')

// 基本设置
const basicSettings = reactive({
  system_name: 'H-System EDR平台',
  system_description: '蜜罐安全管理系统',
  system_version: '1.0.0',
  admin_email: 'admin@hsystem.com',
  timezone: 'Asia/Shanghai',
  session_timeout: 30,
  remember_login_enabled: true,
  concurrent_login_enabled: false,
  force_logout_enabled: true
})

// 安全设置
const securitySettings = reactive({
  min_password_length: 8,
  password_requirements: ['lowercase', 'numbers'],
  password_expiry_days: 90,
  password_history_count: 3,
  login_lockout_enabled: true,
  max_login_attempts: 5,
  lockout_duration: 15,
  captcha_enabled: false,
  two_factor_enabled: false
})

// 邮件设置
const emailSettings = reactive({
  smtp_host: '',
  smtp_port: 587,
  smtp_security: 'tls',
  smtp_username: '',
  smtp_password: '',
  sender_name: 'H-System EDR平台',
  sender_email: 'noreply@hsystem.com',
  notification_types: ['alert', 'report']
})

// 监控设置
const monitoringSettings = reactive({
  log_level: 'INFO',
  log_retention_days: 30,
  metrics_enabled: true,
  performance_monitoring: true,
  error_reporting: true,
  audit_log_enabled: true
})

// 备份设置
const backupSettings = reactive({
  auto_backup_enabled: true,
  backup_frequency: 'daily',
  backup_retention_days: 7,
  backup_location: '/var/backups/hsystem',
  include_logs: false,
  compress_backups: true
})

// 加载状态
const loading = ref(false)
const saving = ref(false)

// 初始化
onMounted(() => {
  loadSettings()
})

// 加载设置
const loadSettings = async () => {
  loading.value = true
  try {
    const settings = await settingsApi.getSettings()

    // 更新各个设置对象
    Object.assign(basicSettings, settings.basic || {})
    Object.assign(securitySettings, settings.security || {})
    Object.assign(emailSettings, settings.email || {})
    Object.assign(monitoringSettings, settings.monitoring || {})
    Object.assign(backupSettings, settings.backup || {})
  } catch (error) {
    console.error('加载设置失败:', error)
    ElMessage.error('加载设置失败')
  } finally {
    loading.value = false
  }
}

// 保存设置
const saveSettings = async () => {
  saving.value = true
  try {
    const allSettings = {
      basic: basicSettings,
      security: securitySettings,
      email: emailSettings,
      monitoring: monitoringSettings,
      backup: backupSettings
    }

    await settingsApi.updateSettings(allSettings)
    ElMessage.success('设置保存成功')
  } catch (error) {
    console.error('保存设置失败:', error)
    ElMessage.error('保存设置失败')
  } finally {
    saving.value = false
  }
}

// 重置设置
const resetSettings = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要重置所有设置到默认值吗？此操作不可恢复！',
      '重置设置',
      {
        type: 'warning'
      }
    )

    await settingsApi.resetSettings()
    ElMessage.success('设置已重置')
    loadSettings()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('重置设置失败:', error)
      ElMessage.error('重置设置失败')
    }
  }
}

// 测试邮件
const testEmail = async () => {
  try {
    await settingsApi.testEmail(emailSettings)
    ElMessage.success('测试邮件发送成功，请检查收件箱')
  } catch (error) {
    console.error('发送测试邮件失败:', error)
    ElMessage.error('发送测试邮件失败')
  }
}

// 创建备份
const createBackup = async () => {
  try {
    await settingsApi.createBackup()
    ElMessage.success('备份创建成功')
  } catch (error) {
    console.error('创建备份失败:', error)
    ElMessage.error('创建备份失败')
  }
}

// 显示恢复对话框
const showRestoreDialog = () => {
  ElMessage.info('恢复功能待实现')
}
</script>

<style lang="scss" scoped>
.settings-container {
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

  .settings-nav {
    margin-bottom: 24px;

    .tab-label {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    :deep(.el-tabs__item) {
      font-size: 14px;
      font-weight: 500;
    }
  }

  .settings-content {
    .settings-card {
      margin-bottom: 20px;

      .card-header {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
        color: #303133;
      }

      .form-tip {
        font-size: 12px;
        color: #909399;
        margin-top: 4px;
        line-height: 1.4;
      }

      :deep(.el-form-item) {
        margin-bottom: 20px;
      }

      :deep(.el-checkbox-group) {
        display: flex;
        flex-direction: column;
        gap: 8px;
      }
    }

    .backup-actions {
      text-align: center;

      .el-button {
        margin: 0 8px 16px 8px;
        width: 140px;
      }

      .backup-info {
        margin-top: 20px;
        padding: 16px;
        background: #f8f9fa;
        border-radius: 6px;
        text-align: left;

        p {
          margin: 8px 0;
          font-size: 14px;
          color: #606266;

          strong {
            color: #303133;
          }
        }
      }
    }
  }

  .settings-actions {
    margin-top: 32px;
    text-align: center;
    padding: 24px;
    background: #f8f9fa;
    border-radius: 8px;

    .el-button {
      margin: 0 8px;
      min-width: 120px;
    }
  }
}

@media (max-width: 768px) {
  .settings-container {
    padding: 16px;

    .settings-content {
      :deep(.el-col) {
        margin-bottom: 20px;
      }
    }

    .settings-actions {
      .el-button {
        display: block;
        width: 100%;
        margin: 8px 0;
      }
    }
  }
}
</style>
