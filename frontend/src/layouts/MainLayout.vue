<template>
  <div class="main-layout">
    <!-- 侧边栏 -->
    <div class="sidebar" :class="{ collapsed: appStore.sidebarCollapsed }">
      <div class="sidebar-header">
        <div class="logo">
          <img src="/logo.svg" alt="Logo" class="logo-img" />
          <span v-show="!appStore.sidebarCollapsed" class="logo-text">H-System EDR</span>
        </div>
      </div>
      
      <el-menu
        :default-active="$route.path"
        :collapse="appStore.sidebarCollapsed"
        :unique-opened="true"
        router
        class="sidebar-menu"
      >
        <!-- 递归菜单组件 -->
        <MenuTree
          :routes="menuRoutes"
          :has-permission="hasPermission"
        />
      </el-menu>
    </div>
    
    <!-- 主内容区 -->
    <div class="main-container">
      <!-- 顶部导航栏 -->
      <div class="header">
        <div class="header-left">
          <el-button
            type="text"
            @click="appStore.toggleSidebar"
            class="collapse-btn"
          >
            <el-icon><Expand v-if="appStore.sidebarCollapsed" /><Fold v-else /></el-icon>
          </el-button>
          
          <el-breadcrumb separator="/">
            <el-breadcrumb-item
              v-for="item in breadcrumbs"
              :key="item.path"
              :to="item.path"
            >
              {{ item.title }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        
        <div class="header-right">
          <!-- 全屏按钮 -->
          <el-tooltip content="全屏" placement="bottom">
            <el-button type="text" @click="toggleFullscreen">
              <el-icon><FullScreen /></el-icon>
            </el-button>
          </el-tooltip>
          
          <!-- 主题切换 -->
          <el-tooltip content="切换主题" placement="bottom">
            <el-button type="text" @click="appStore.toggleTheme">
              <el-icon><Sunny v-if="appStore.theme === 'light'" /><Moon v-else /></el-icon>
            </el-button>
          </el-tooltip>
          
          <!-- 用户菜单 -->
          <el-dropdown @command="handleUserCommand">
            <div class="user-info">
              <el-avatar :size="32" :src="userAvatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <span class="username">{{ userStore.userName }}</span>
              <el-icon class="arrow-down"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  个人资料
                </el-dropdown-item>
                <el-dropdown-item command="settings">
                  <el-icon><Setting /></el-icon>
                  系统设置
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      
      <!-- 页面内容 -->
      <div class="content">
        <router-view v-slot="{ Component, route }">
          <transition name="fade-transform" mode="out-in">
            <keep-alive :include="cachedViews">
              <component :is="Component" :key="route.path" />
            </keep-alive>
          </transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Expand,
  Fold,
  FullScreen,
  Sunny,
  Moon,
  User,
  ArrowDown,
  Setting,
  SwitchButton
} from '@element-plus/icons-vue'
import { useAppStore } from '@/store/app'
import { useUserStore } from '@/store/user'
import MenuTree from '@/components/layout/MenuTree.vue'

const router = useRouter()
const appStore = useAppStore()
const userStore = useUserStore()

// 菜单路由
const menuRoutes = computed(() => {
  return router.getRoutes()
    .find(route => route.name === 'Layout')
    ?.children?.filter(route => !route.meta?.hideInMenu) || []
})

// 面包屑导航
const breadcrumbs = computed(() => {
  const matched = router.currentRoute.value.matched.filter(item => item.meta?.title)
  return matched.map(item => ({
    title: item.meta?.title as string,
    path: item.path
  }))
})

// 缓存的视图
const cachedViews = ref<string[]>([])

// 用户头像
const userAvatar = computed(() => {
  return userStore.user?.avatar || ''
})

// 权限检查
const hasPermission = (permission?: string) => {
  if (!permission) return true

  // 开发环境禁用权限检查
  const ENABLE_AUTH = import.meta.env.VITE_ENABLE_AUTH === 'true'
  if (!ENABLE_AUTH) return true

  // 检查userStore是否存在且有hasPermission方法
  if (!userStore || typeof userStore.hasPermission !== 'function') {
    console.warn('用户权限检查失败，userStore未正确初始化')
    return false
  }

  return userStore.hasPermission(permission)
}

// 全屏切换
const toggleFullscreen = () => {
  if (document.fullscreenElement) {
    document.exitFullscreen()
  } else {
    document.documentElement.requestFullscreen()
  }
}

// 用户菜单命令处理
const handleUserCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      // 跳转到个人资料页面
      router.push('/profile')
      break
    case 'settings':
      // 跳转到设置页面
      router.push('/settings')
      break
    case 'logout':
      try {
        await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await userStore.logout()
        ElMessage.success('退出登录成功')
        router.push('/login')
      } catch (error) {
        // 用户取消操作
      }
      break
  }
}
</script>

<style lang="scss" scoped>
.main-layout {
  display: flex;
  height: 100vh;
  
  .sidebar {
    width: 220px;
    background: #2c3e50;
    transition: width 0.3s;
    overflow: hidden;
    
    &.collapsed {
      width: 64px;
    }
    
    .sidebar-header {
      height: 60px;
      display: flex;
      align-items: center;
      padding: 0 20px;
      border-bottom: 1px solid #34495e;
      
      .logo {
        display: flex;
        align-items: center;
        color: white;
        
        .logo-img {
          width: 32px;
          height: 32px;
          margin-right: 12px;
        }
        
        .logo-text {
          font-size: 18px;
          font-weight: 600;
        }
      }
    }
    
    .sidebar-menu {
      border: none;
      background: transparent;

      :deep(.el-menu-item) {
        color: #bdc3c7;
        background: transparent;

        &:hover {
          background-color: #34495e;
          color: white;
        }

        &.is-active {
          background-color: #409eff;
          color: white;
        }
      }

      :deep(.el-sub-menu) {
        .el-sub-menu__title {
          color: #bdc3c7;
          background: transparent;

          &:hover {
            background-color: #34495e;
            color: white;
          }
        }

        .el-menu {
          background: transparent;
        }

        .el-menu-item {
          color: #bdc3c7;
          background: transparent;

          &:hover {
            background-color: #34495e;
            color: white;
          }

          &.is-active {
            background-color: #409eff;
            color: white;
          }
        }
      }
    }
  }
  
  .main-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    
    .header {
      height: 60px;
      background: white;
      border-bottom: 1px solid #e4e7ed;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
      
      .header-left {
        display: flex;
        align-items: center;
        
        .collapse-btn {
          margin-right: 20px;
          font-size: 18px;
        }
      }
      
      .header-right {
        display: flex;
        align-items: center;
        gap: 16px;
        
        .user-info {
          display: flex;
          align-items: center;
          cursor: pointer;
          padding: 8px 12px;
          border-radius: 4px;
          transition: background-color 0.3s;
          
          &:hover {
            background-color: #f5f7fa;
          }
          
          .username {
            margin: 0 8px;
            font-size: 14px;
            color: #606266;
          }
          
          .arrow-down {
            font-size: 12px;
            color: #909399;
          }
        }
      }
    }
    
    .content {
      flex: 1;
      overflow: auto;
      background: #f5f7fa;
    }
  }
}

// 页面切换动画
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.3s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
</style>
