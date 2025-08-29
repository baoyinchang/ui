<template>
  <div class="error-page">
    <div class="error-content">
      <div class="error-illustration">
        <div class="error-code">403</div>
        <div class="error-icon">
          <el-icon><Lock /></el-icon>
        </div>
      </div>
      
      <div class="error-info">
        <h1 class="error-title">权限不足</h1>
        <p class="error-description">
          抱歉，您没有权限访问此页面。
          <br>
          请联系系统管理员获取相应权限，或返回首页继续浏览。
        </p>
        
        <div class="error-actions">
          <el-button type="primary" @click="goHome">
            <el-icon><HomeFilled /></el-icon>
            返回首页
          </el-button>
          <el-button @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            返回上页
          </el-button>
        </div>
      </div>
    </div>
    
    <div class="error-footer">
      <p>如需申请权限，请联系系统管理员</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Lock, HomeFilled, ArrowLeft } from '@element-plus/icons-vue'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.back()
}
</script>

<style lang="scss" scoped>
.error-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  padding: 20px;
  
  .error-content {
    background: white;
    border-radius: 16px;
    padding: 60px 40px;
    text-align: center;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    max-width: 500px;
    width: 100%;
    
    .error-illustration {
      position: relative;
      margin-bottom: 40px;
      
      .error-code {
        font-size: 120px;
        font-weight: 700;
        color: #f0f0f0;
        line-height: 1;
        margin-bottom: 20px;
      }
      
      .error-icon {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 60px;
        color: #f56c6c;
      }
    }
    
    .error-info {
      .error-title {
        font-size: 28px;
        font-weight: 600;
        color: #303133;
        margin-bottom: 16px;
      }
      
      .error-description {
        color: #606266;
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 32px;
      }
      
      .error-actions {
        display: flex;
        justify-content: center;
        gap: 16px;
        
        .el-button {
          padding: 12px 24px;
          font-size: 16px;
        }
      }
    }
  }
  
  .error-footer {
    margin-top: 40px;
    color: rgba(255, 255, 255, 0.8);
    font-size: 14px;
  }
}

@media (max-width: 768px) {
  .error-page {
    .error-content {
      padding: 40px 20px;
      
      .error-illustration {
        .error-code {
          font-size: 80px;
        }
        
        .error-icon {
          font-size: 40px;
        }
      }
      
      .error-info {
        .error-title {
          font-size: 24px;
        }
        
        .error-actions {
          flex-direction: column;
          
          .el-button {
            width: 100%;
          }
        }
      }
    }
  }
}
</style>
