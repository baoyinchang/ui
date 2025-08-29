# 修复验证测试命令

## 在浏览器控制台中运行以下命令

### 1. 测试菜单样式
```javascript
// 检查子菜单背景色
const subMenus = document.querySelectorAll('.el-sub-menu .el-menu');
console.log('子菜单数量:', subMenus.length);

subMenus.forEach((menu, index) => {
    const bgColor = window.getComputedStyle(menu).backgroundColor;
    console.log(`子菜单 ${index + 1} 背景色:`, bgColor);
});

// 检查菜单项样式
const menuItems = document.querySelectorAll('.sidebar-menu .el-menu-item');
console.log('菜单项数量:', menuItems.length);

menuItems.forEach((item, index) => {
    const bgColor = window.getComputedStyle(item).backgroundColor;
    console.log(`菜单项 ${index + 1} 背景色:`, bgColor);
});
```

### 2. 测试用户管理页面
```javascript
// 导航到用户管理页面
$router.push('/system/user-permission/users');

// 等待页面加载
setTimeout(() => {
    console.log('当前路由:', $route.path);
    console.log('页面标题:', document.title);
    
    // 检查页面是否正常加载
    const userContainer = document.querySelector('.users-container');
    if (userContainer) {
        console.log('✅ 用户管理页面加载成功');
    } else {
        console.log('❌ 用户管理页面加载失败');
    }
}, 2000);
```

### 3. 测试图标显示
```javascript
// 检查图标是否正常显示
const icons = document.querySelectorAll('.el-icon');
console.log('页面图标数量:', icons.length);

let brokenIcons = 0;
icons.forEach((icon, index) => {
    const hasContent = icon.innerHTML.trim().length > 0;
    if (!hasContent) {
        brokenIcons++;
        console.log(`图标 ${index + 1} 可能有问题`);
    }
});

console.log(`正常图标: ${icons.length - brokenIcons}, 问题图标: ${brokenIcons}`);
```

### 4. 测试三级菜单展开
```javascript
// 测试系统管理菜单展开
const systemMenu = document.querySelector('[data-index="/system"]');
if (systemMenu) {
    systemMenu.click();
    console.log('✅ 点击系统管理菜单');
    
    setTimeout(() => {
        const subMenus = document.querySelectorAll('.el-sub-menu.is-opened');
        console.log('展开的子菜单数量:', subMenus.length);
        
        // 测试用户与权限子菜单
        const userPermissionMenu = document.querySelector('[data-index="/system/user-permission"]');
        if (userPermissionMenu) {
            userPermissionMenu.click();
            console.log('✅ 点击用户与权限菜单');
        }
    }, 500);
} else {
    console.log('❌ 未找到系统管理菜单');
}
```

## 预期结果

### 菜单样式
- 所有子菜单背景应该是透明的 (rgba(0, 0, 0, 0) 或 transparent)
- 悬停时背景变为 #34495e
- 激活时背景变为 #409eff

### 用户管理页面
- 页面能正常加载，不会卡在刷新状态
- 没有 "Identifier 'User' has already been declared" 错误
- 图标正常显示

### 路由导航
- 能正常导航到 /system/user-permission/users
- 面包屑显示正确的路径
- 菜单高亮状态正确
