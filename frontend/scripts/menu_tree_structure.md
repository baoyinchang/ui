# H-System EDR 三级菜单结构

## 🌳 完整菜单树

```
H-System EDR
├── 安全态势 (/dashboard)
├── 告警中心 (/alerts)
├── 调查与响应 (/investigation)
├── 资产管理 (/assets)
├── 威胁狩猎 (/hunting)
├── 威胁情报 (/intelligence)
├── 报告中心 (/reports)
└── 系统管理 (/system) ⭐ 三级菜单
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

## 🎯 与demo_01对比

### ✅ 完全匹配的结构
- 系统管理作为主菜单项
- 蜜罐策略中心包含2个子功能
- 用户与权限包含2个子功能  
- 系统维护包含3个子功能

### 🔧 技术实现
- Vue Router嵌套路由
- 递归菜单组件 (MenuTree.vue)
- Element Plus多级菜单
- 权限控制每个层级

## 📋 测试清单

### 菜单显示测试
- [ ] 系统管理显示为可展开菜单
- [ ] 蜜罐策略中心显示子菜单
- [ ] 用户与权限显示子菜单
- [ ] 系统维护显示子菜单

### 路由导航测试
- [ ] 点击系统状态正常跳转
- [ ] 点击蜜罐探针管理正常跳转
- [ ] 点击用户管理正常跳转
- [ ] 点击日志审计正常跳转

### 权限控制测试
- [ ] 开发模式下所有菜单可见
- [ ] 权限控制正常工作
- [ ] 面包屑导航正确显示

## 🚀 使用说明

1. **重启服务**: `npm run dev`
2. **查看菜单**: 左侧菜单应显示三级结构
3. **测试导航**: 点击各级菜单项测试跳转
4. **检查权限**: 确认权限控制正常
