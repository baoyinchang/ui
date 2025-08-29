# H-System EDR Frontend 项目结构

## 📁 目录结构

```
frontend/
├── public/                     # 静态资源
│   ├── favicon.ico            # 网站图标
│   ├── logo.svg               # SVG Logo
│   ├── logo.png               # PNG Logo
│   ├── icon-192x192.png       # PWA图标
│   └── icon-512x512.png       # PWA图标
├── src/                       # 源代码
│   ├── components/            # 组件
│   │   ├── icons/            # 图标组件
│   │   └── layout/           # 布局组件
│   │       └── MenuTree.vue  # 递归菜单组件
│   ├── layouts/              # 布局
│   │   └── MainLayout.vue    # 主布局
│   ├── views/                # 页面视图
│   │   ├── dashboard/        # 仪表板
│   │   ├── alerts/           # 告警管理
│   │   ├── assets/           # 资产管理
│   │   ├── hunting/          # 威胁狩猎
│   │   ├── intelligence/     # 威胁情报
│   │   ├── investigation/    # 事件调查
│   │   ├── reports/          # 报表分析
│   │   ├── system/           # 系统管理
│   │   │   ├── honeypot/     # 蜜罐策略中心
│   │   │   ├── user-permission/ # 用户与权限
│   │   │   └── maintenance/  # 系统维护
│   │   └── users/            # 用户管理
│   ├── router/               # 路由配置
│   ├── store/                # 状态管理
│   ├── api/                  # API接口
│   └── types/                # 类型定义
├── scripts/                  # 工具脚本
│   ├── test_*.py            # 测试脚本
│   ├── create_*.py          # 创建脚本
│   ├── *.html               # 测试页面
│   └── *.md                 # 文档
└── package.json             # 项目配置
```

## 🎨 图标系统

### 静态图标文件
- `public/favicon.ico` - 浏览器标签页图标
- `public/logo.svg` - 矢量Logo（推荐）
- `public/logo.png` - 位图Logo
- PWA图标用于移动端和桌面应用

### Vue图标组件
- `src/components/icons/` - 自定义图标组件
- 支持Element Plus图标系统
- 可扩展的图标映射

## 🔧 开发工具

### scripts/ 目录
- **测试脚本**: 用于验证功能和结构
- **创建脚本**: 用于生成代码和文件
- **调试工具**: 用于问题排查
- **文档**: 项目说明和使用指南

### 使用方法
```bash
# 运行测试脚本
cd scripts
python test_three_level_menu.py

# 查看调试信息
open debug_three_level_menu.md
```

## 🚀 部署说明

### 开发环境
```bash
npm run dev
```

### 生产构建
```bash
npm run build
```

### 图标优化
- SVG图标自动优化
- PNG图标压缩
- ICO图标多尺寸支持

## 📋 维护清单

### 定期检查
- [ ] 图标文件完整性
- [ ] 路由配置正确性
- [ ] 组件依赖关系
- [ ] 权限控制逻辑

### 更新流程
1. 修改源代码
2. 运行测试脚本验证
3. 更新文档
4. 提交代码

## 🎯 最佳实践

### 图标使用
- 优先使用SVG格式
- 保持图标风格一致
- 合理使用图标尺寸

### 组件开发
- 遵循Vue 3 Composition API
- 使用TypeScript类型检查
- 保持组件单一职责

### 目录管理
- 定期清理临时文件
- 保持目录结构清晰
- 及时更新文档
