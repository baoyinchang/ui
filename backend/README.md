# H-System 蜜罐EDR平台 - 后端服务

基于FastAPI的现代化蜜罐系统管理平台后端服务。

## 🚀 快速开始

### 1. 环境准备

确保已安装以下软件：
- Python 3.9+
- PostgreSQL 14+
- Redis 6+ (可选)

### 2. 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt
```

### 3. 配置环境

复制并编辑环境配置文件：

```bash
# 创建.env文件
cp .env.example .env

# 编辑配置
vim .env
```

主要配置项：
```env
# 数据库配置
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=hsystem

# JWT密钥
SECRET_KEY=your_secret_key

# Redis配置（可选）
REDIS_URL=redis://localhost:6379/0
```

### 4. 初始化数据库

```bash
# 方法1: 使用管理脚本（推荐）
python manage_db.py create-tables
python manage_db.py init-data

# 方法2: 使用Alembic迁移
python manage_db.py init
python manage_db.py upgrade
python manage_db.py init-data

# 方法3: 直接重置数据库
python manage_db.py reset
```

### 5. 启动服务

```bash
# 开发模式启动
python start_server.py

# 或者直接使用uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. 测试API

```bash
# 运行API测试
python test_api.py
```

## 📋 默认账户

系统初始化后会创建以下默认账户：

| 用户名 | 密码 | 角色 | 描述 |
|--------|------|------|------|
| admin | admin123456 | 系统管理员 | 拥有所有权限 |
| analyst | analyst123456 | 安全分析师 | 告警处理和威胁分析 |
| operator | operator123456 | 安全运维 | 系统维护和资产管理 |

⚠️ **生产环境请务必修改默认密码！**

## 🔧 开发工具

### 数据库管理

```bash
# 查看所有可用命令
python manage_db.py --help

# 创建新的迁移
python manage_db.py migrate "描述信息"

# 升级数据库
python manage_db.py upgrade

# 查看当前版本
python manage_db.py current

# 查看迁移历史
python manage_db.py history
```

### API文档

启动服务后，访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/api/v1/openapi.json

## 🏗️ 项目结构

```
backend/
├── app/                    # 应用主目录
│   ├── api/               # API路由
│   │   └── v1/           # v1版本API
│   │       ├── auth.py   # 认证接口
│   │       ├── users.py  # 用户管理
│   │       ├── dashboard.py # 安全态势
│   │       └── ...       # 其他业务接口
│   ├── core/             # 核心模块
│   │   ├── config.py     # 配置管理
│   │   ├── db.py         # 数据库连接
│   │   ├── security.py   # 安全认证
│   │   └── dependencies.py # 依赖注入
│   ├── crud/             # 数据访问层
│   │   ├── base.py       # 基础CRUD
│   │   ├── user_crud.py  # 用户CRUD
│   │   └── ...           # 其他CRUD
│   ├── models/           # 数据模型
│   │   ├── postgres.py   # PostgreSQL模型
│   │   └── manticore.py  # Manticore模型
│   ├── schemas/          # 数据验证模式
│   │   ├── common.py     # 通用模式
│   │   ├── user.py       # 用户模式
│   │   └── ...           # 其他模式
│   ├── services/         # 业务逻辑层
│   ├── tasks/            # 异步任务
│   ├── utils/            # 工具函数
│   ├── main.py           # 应用入口
│   └── db_init.py        # 数据库初始化
├── migrations/           # 数据库迁移
├── tests/               # 测试文件
├── requirements.txt     # 依赖清单
├── alembic.ini         # Alembic配置
├── manage_db.py        # 数据库管理脚本
├── start_server.py     # 服务启动脚本
├── test_api.py         # API测试脚本
└── README.md           # 说明文档
```

## 🔐 安全特性

- **JWT认证**: 基于JSON Web Token的无状态认证
- **RBAC权限控制**: 基于角色的访问控制
- **密码加密**: 使用bcrypt进行密码哈希
- **输入验证**: 基于Pydantic的数据验证
- **SQL注入防护**: 使用SQLAlchemy ORM
- **CORS配置**: 跨域请求安全控制

## 📊 核心功能

### 已实现功能

- ✅ 用户认证与授权
- ✅ 用户管理（CRUD）
- ✅ 角色权限管理
- ✅ 安全态势总览
- ✅ 告警中心（告警管理、规则配置、统计分析）
- ✅ 资产管理（资产清单、漏洞管理、合规检查）
- ✅ 威胁狩猎（狩猎任务、模板管理、结果分析）
- ✅ 威胁情报（IOC管理、情报源配置、统计分析）
- ✅ 调查与响应（调查会话、时间线、证据管理）
- ✅ 报告中心（报告模板、生成管理、统计分析）
- ✅ 系统管理（系统监控、健康检查、配置管理）
- ✅ 数据库迁移管理
- ✅ API文档自动生成

