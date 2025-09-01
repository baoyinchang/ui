<template>
  <div class="system-container">
    <div class="page-header">
      <h1 class="page-title">系统管理</h1>
      <p class="page-description">管理系统配置、用户权限、蜜罐策略和系统维护</p>
    </div>
    
    <div class="page-content">
      <!-- 系统概览 -->
      <el-row :gutter="16" class="overview-row">
        <el-col :span="6" v-for="overview in systemOverview" :key="overview.key">
          <el-card class="overview-card" @click="navigateTo(overview.route)">
            <div class="card-content">
              <div class="card-icon" :class="overview.iconClass">
                <el-icon><component :is="overview.icon" /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-value">{{ overview.value }}</div>
                <div class="card-label">{{ overview.label }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 功能模块 -->
      <el-row :gutter="16" class="modules-row">
        <el-col :span="8" v-for="module in systemModules" :key="module.key">
          <el-card class="module-card" @click="navigateTo(module.route)">
            <div class="module-header">
              <el-icon class="module-icon" :class="module.iconClass">
                <component :is="module.icon" />
              </el-icon>
              <h3 class="module-title">{{ module.title }}</h3>
            </div>
            <p class="module-description">{{ module.description }}</p>
            <div class="module-actions">
              <el-button type="primary" size="small">进入</el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 快速操作 -->
      <el-row :gutter="16" class="actions-row">
        <el-col :span="12">
          <el-card title="快速操作">
            <div class="quick-actions">
              <el-button-group>
                <el-button @click="navigateTo('/system/status')">
                  <el-icon><Monitor /></el-icon>
                  系统状态
                </el-button>
                <el-button @click="navigateTo('/system/logs')">
                  <el-icon><Document /></el-icon>
                  查看日志
                </el-button>
                <el-button @click="navigateTo('/system/settings')">
                  <el-icon><Setting /></el-icon>
                  系统设置
                </el-button>
              </el-button-group>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card title="系统信息">
            <div class="system-info">
              <div class="info-item">
                <span class="info-label">系统版本:</span>
                <span class="info-value">v1.0.0</span>
              </div>
              <div class="info-item">
                <span class="info-label">运行时间:</span>
                <span class="info-value">{{ uptime }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">最后更新:</span>
                <span class="info-value">{{ lastUpdate }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  Monitor,
  Setting,
  User,
  Lock,
  DataBoard,
  Tools,
  Document,
  Refresh
} from '@element-plus/icons-vue'

const router = useRouter()

// 系统概览数据
const systemOverview = ref([
  { key: 'users', label: '用户总数', value: 12, icon: User, iconClass: 'users', route: '/system/user-permission/users' },
  { key: 'roles', label: '角色数量', value: 5, icon: Lock, iconClass: 'roles', route: '/system/user-permission/roles' },
  { key: 'honeypots', label: '蜜罐探针', value: 8, icon: DataBoard, iconClass: 'honeypots', route: '/system/honeypot' },
  { key: 'logs', label: '今日日志', value: 156, icon: Document, iconClass: 'logs', route: '/system/logs' }
])

// 功能模块
const systemModules = ref([
  {
    key: 'user-permission',
    title: '用户与权限',
    description: '管理用户账户、角色和权限分配',
    icon: User,
    iconClass: 'user-permission',
    route: '/system/user-permission'
  },
  {
    key: 'honeypot',
    title: '蜜罐策略中心',
    description: '配置和管理蜜罐探针策略',
    icon: DataBoard,
    iconClass: 'honeypot',
    route: '/system/honeypot'
  },
  {
    key: 'maintenance',
    title: '系统维护',
    description: '日志审计、更新管理和备份恢复',
    icon: Tools,
    iconClass: 'maintenance',
    route: '/system/maintenance'
  }
])

// 系统信息
const uptime = ref('3天 12小时 45分钟')
const lastUpdate = ref('2024-01-15 14:30:00')

// 导航方法
const navigateTo = (route: string) => {
  router.push(route)
}

// 组件挂载
onMounted(() => {
  console.log('System Management 页面已加载')
})
</script>

<style scoped lang="scss">
.system-container {
  padding: 20px;

  .page-header {
    margin-bottom: 24px;

    .page-title {
      font-size: 28px;
      font-weight: 600;
      color: var(--el-text-color-primary);
      margin: 0 0 8px 0;
    }

    .page-description {
      font-size: 16px;
      color: var(--el-text-color-regular);
      margin: 0;
    }
  }

  .overview-row {
    margin-bottom: 24px;

    .overview-card {
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }

      .card-content {
        display: flex;
        align-items: center;
        gap: 16px;

        .card-icon {
          width: 56px;
          height: 56px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 28px;

          &.users { background: rgba(64, 158, 255, 0.1); color: #409eff; }
          &.roles { background: rgba(103, 194, 58, 0.1); color: #67c23a; }
          &.honeypots { background: rgba(230, 162, 60, 0.1); color: #e6a23c; }
          &.logs { background: rgba(245, 108, 108, 0.1); color: #f56c6c; }
        }

        .card-info {
          .card-value {
            font-size: 32px;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 4px;
          }

          .card-label {
            font-size: 14px;
            color: var(--el-text-color-regular);
          }
        }
      }
    }
  }

  .modules-row {
    margin-bottom: 24px;

    .module-card {
      cursor: pointer;
      transition: all 0.3s ease;
      height: 200px;
      display: flex;
      flex-direction: column;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }

      .module-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;

        .module-icon {
          width: 48px;
          height: 48px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 24px;

          &.user-permission { background: rgba(64, 158, 255, 0.1); color: #409eff; }
          &.honeypot { background: rgba(230, 162, 60, 0.1); color: #e6a23c; }
          &.maintenance { background: rgba(103, 194, 58, 0.1); color: #67c23a; }
        }

        .module-title {
          font-size: 18px;
          font-weight: 600;
          margin: 0;
          color: var(--el-text-color-primary);
        }
      }

      .module-description {
        flex: 1;
        color: var(--el-text-color-regular);
        line-height: 1.6;
        margin-bottom: 16px;
      }

      .module-actions {
        text-align: right;
      }
    }
  }

  .actions-row {
    .quick-actions {
      text-align: center;
    }

    .system-info {
      .info-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid var(--el-border-color-lighter);

        &:last-child {
          border-bottom: none;
        }

        .info-label {
          color: var(--el-text-color-regular);
        }

        .info-value {
          font-weight: 500;
          color: var(--el-text-color-primary);
        }
      }
    }
  }
}
</style>