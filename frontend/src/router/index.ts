import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import NProgress from 'nprogress'

// 路由配置
const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: {
      title: '用户登录',
      requiresAuth: false,
      hideInMenu: true
    }
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/layouts/MainLayout.vue'),
    redirect: '/dashboard',
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: {
          title: '安全态势',
          icon: 'TrendCharts',
          requiresAuth: true
        }
      },
      {
        path: '/alerts',
        name: 'Alerts',
        component: () => import('@/views/alerts/Index.vue'),
        meta: {
          title: '告警中心',
          icon: 'Warning',
          requiresAuth: true,
          permission: 'alert:read'
        }
      },
      {
        path: '/alerts/:id',
        name: 'AlertDetail',
        component: () => import('@/views/alerts/Detail.vue'),
        meta: {
          title: '告警详情',
          requiresAuth: true,
          hideInMenu: true,
          permission: 'alert:read'
        }
      },
      {
        path: '/assets',
        name: 'Assets',
        component: () => import('@/views/assets/index.vue'),
        meta: {
          title: '资产管理',
          icon: 'Monitor',
          requiresAuth: true,
          permission: 'asset:read'
        }
      },
      {
        path: '/assets/:id',
        name: 'AssetDetail',
        component: () => import('@/views/assets/detail.vue'),
        meta: {
          title: '资产详情',
          requiresAuth: true,
          hideInMenu: true,
          permission: 'asset:read'
        }
      },
      {
        path: '/hunting',
        name: 'Hunting',
        component: () => import('@/views/hunting/index.vue'),
        meta: {
          title: '威胁狩猎',
          icon: 'Aim',
          requiresAuth: true,
          permission: 'hunting:read'
        }
      },
      {
        path: '/hunting/:id',
        name: 'HuntingDetail',
        component: () => import('@/views/hunting/detail.vue'),
        meta: {
          title: '狩猎任务详情',
          requiresAuth: true,
          hideInMenu: true,
          permission: 'hunting:read'
        }
      },
      {
        path: '/intelligence',
        name: 'Intelligence',
        component: () => import('@/views/intelligence/index.vue'),
        meta: {
          title: '威胁情报',
          icon: 'Shield',
          requiresAuth: true,
          permission: 'intelligence:read'
        }
      },
      {
        path: '/investigation',
        name: 'Investigation',
        component: () => import('@/views/investigation/index.vue'),
        meta: {
          title: '调查与响应',
          icon: 'Search',
          requiresAuth: true,
          permission: 'investigation:read'
        }
      },
      {
        path: '/investigation/:id',
        name: 'InvestigationDetail',
        component: () => import('@/views/investigation/detail.vue'),
        meta: {
          title: '调查详情',
          requiresAuth: true,
          hideInMenu: true,
          permission: 'investigation:read'
        }
      },
      {
        path: '/reports',
        name: 'Reports',
        component: () => import('@/views/reports/index.vue'),
        meta: {
          title: '报告中心',
          icon: 'Document',
          requiresAuth: true,
          permission: 'report:read'
        }
      },
      {
        path: '/system',
        name: 'System',
        component: () => import('@/views/system/index.vue'),
        meta: {
          title: '系统管理',
          icon: 'Setting',
          requiresAuth: true,
          permission: 'system:read'
        },
        children: [
          {
            path: 'status',
            name: 'SystemStatus',
            component: () => import('@/views/system/status.vue'),
            meta: {
              title: '系统状态',
              requiresAuth: true,
              permission: 'system:read'
            }
          },
          {
            path: 'settings',
            name: 'SystemSettings',
            component: () => import('@/views/system/settings.vue'),
            meta: {
              title: '系统设置',
              requiresAuth: true,
              permission: 'system:write'
            }
          },
          {
            path: 'honeypot',
            name: 'HoneypotCenter',
            component: () => import('@/views/system/honeypot/index.vue'),
            meta: {
              title: '蜜罐策略中心',
              requiresAuth: true,
              permission: 'honeypot:read'
            },
            children: [
              {
                path: 'sensors',
                name: 'HoneypotSensors',
                component: () => import('@/views/system/honeypot/sensors.vue'),
                meta: {
                  title: '蜜罐探针管理',
                  requiresAuth: true,
                  permission: 'honeypot:read'
                }
              },
              {
                path: 'policies',
                name: 'HoneypotPolicies',
                component: () => import('@/views/system/honeypot/policies.vue'),
                meta: {
                  title: '蜜罐策略配置',
                  requiresAuth: true,
                  permission: 'honeypot:write'
                }
              }
            ]
          },
          {
            path: 'user-permission',
            name: 'UserPermissionCenter',
            component: () => import('@/views/system/user-permission/index.vue'),
            meta: {
              title: '用户与权限',
              requiresAuth: true,
              permission: 'user:read'
            },
            children: [
              {
                path: 'users',
                name: 'UserManagement',
                component: () => import('@/views/users/Index.vue'),
                meta: {
                  title: '用户管理',
                  requiresAuth: true,
                  permission: 'user:read'
                }
              },
              {
                path: 'roles',
                name: 'RolePermission',
                component: () => import('@/views/system/user-permission/roles.vue'),
                meta: {
                  title: '角色与权限',
                  requiresAuth: true,
                  permission: 'role:read'
                }
              }
            ]
          },
          {
            path: 'maintenance',
            name: 'SystemMaintenance',
            component: () => import('@/views/system/maintenance/index.vue'),
            meta: {
              title: '系统维护',
              requiresAuth: true,
              permission: 'system:maintain'
            },
            children: [
              {
                path: 'logs',
                name: 'LogAudit',
                component: () => import('@/views/system/maintenance/logs.vue'),
                meta: {
                  title: '日志审计',
                  requiresAuth: true,
                  permission: 'log:read'
                }
              },
              {
                path: 'updates',
                name: 'UpdateManagement',
                component: () => import('@/views/system/maintenance/updates.vue'),
                meta: {
                  title: '更新管理',
                  requiresAuth: true,
                  permission: 'system:update'
                }
              },
              {
                path: 'backup',
                name: 'BackupRestore',
                component: () => import('@/views/system/maintenance/backup.vue'),
                meta: {
                  title: '备份与恢复',
                  requiresAuth: true,
                  permission: 'system:backup'
                }
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/403',
    name: 'Forbidden',
    component: () => import('@/views/error/403.vue'),
    meta: {
      title: '权限不足',
      hideInMenu: true
    }
  },
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue'),
    meta: {
      title: '页面不存在',
      hideInMenu: true
    }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  NProgress.start()

  try {
    const userStore = useUserStore()
    const appStore = useAppStore()

    // 设置页面标题
    if (to.meta.title) {
      document.title = `${to.meta.title} - H-System EDR`
      // 安全地设置应用标题
      if (appStore && typeof appStore.setPageTitle === 'function') {
        appStore.setPageTitle(to.meta.title as string)
      }
    }

    // 开发环境临时禁用认证检查
    // 可以通过环境变量控制：VITE_ENABLE_AUTH=true
    const ENABLE_AUTH = import.meta.env.VITE_ENABLE_AUTH === 'true'

    if (ENABLE_AUTH && to.meta.requiresAuth) {
      // 检查用户是否登录
      if (!userStore || !userStore.isLoggedIn) {
        console.log('用户未登录，重定向到登录页')
        next('/login')
        return
      }

      // 检查权限
      if (to.meta.permission && typeof userStore.hasPermission === 'function') {
        if (!userStore.hasPermission(to.meta.permission as string)) {
          console.log('用户权限不足，重定向到403页面')
          next('/403')
          return
        }
      }
    }

    // 已登录用户访问登录页，重定向到首页
    if (ENABLE_AUTH && to.name === 'Login' && userStore && userStore.isLoggedIn) {
      next('/')
      return
    }

    next()
  } catch (error) {
    console.error('路由守卫错误:', error)
    // 发生错误时直接放行，避免页面卡死
    next()
  }
})

router.afterEach(() => {
  NProgress.done()
})

export default router