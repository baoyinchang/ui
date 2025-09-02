import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import Layout from '@/layouts/MainLayout.vue';

// 该路由配置直接关联到您在 src/views/ 目录下已实现的 Vue 组件。
// 我们在这里定义了完整的嵌套结构，以支持三级菜单的正确显示。
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        // 关联到您已有的 dashboard/index.vue
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '安全态势', icon: 'Dashboard' }
      },
      {
        path: 'alert-center',
        name: 'AlertCenter',
        // 关联到您已有的 alert-center/index.vue
        component: () => import('@/views/alerts/index.vue'),
        meta: { title: '告警中心', icon: 'Alert' }
      },
      // ... 其他一级菜单的关联 ...
      {
        path: 'investigation',
        name: 'Investigation',
        component: () => import('@/views/investigation/index.vue'),
        meta: { title: '调查与响应', icon: 'Search' }
      },
      {
        path: 'asset-management',
        name: 'AssetManagement',
        component: () => import('@/views/assets/AssetList.vue'),
        meta: { title: '资产管理', icon: 'Desktop' }
      },
      {
        path: 'threat-hunting',
        name: 'ThreatHunting',
        component: () => import('@/views/threat-hunting/index.vue'),
        meta: { title: '威胁狩猎', icon: 'Crosshairs' }
      },
      {
        path: 'threat-intelligence',
        name: 'ThreatIntelligence',
        component: () => import('@/views/intelligence/index.vue'),
        meta: { title: '威胁情报', icon: 'Shield' }
      },
      {
        path: 'report-center',
        name: 'ReportCenter',
        component: () => import('@/views/reports/index.vue'),
        meta: { title: '报告中心', icon: 'Document' }
      },
      {
        path: 'system',
        name: 'System',
        // 这是一个父路由容器，用于渲染下面的 children
        component: () => import('@/views/system/index.vue'), 
        redirect: '/system/status',
        meta: { title: '系统管理', icon: 'Setting' },
        children: [
          {
            path: 'status',
            name: 'SystemStatus',
            // 关联到您已有的 system/status.vue
            component: () => import('@/views/system/status.vue'),
            meta: { title: '系统状态' }
          },
          {
            path: 'settings',
            name: 'SystemSettings',
             // 关联到您已有的 system/settings.vue
            component: () => import('@/views/system/settings.vue'),
            meta: { title: '系统设置' }
          },
          // --- 蜜罐策略中心 (三级菜单) ---
          {
            path: 'honeypot',
            name: 'Honeypot',
            component: () => import('@/views/system/honeypot/index.vue'),
            redirect: '/system/honeypot/sensors',
            meta: { title: '蜜罐策略中心' },
            children: [
              {
                path: 'sensors',
                name: 'HoneypotSensors',
                component: () => import('@/views/system/honeypot/sensors.vue'),
                meta: { title: '蜜罐探针管理' }
              },
              {
                path: 'policies',
                name: 'HoneypotPolicies',
                component: () => import('@/views/system/honeypot/policies.vue'),
                meta: { title: '蜜罐策略配置' }
              }
            ]
          },
          // --- 用户与权限 (三级菜单) ---
          {
            path: 'user-permission',
            name: 'UserPermission',
            component: () => import('@/views/system/user-permission/index.vue'),
            redirect: '/system/user-permission/users',
            meta: { title: '用户与权限' },
            children: [
              {
                path: 'users',
                name: 'UserManagement',
                // 关联到您已有的 users/index.vue
                component: () => import('@/views/users/index.vue'), 
                meta: { title: '用户管理' }
              },
              {
                path: 'roles',
                name: 'RolePermission',
                component: () => import('@/views/system/user-permission/roles.vue'),
                meta: { title: '角色与权限' }
              }
            ]
          },
          // --- 系统维护 (三级菜单) ---
          {
            path: 'maintenance',
            name: 'Maintenance',
            component: () => import('@/views/system/maintenance/index.vue'),
            redirect: '/system/maintenance/logs',
            meta: { title: '系统维护' },
            children: [
              {
                path: 'logs',
                name: 'LogAudit',
                component: () => import('@/views/system/maintenance/logs.vue'),
                meta: { title: '日志审计' }
              },
              {
                path: 'updates',
                name: 'UpdateManagement',
                component: () => import('@/views/system/maintenance/updates.vue'),
                meta: { title: '更新管理' }
              },
              {
                path: 'backup',
                name: 'BackupRestore',
                component: () => import('@/views/system/maintenance/backup.vue'),
                meta: { title: '备份与恢复' }
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue')
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;

