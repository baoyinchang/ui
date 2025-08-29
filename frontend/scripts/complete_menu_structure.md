# H-System EDR 完整菜单结构

## 🎯 基于demo_01的三级菜单设计

### 完整菜单树状结构

```
H-System EDR 菜单
├── 安全态势 (/dashboard)
├── 告警中心 (/alerts)
├── 调查与响应 (/investigation)
├── 资产管理 (/assets)
├── 威胁狩猎 (/hunting)
├── 威胁情报 (/intelligence)
├── 报告中心 (/reports)
└── 系统管理 (/system) ⭐ 三级菜单结构
    ├── 系统状态 (/system/status)
    ├── 系统设置 (/system/settings)
    ├── 蜜罐策略中心 (/system/honeypot) 📁
    │   ├── 蜜罐探针管理 (/system/honeypot/sensors)
    │   └── 蜜罐策略配置 (/system/honeypot/policies)
    ├── 用户与权限 (/system/user-permission) 📁
    │   ├── 用户管理 (/system/user-permission/users)
    │   └── 角色与权限 (/system/user-permission/roles)
    └── 系统维护 (/system/maintenance) 📁
        ├── 日志审计 (/system/maintenance/logs)
        ├── 更新管理 (/system/maintenance/updates)
        └── 备份与恢复 (/system/maintenance/backup)
```

## 📁 文件结构

### Vue组件文件
```
src/views/system/
├── index.vue                    # 系统管理主页
├── status.vue                   # 系统状态
├── settings.vue                 # 系统设置
├── honeypot/                    # 蜜罐策略中心
│   ├── index.vue               # 蜜罐策略中心主页
│   ├── sensors.vue             # 蜜罐探针管理
│   └── policies.vue            # 蜜罐策略配置
├── user-permission/             # 用户与权限
│   ├── index.vue               # 用户与权限主页
│   └── roles.vue               # 角色与权限
└── maintenance/                 # 系统维护
    ├── index.vue               # 系统维护主页
    ├── logs.vue                # 日志审计
    ├── updates.vue             # 更新管理
    └── backup.vue              # 备份与恢复
```

### 路由配置
- 使用Vue Router的嵌套路由
- 支持三级菜单结构
- 每个级别都有独立的权限控制

## 🎨 UI设计要求

### Element Plus菜单组件
- 使用el-sub-menu支持多级菜单
- 需要递归渲染子菜单
- 支持菜单展开/折叠状态

### 菜单渲染逻辑
```vue
<template v-for="route in menuRoutes" :key="route.path">
  <!-- 无子菜单的普通菜单项 -->
  <el-menu-item v-if="!route.children" />
  
  <!-- 有子菜单的菜单组 -->
  <el-sub-menu v-else>
    <!-- 递归渲染子菜单 -->
    <menu-item v-for="child in route.children" :route="child" />
  </el-sub-menu>
</template>
```

## 🔧 技术实现要点

1. **三级路由嵌套**: 需要正确配置Vue Router的children属性
2. **菜单递归渲染**: MainLayout.vue需要支持递归渲染多级菜单
3. **权限控制**: 每个菜单级别都需要独立的权限检查
4. **面包屑导航**: 需要显示完整的导航路径
5. **路由守卫**: 确保路由跳转和权限检查正确

## 📋 待完善功能

1. ✅ 创建所有Vue组件文件
2. ⚠️ 更新MainLayout.vue支持三级菜单
3. ⚠️ 测试菜单展开/折叠功能
4. ⚠️ 完善权限控制逻辑
5. ⚠️ 优化菜单样式和交互
