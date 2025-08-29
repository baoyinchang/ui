# 三级菜单调试命令

## 在浏览器控制台中运行以下命令

### 1. 检查路由结构
```javascript
// 获取所有路由
const allRoutes = $router.getRoutes();
console.log('所有路由:', allRoutes);

// 查找系统管理路由
const systemRoute = allRoutes.find(r => r.path === '/system');
console.log('系统管理路由:', systemRoute);

// 检查系统管理的子路由
if (systemRoute && systemRoute.children) {
    console.log('系统管理子路由数量:', systemRoute.children.length);
    systemRoute.children.forEach(child => {
        console.log(`子路由: ${child.path} - ${child.meta?.title}`);
        if (child.children) {
            console.log(`  有 ${child.children.length} 个三级子路由`);
            child.children.forEach(grandChild => {
                console.log(`    三级路由: ${grandChild.path} - ${grandChild.meta?.title}`);
            });
        }
    });
}
```

### 2. 测试菜单权限
```javascript
// 检查权限函数
const userStore = useUserStore();
console.log('权限检查函数:', typeof userStore.hasPermission);

// 测试各种权限
const permissions = [
    'system:read',
    'honeypot:read', 
    'user:read',
    'system:maintain'
];

permissions.forEach(perm => {
    console.log(`权限 ${perm}:`, userStore.hasPermission(perm));
});
```

### 3. 测试路由导航
```javascript
// 测试三级路由导航
const testRoutes = [
    '/system',
    '/system/status',
    '/system/honeypot',
    '/system/honeypot/sensors',
    '/system/user-permission/users',
    '/system/maintenance/logs'
];

testRoutes.forEach(route => {
    console.log(`测试路由: ${route}`);
    try {
        $router.push(route);
        console.log(`✅ ${route} 导航成功`);
    } catch (error) {
        console.log(`❌ ${route} 导航失败:`, error.message);
    }
});
```

### 4. 检查菜单组件
```javascript
// 检查MenuTree组件是否正确加载
const app = getCurrentInstance();
console.log('当前组件实例:', app);

// 检查菜单数据
const layoutRoute = $router.getRoutes().find(r => r.name === 'Layout');
const menuRoutes = layoutRoute?.children?.filter(r => !r.meta?.hideInMenu) || [];
console.log('菜单路由数据:', menuRoutes);
```