### 核心特性

- 🔐 **完整的认证授权体系** - JWT + RBAC权限控制
- 📊 **8大核心业务模块** - 覆盖完整的安全管理场景
- 🛡️ **生产级安全架构** - 密码加密、输入验证、SQL注入防护
- ⚡ **高性能数据库设计** - 连接池、异步支持、事务管理
- 📈 **丰富的统计分析** - 多维度数据统计和趋势分析
- 🔍 **强大的搜索过滤** - 支持多条件组合查询
- 📝 **详细的操作日志** - 完整的审计追踪
- 🎯 **RESTful API设计** - 标准化接口，易于集成

## 📋 **API接口列表**

### 已实现的API接口

#### **认证相关** (`/api/v1/auth/`)
- `POST /login` - 用户登录
- `POST /refresh` - 刷新令牌
- `POST /logout` - 用户登出
- `GET /me` - 获取当前用户信息
- `POST /password-reset` - 密码重置

#### **用户管理** (`/api/v1/users/`)
- `GET /` - 获取用户列表
- `POST /` - 创建用户
- `GET /{user_id}` - 获取用户详情
- `PUT /{user_id}` - 更新用户信息
- `PUT /{user_id}/password` - 更新密码
- `DELETE /{user_id}` - 删除用户

#### **安全态势** (`/api/v1/dashboard/`)
- `GET /metrics` - 安全态势指标
- `GET /alert-trend` - 告警趋势数据
- `GET /threat-distribution` - 威胁类型分布
- `GET /asset-status` - 资产状态分布
- `GET /recent-alerts` - 最近告警
- `GET /big-screen` - 大屏数据

#### **告警中心** (`/api/v1/alerts/`)
- `GET /` - 获取告警列表
- `POST /` - 创建告警
- `GET /{alert_id}` - 获取告警详情
- `PUT /{alert_id}/status` - 更新告警状态
- `GET /statistics` - 获取告警统计
- `GET /rules` - 获取告警规则列表
- `POST /rules` - 创建告警规则
- `PUT /rules/{rule_id}` - 更新告警规则

#### **资产管理** (`/api/v1/assets/`)
- `GET /` - 获取资产列表
- `POST /` - 创建资产
- `GET /{asset_id}` - 获取资产详情
- `PUT /{asset_id}` - 更新资产信息
- `DELETE /{asset_id}` - 删除资产
- `GET /statistics` - 获取资产统计

#### **威胁狩猎** (`/api/v1/hunting/`)
- `GET /` - 获取狩猎任务列表
- `POST /` - 创建狩猎任务
- `GET /{task_id}` - 获取任务详情
- `POST /{task_id}/execute` - 执行狩猎任务
- `DELETE /{task_id}` - 删除狩猎任务
- `GET /templates` - 获取狩猎模板
- `GET /statistics` - 获取狩猎统计

#### **威胁情报** (`/api/v1/intelligence/`)
- `GET /iocs` - 获取IOC列表
- `POST /iocs` - 创建IOC
- `GET /iocs/{ioc_id}` - 获取IOC详情
- `GET /statistics` - 获取情报统计

#### **调查与响应** (`/api/v1/investigation/`)
- `GET /` - 获取调查会话列表
- `POST /` - 创建调查会话
- `GET /{session_id}` - 获取会话详情
- `GET /statistics` - 获取调查统计

#### **报告中心** (`/api/v1/reports/`)
- `GET /templates` - 获取报告模板
- `POST /generate` - 生成报告
- `GET /` - 获取报告列表
- `DELETE /{report_id}` - 删除报告
- `GET /statistics` - 获取报告统计

#### **系统管理** (`/api/v1/system/`)
- `GET /health` - 系统健康检查
- `GET /info` - 获取系统信息
- `GET /status` - 获取系统状态

**📊 总计：60+ API接口，覆盖8大核心业务模块**

## 🐛 故障排除

### 常见问题

1. **数据库连接失败**
   ```bash
   # 检查PostgreSQL服务状态
   sudo systemctl status postgresql

   # 检查数据库配置
   psql -h localhost -U postgres -d hsystem
   ```

2. **依赖安装失败**
   ```bash
   # 升级pip
   pip install --upgrade pip

   # 使用国内镜像
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
   ```

3. **端口占用**
   ```bash
   # 查看端口占用
   lsof -i :8000

   # 修改启动端口
   uvicorn app.main:app --port 8001
   ```

## 📝 开发规范

- 遵循PEP 8代码规范
- 使用类型提示增强代码可读性
- 编写详细的文档字符串
- 添加适当的日志记录
- 编写单元测试

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。