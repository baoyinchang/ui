# H-System EDR 菜单结构

## 🎯 基于demo_01的原始设计

### 主菜单（一级菜单）
1. **安全态势** (`/dashboard`) - 仪表板总览
2. **告警中心** (`/alerts`) - 安全告警管理
3. **调查与响应** (`/investigation`) - 事件调查分析
4. **资产管理** (`/assets`) - IT资产管理
5. **威胁狩猎** (`/hunting`) - 主动威胁搜索
6. **威胁情报** (`/intelligence`) - 威胁情报分析
7. **报告中心** (`/reports`) - 报表和分析
8. **系统管理** (`/system`) - 系统配置管理 ⭐ **有子菜单**

### 系统管理子菜单
```
系统管理 (/system)
├── 系统状态 (/system/status) - 监控系统运行状态
├── 系统设置 (/system/settings) - 系统参数配置
├── 用户管理 (/system/users) - 用户账户管理
├── 角色与权限 (/system/roles) - 权限管理
├── 蜜罐策略中心 (/system/honeypot) - 蜜罐配置
└── 日志审计 (/system/logs) - 操作日志查看
```

## 🔧 技术实现

### 路由配置
- 使用Vue Router的嵌套路由
- 父路由: `/system`
- 子路由: `/system/status`, `/system/users` 等

### 菜单渲染
- MainLayout.vue中使用Element Plus的el-sub-menu
- 根据route.children自动渲染子菜单
- 支持权限控制和菜单折叠

### 权限控制
- 每个子菜单都有独立的权限要求
- 开发模式下可通过VITE_ENABLE_AUTH=false禁用权限检查

## 🎨 UI设计
- 遵循Element Plus设计规范
- 支持菜单展开/折叠
- 面包屑导航显示当前位置
- 响应式设计，适配不同屏幕尺寸

## 📋 待完善功能
1. 蜜罐策略中心的二级子菜单
2. 系统维护相关功能
3. 更详细的权限粒度控制
4. 菜单项的图标和样式优化
