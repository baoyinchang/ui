# 🔍 前后端集成检查清单

## 📋 检查概览

### ✅ 已修复的问题
1. **响应格式统一** - 创建了统一的 `BaseResponse` 格式
2. **API路径配置** - 修复了Vite代理配置
3. **类型定义匹配** - 创建了匹配的schemas
4. **环境变量配置** - 添加了开发环境配置

### ⚠️ 需要注意的问题

## 🚀 启动前检查

### 1. 后端启动检查
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**检查项目**:
- [ ] 服务启动无错误
- [ ] 数据库连接正常
- [ ] API文档可访问 (http://localhost:8000/docs)

### 2. 前端启动检查
```bash
cd frontend
npm install
npm run dev
```

**检查项目**:
- [ ] 依赖安装成功
- [ ] 开发服务器启动正常
- [ ] 页面可正常访问 (http://localhost:3000)

## 🔧 关键配置检查

### 1. 后端配置 (`backend/app/core/config.py`)
```python
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"  # ✅ 正确
    PROJECT_NAME: str = "H-System蜜罐EDR平台"
    
    # 数据库配置
    POSTGRES_SERVER: str = "localhost"  # 🔧 开发环境改为localhost
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "hsystem"
```

### 2. 前端API配置 (`frontend/src/api/request.ts`)
```typescript
const baseURL = '/api/v1'  // ✅ 正确，匹配后端路径
```

### 3. Vite代理配置 (`frontend/vite.config.ts`)
```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    // ✅ 不重写路径，保持/api前缀
  }
}
```

## 📡 API通信检查

### 1. 响应格式统一
**前端期望格式**:
```typescript
interface ResponseData<T> {
  code: number
  message: string
  data: T
  success: boolean
  timestamp: string
}
```

**后端返回格式** (已修复):
```python
class BaseResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: Optional[T] = None
    success: bool = True
    timestamp: datetime = None
```

### 2. 登录接口测试
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test"}'
```

**预期响应**:
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "...",
    "refresh_token": "...",
    "token_type": "bearer",
    "expires_in": 7200,
    "user": {...}
  },
  "success": true,
  "timestamp": "2024-01-01T00:00:00"
}
```

## 🗄️ 数据库检查

### 1. PostgreSQL连接
```bash
# 检查PostgreSQL是否运行
pg_isready -h localhost -p 5432

# 连接数据库
psql -h localhost -U postgres -d hsystem
```

### 2. 数据库迁移
```bash
cd backend
alembic upgrade head
```

## 🔐 认证流程检查

### 1. JWT令牌配置
- [ ] SECRET_KEY已设置
- [ ] 令牌过期时间合理 (2小时)
- [ ] 刷新令牌机制正常

### 2. 密码加密
- [ ] 使用bcrypt加密
- [ ] 密码强度验证

## 🌐 CORS配置检查

### 后端CORS设置 (`backend/app/main.py`)
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📝 类型定义检查

### 1. 前端类型定义 (`frontend/src/types/api.ts`)
```typescript
// 用户类型
export interface User {
  id: number
  username: string
  email: string
  full_name?: string
  is_active: boolean
  role: string
  created_at: string
  updated_at: string
}

// 登录响应类型
export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
  user: User
}
```

### 2. 后端Schema定义 (`backend/app/schemas/`)
- [ ] 用户模型匹配
- [ ] 认证模型匹配
- [ ] 响应格式统一

## 🧪 测试检查

### 1. 运行集成检查脚本
```bash
python scripts/check-integration.py
```

### 2. 运行前端检查脚本
```bash
node scripts/check-frontend.js
```

### 3. 手动测试流程
1. [ ] 访问登录页面
2. [ ] 输入用户名密码
3. [ ] 检查网络请求
4. [ ] 验证响应格式
5. [ ] 确认页面跳转

## 🚨 常见问题及解决方案

### 1. CORS错误
**问题**: `Access to XMLHttpRequest at 'http://localhost:8000/api/v1/auth/login' from origin 'http://localhost:3000' has been blocked by CORS policy`

**解决方案**:
- 检查后端CORS配置
- 确认前端地址在允许列表中

### 2. 404错误
**问题**: API请求返回404

**解决方案**:
- 检查API路径是否正确
- 确认Vite代理配置
- 验证后端路由注册

### 3. 类型错误
**问题**: TypeScript类型不匹配

**解决方案**:
- 对比前后端类型定义
- 更新接口类型
- 运行类型检查

### 4. 认证失败
**问题**: 登录请求返回401

**解决方案**:
- 检查用户名密码
- 确认数据库中有测试用户
- 验证密码加密逻辑

## 📊 性能检查

### 1. 前端构建检查
```bash
cd frontend
npm run build
npm run preview
```

### 2. 后端性能检查
- [ ] 数据库查询优化
- [ ] API响应时间
- [ ] 内存使用情况

## 🔄 持续集成

### 1. 代码质量检查
```bash
# 前端
cd frontend
npm run lint
npm run type-check

# 后端
cd backend
black .
isort .
pytest
```

### 2. 自动化测试
- [ ] 单元测试覆盖率 > 80%
- [ ] 集成测试通过
- [ ] E2E测试通过

## ✅ 最终检查清单

在部署前，确保以下所有项目都已完成：

- [ ] 后端服务正常启动
- [ ] 前端应用正常启动
- [ ] 数据库连接正常
- [ ] API接口可正常访问
- [ ] 登录流程完整可用
- [ ] CORS配置正确
- [ ] 类型定义匹配
- [ ] 错误处理完善
- [ ] 性能表现良好
- [ ] 代码质量检查通过

## 🎯 下一步行动

1. **立即执行**: 运行检查脚本，修复发现的问题
2. **短期目标**: 完善测试覆盖率，优化性能
3. **长期规划**: 建立CI/CD流程，自动化部署

---

**注意**: 这个检查清单应该在每次重大更改后执行，确保系统的稳定性和可靠性。
