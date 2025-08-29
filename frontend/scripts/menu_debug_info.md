# 菜单调试信息

## 问题描述
页面右边菜单只显示"安全态势"，其他菜单项不显示。

## 可能原因
1. 路由权限检查失败
2. 用户权限未正确初始化
3. 菜单过滤逻辑问题

## 修复措施
1. 在MainLayout.vue中修改hasPermission函数，开发模式下返回true
2. 在user.ts中修改hasPermission方法，开发模式下返回true
3. 确保VITE_ENABLE_AUTH=false

## 调试步骤
1. 打开浏览器开发者工具
2. 在Console中输入：
   ```javascript
   // 检查环境变量
   console.log('VITE_ENABLE_AUTH:', import.meta.env.VITE_ENABLE_AUTH)
   
   // 检查路由
   console.log('所有路由:', $router.getRoutes())
   
   // 检查菜单路由
   const layoutRoute = $router.getRoutes().find(r => r.name === 'Layout')
   console.log('菜单路由:', layoutRoute?.children)
   
   // 检查用户store
   console.log('用户store:', useUserStore())
   ```

## 预期结果
所有菜单项都应该显示，包括：
- 仪表板
- 告警管理
- 资产管理
- 威胁狩猎
- 威胁情报
- 事件调查
- 报表分析
- 系统管理
