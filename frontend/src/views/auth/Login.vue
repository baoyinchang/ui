<template>
  <div class="login-container">
    <div class="login-background">
      <div class="bg-overlay"></div>
      <div class="bg-particles"></div>
    </div>
    
    <div class="login-content">
      <div class="login-form-container">
        <div class="login-header">
          <div class="logo">
            <img src="/logo.svg" alt="H-System" class="logo-img" />
            <h1 class="logo-text">H-System EDR平台</h1>
          </div>
          <p class="subtitle">蜜罐安全管理系统</p>
        </div>
        
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          @keyup.enter="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              size="large"
              :prefix-icon="User"
              clearable
            />
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              :prefix-icon="Lock"
              show-password
              clearable
            />
          </el-form-item>
          
          <el-form-item>
            <div class="login-options">
              <el-checkbox v-model="rememberMe">记住我</el-checkbox>
              <el-link type="primary" @click="showForgotPassword">忘记密码？</el-link>
            </div>
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              @click="handleLogin"
              class="login-btn"
            >
              {{ loading ? '登录中...' : '登录' }}
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="demo-accounts">
          <div class="demo-title">演示账户</div>
          <div class="demo-list">
            <el-tag
              v-for="account in demoAccounts"
              :key="account.username"
              class="demo-tag"
              @click="fillDemoAccount(account)"
            >
              {{ account.label }}
            </el-tag>
          </div>
        </div>
      </div>
      
      <div class="login-info">
        <div class="info-card">
          <h3>系统特性</h3>
          <ul class="feature-list">
            <li><el-icon><Shield /></el-icon> 全方位安全防护</li>
            <li><el-icon><Monitor /></el-icon> 实时威胁监控</li>
            <li><el-icon><DataAnalysis /></el-icon> 智能分析引擎</li>
            <li><el-icon><Connection /></el-icon> 多维度关联分析</li>
          </ul>
        </div>
        
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-number">2,456</div>
            <div class="stat-label">监控资产</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">24</div>
            <div class="stat-label">今日告警</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">99.9%</div>
            <div class="stat-label">系统可用性</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElForm } from 'element-plus'
import { User, Lock, Shield, Monitor, DataAnalysis, Connection } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import type { FormInstance, FormRules } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

// 表单引用
const loginFormRef = ref<FormInstance>()

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 表单验证规则
const loginRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 50, message: '用户名长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 128, message: '密码长度在 6 到 128 个字符', trigger: 'blur' }
  ]
}

// 其他状态
const loading = ref(false)
const rememberMe = ref(false)

// 演示账户
const demoAccounts = [
  { username: 'admin', password: 'admin123456', label: '管理员' },
  { username: 'analyst', password: 'analyst123456', label: '分析师' },
  { username: 'operator', password: 'operator123456', label: '运维' }
]

// 登录处理
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    const valid = await loginFormRef.value.validate()
    if (!valid) return
    
    loading.value = true
    
    await userStore.login({
      username: loginForm.username,
      password: loginForm.password
    })
    
    ElMessage.success('登录成功')
    
    // 跳转到首页
    const redirect = router.currentRoute.value.query.redirect as string
    router.push(redirect || '/')
    
  } catch (error: any) {
    console.error('登录失败:', error)
    ElMessage.error(error.message || '登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}

// 填充演示账户
const fillDemoAccount = (account: typeof demoAccounts[0]) => {
  loginForm.username = account.username
  loginForm.password = account.password
}

// 忘记密码
const showForgotPassword = () => {
  ElMessage.info('请联系系统管理员重置密码')
}
</script>

<style lang="scss" scoped>
.login-container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  
  .login-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    
    .bg-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.3);
    }
    
    .bg-particles {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-image: 
        radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(120, 200, 255, 0.3) 0%, transparent 50%);
      animation: float 6s ease-in-out infinite;
    }
  }
  
  .login-content {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 20px;
    gap: 60px;
    
    .login-form-container {
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      padding: 40px;
      width: 400px;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
      
      .login-header {
        text-align: center;
        margin-bottom: 32px;
        
        .logo {
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 16px;
          
          .logo-img {
            width: 48px;
            height: 48px;
            margin-right: 12px;
          }
          
          .logo-text {
            font-size: 24px;
            font-weight: 600;
            color: #2c3e50;
            margin: 0;
          }
        }
        
        .subtitle {
          color: #606266;
          font-size: 14px;
          margin: 0;
        }
      }
      
      .login-form {
        .login-options {
          display: flex;
          justify-content: space-between;
          align-items: center;
          width: 100%;
        }
        
        .login-btn {
          width: 100%;
          height: 44px;
          font-size: 16px;
          font-weight: 500;
        }
      }
      
      .demo-accounts {
        margin-top: 24px;
        padding-top: 24px;
        border-top: 1px solid #ebeef5;
        
        .demo-title {
          font-size: 14px;
          color: #909399;
          margin-bottom: 12px;
          text-align: center;
        }
        
        .demo-list {
          display: flex;
          justify-content: center;
          gap: 8px;
          flex-wrap: wrap;
          
          .demo-tag {
            cursor: pointer;
            transition: all 0.3s;
            
            &:hover {
              transform: translateY(-2px);
              box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
          }
        }
      }
    }
    
    .login-info {
      color: white;
      max-width: 400px;
      
      .info-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 32px;
        margin-bottom: 24px;
        
        h3 {
          font-size: 20px;
          margin-bottom: 20px;
          color: white;
        }
        
        .feature-list {
          list-style: none;
          padding: 0;
          margin: 0;
          
          li {
            display: flex;
            align-items: center;
            margin-bottom: 16px;
            font-size: 14px;
            
            .el-icon {
              margin-right: 12px;
              font-size: 18px;
              color: #67c23a;
            }
          }
        }
      }
      
      .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        
        .stat-item {
          background: rgba(255, 255, 255, 0.1);
          backdrop-filter: blur(10px);
          border-radius: 12px;
          padding: 20px;
          text-align: center;
          
          .stat-number {
            font-size: 24px;
            font-weight: 600;
            color: white;
            margin-bottom: 4px;
          }
          
          .stat-label {
            font-size: 12px;
            color: rgba(255, 255, 255, 0.8);
          }
        }
      }
    }
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

// 响应式设计
@media (max-width: 1024px) {
  .login-content {
    flex-direction: column;
    gap: 40px;
    
    .login-info {
      max-width: 400px;
    }
  }
}

@media (max-width: 768px) {
  .login-content {
    padding: 20px;
    
    .login-form-container {
      width: 100%;
      max-width: 400px;
      padding: 32px 24px;
    }
    
    .login-info {
      .stats-grid {
        grid-template-columns: 1fr;
      }
    }
  }
}
</style>
