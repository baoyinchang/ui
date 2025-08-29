# H-System EDR平台 - 前端

基于Vue 3 + TypeScript + Element Plus构建的现代化蜜罐EDR平台前端应用。

## 技术栈

- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **UI组件库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **图表库**: ECharts + Vue-ECharts
- **HTTP客户端**: Axios
- **样式**: SCSS
- **工具库**: Day.js, Lodash-es, VueUse

## 功能特性

### 核心功能
- 🔐 用户认证与权限管理
- 📊 安全态势总览仪表板
- 🚨 告警中心与事件管理
- 💻 资产管理与监控
- 🎯 威胁狩猎与分析
- 🛡️ 威胁情报管理
- 🔍 调查与响应
- 📋 报告中心
- ⚙️ 系统管理

### 界面特性
- 🎨 现代化Material Design风格
- 📱 响应式设计，支持移动端
- 🌙 支持明暗主题切换
- 🚀 流畅的页面切换动画
- 📈 丰富的数据可视化图表
- 🔄 实时数据更新

## 开发环境要求

- Node.js >= 18.0.0
- npm >= 8.0.0 或 yarn >= 1.22.0

## 快速开始

### 方式一：使用自动化脚本（推荐）

#### Windows用户
```batch
# 项目初始化（首次运行）
setup.bat

# 启动开发服务器
start.bat

# 构建生产版本
build.bat

# 运行测试
test.bat all
```

#### Linux/Mac用户
```bash
# 设置脚本执行权限（首次运行）
chmod +x *.sh

# 项目初始化
./manage.sh setup

# 启动开发服务器
./manage.sh dev

# 构建生产版本
./manage.sh build

# 运行测试
./manage.sh test
```

### 方式二：使用npm命令

#### 安装依赖
```bash
npm install
# 或
yarn install
```

#### 启动开发服务器
```bash
npm run dev
# 或
yarn dev
```

访问 http://localhost:3000

#### 构建生产版本
```bash
npm run build
# 或
yarn build
```

#### 预览生产构建
```bash
npm run preview
# 或
yarn preview
```

## 项目结构

```
src/
├── api/                 # API接口定义
├── assets/             # 静态资源
├── components/         # 公共组件
├── composables/        # 组合式函数
├── hooks/              # 自定义钩子
├── layouts/            # 布局组件
├── router/             # 路由配置
├── store/              # 状态管理
├── styles/             # 全局样式
├── types/              # TypeScript类型定义
├── utils/              # 工具函数
├── views/              # 页面组件
├── App.vue             # 根组件
└── main.ts             # 应用入口
```

## 环境配置

### 开发环境
复制 `.env.example` 到 `.env.development` 并配置：

```env
# API配置
VITE_API_BASE_URL=http://localhost:8000

# 开发服务器配置
VITE_DEV_PORT=3000
```

### 生产环境
配置 `.env.production`：

```env
# API配置
VITE_API_BASE_URL=https://your-api-domain.com

# 应用配置
VITE_APP_TITLE=H-System EDR平台
```

## 自动化脚本说明

### Windows脚本
- `setup.bat` - 项目初始化，检查环境、安装依赖、配置文件
- `start.bat` - 启动开发服务器，自动检查环境和依赖
- `build.bat` - 构建生产版本，包含完整的构建流程
- `test.bat` - 测试套件，支持多种测试命令

### Linux/Mac脚本
- `manage.sh` - 统一项目管理脚本，包含所有功能
- `start.sh` - 启动开发服务器
- `build.sh` - 构建生产版本
- `test.sh` - 测试套件

### 管理脚本使用示例
```bash
# 查看所有可用命令
./manage.sh help

# 项目健康检查
./manage.sh doctor

# 清理项目文件
./manage.sh clean

# 查看项目信息
./manage.sh info

# 更新依赖
./manage.sh deps
```

## 代码规范

项目使用ESLint + Prettier进行代码规范检查：

```bash
# 使用脚本（推荐）
test.bat lint       # Windows
./manage.sh lint    # Linux/Mac

# 使用npm命令
npm run lint        # 代码检查
npm run lint:fix    # 自动修复
npm run type-check  # 类型检查
```

## 部署

### Docker部署
```bash
# 构建镜像
docker build -t hsystem-frontend .

# 运行容器
docker run -p 80:80 hsystem-frontend
```

### Nginx部署
将构建产物部署到Nginx服务器，参考 `nginx.conf` 配置。

## 开发指南

### 添加新页面
1. 在 `src/views/` 下创建页面组件
2. 在 `src/router/index.ts` 中添加路由配置
3. 如需要，在侧边栏菜单中添加导航

### 添加新API
1. 在 `src/types/api.ts` 中定义类型
2. 在 `src/api/` 下创建对应的API模块
3. 在组件中使用API

### 状态管理
使用Pinia进行状态管理，在 `src/store/` 下创建store模块。

## 浏览器支持

- Chrome >= 87
- Firefox >= 78
- Safari >= 14
- Edge >= 88

## 许可证

MIT License