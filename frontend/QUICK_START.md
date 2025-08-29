# H-System EDR平台前端 - 快速启动指南

## 环境要求
- Node.js 18+
- npm 8+ 或 yarn 1.22+

## 快速启动

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

#### 1. 安装依赖
```bash
cd frontend
npm install
```

#### 2. 启动开发服务器
```bash
npm run dev
```

#### 3. 访问应用
打开浏览器访问: http://localhost:3000

## 默认登录账户
- 管理员: admin / admin123456
- 分析师: analyst / analyst123456
- 运维: operator / operator123456

## 主要功能页面
- 安全态势总览: /dashboard
- 告警中心: /alerts
- 资产管理: /assets
- 威胁狩猎: /hunting
- 威胁情报: /intelligence
- 调查响应: /investigation
- 报告中心: /reports
- 用户管理: /users
- 系统设置: /settings
- 系统管理: /system

## 项目结构
```
src/
├── api/          # API接口
├── components/   # 公共组件
├── layouts/      # 布局组件
├── router/       # 路由配置
├── store/        # 状态管理
├── styles/       # 全局样式
├── types/        # 类型定义
├── utils/        # 工具函数
├── views/        # 页面组件
├── App.vue       # 根组件
└── main.ts       # 入口文件
```

## 开发说明
1. 所有页面组件都在 `src/views/` 目录下
2. API接口定义在 `src/api/` 目录下
3. 全局状态使用 Pinia 管理
4. 样式使用 SCSS 编写
5. 图表使用 ECharts + Vue-ECharts

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

## 构建部署
```bash
# 使用脚本构建（推荐）
build.bat          # Windows
./manage.sh build  # Linux/Mac

# 使用npm命令构建
npm run build

# 预览构建结果
npm run preview
```

## 测试命令
```bash
# 使用脚本测试（推荐）
test.bat all        # Windows - 运行所有测试
./manage.sh test    # Linux/Mac - 运行所有测试

# 单独测试命令
test.bat unit       # 单元测试
test.bat lint       # 代码检查
test.bat type       # 类型检查
test.bat coverage   # 测试覆盖率
```

## 故障排除

### 环境问题
1. **Node.js版本过低**：升级到18.0.0或更高版本
2. **依赖安装失败**：
   ```bash
   npm cache clean --force
   npm config set registry https://registry.npmmirror.com/
   ```

### 开发问题
1. **端口被占用**：修改 `vite.config.ts` 中的端口配置
2. **API请求失败**：检查 `.env` 文件中的API地址配置
3. **类型错误**：运行 `npm run type-check` 检查类型问题

### 构建问题
1. **构建失败**：检查代码语法错误和依赖问题
2. **构建文件过大**：检查是否正确配置了代码分割
3. **静态资源404**：检查 `vite.config.ts` 中的 `base` 配置

### 使用健康检查
```bash
# Windows
setup.bat

# Linux/Mac
./manage.sh doctor
```
