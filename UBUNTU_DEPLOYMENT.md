# H-System EDR 平台 Ubuntu 部署指南

本文档说明如何在 Ubuntu 系统中部署和测试 H-System EDR 平台的前后端服务。

## 🚀 快速开始

### 1. 系统要求

- Ubuntu 20.04 LTS 或更高版本
- Python 3.8+
- Node.js 18+
- npm 8+

### 2. 安装系统依赖

```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y

# 安装 Python 3 和 pip
sudo apt install -y python3 python3-pip python3-venv

# 安装 Node.js 和 npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 安装其他必要工具
sudo apt install -y curl git build-essential
```

### 3. 克隆项目

```bash
git clone <your-repository-url>
cd honeypot-platform
```

## 🔧 自动部署

### 使用启动脚本（推荐）

我们提供了一个自动化的启动脚本来简化部署过程：

```bash
# 给脚本执行权限
chmod +x start_services.sh

# 启动所有服务
./start_services.sh start

# 查看服务状态
./start_services.sh status

# 运行连通性测试
./start_services.sh test

# 停止所有服务
./start_services.sh stop

# 重启所有服务
./start_services.sh restart
```

### 启动脚本功能

- ✅ 自动检查系统依赖
- ✅ 自动安装 Python 和 Node.js 依赖
- ✅ 自动启动前后端服务
- ✅ 自动检查服务状态
- ✅ 提供连通性测试
- ✅ 优雅的服务停止和重启

## 🛠️ 手动部署

### 1. 后端服务

```bash
cd backend

# 创建虚拟环境（可选）
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. 前端服务

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 🧪 测试连通性

### 1. 使用 Python 测试脚本

```bash
cd backend

# 安装测试依赖
pip install aiohttp

# 运行连通性测试
python3 test_connectivity.py
```

### 2. 使用 JavaScript 测试脚本

```bash
cd frontend

# 安装测试依赖
npm install axios

# 运行连通性测试
node test_connectivity.js
```

### 3. 手动测试

```bash
# 测试后端健康状态
curl http://localhost:8000/health

# 测试后端API
curl http://localhost:8000/api/v1

# 测试前端代理
curl http://localhost:3000/api/v1

# 测试前端页面
curl http://localhost:3000
```

## 📊 服务状态检查

### 端口占用检查

```bash
# 检查端口8000（后端）
sudo lsof -i :8000

# 检查端口3000（前端）
sudo lsof -i :3000

# 检查所有监听端口
sudo netstat -tlnp
```

### 进程状态检查

```bash
# 查看Python进程
ps aux | grep python

# 查看Node.js进程
ps aux | grep node

# 查看特定进程
ps aux | grep uvicorn
ps aux | grep vite
```

## 🔍 故障排除

### 常见问题

#### 1. 端口被占用

```bash
# 查找占用端口的进程
sudo lsof -i :8000
sudo lsof -i :3000

# 杀死占用端口的进程
sudo kill -9 <PID>
```

#### 2. 依赖安装失败

```bash
# 清理 npm 缓存
npm cache clean --force

# 清理 pip 缓存
pip cache purge

# 重新安装依赖
rm -rf node_modules package-lock.json
npm install
```

#### 3. 权限问题

```bash
# 修复文件权限
sudo chown -R $USER:$USER .

# 修复脚本权限
chmod +x start_services.sh
```

#### 4. 服务启动失败

```bash
# 查看后端日志
tail -f backend/backend.log

# 查看前端日志
tail -f frontend/frontend.log

# 检查配置文件
cat backend/app/core/config.py
cat frontend/vite.config.ts
```

### 日志文件位置

- 后端日志：`backend/backend.log`
- 前端日志：`frontend/frontend.log`
- 启动脚本日志：`start_services.log`

## 🌐 网络配置

### 防火墙设置

```bash
# 允许端口8000（后端）
sudo ufw allow 8000

# 允许端口3000（前端）
sudo ufw allow 3000

# 启用防火墙
sudo ufw enable

# 查看防火墙状态
sudo ufw status
```

### 反向代理配置（可选）

如果需要通过 Nginx 反向代理访问：

```nginx
# /etc/nginx/sites-available/hsystem
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📝 环境变量配置

### 后端环境变量

创建 `backend/.env` 文件：

```env
# 数据库配置
DATABASE_URL=sqlite:///./hsystem.db
# 或者使用 PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost/hsystem

# 开发配置
DEBUG=true
LOG_LEVEL=INFO

# JWT配置
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=120
```

### 前端环境变量

创建 `frontend/.env` 文件：

```env
# API配置
VITE_API_BASE_URL=http://localhost:8000

# 应用配置
VITE_APP_TITLE=H-System EDR平台
VITE_APP_DESCRIPTION=蜜罐安全管理系统

# 构建配置
VITE_BUILD_SOURCEMAP=true
VITE_BUILD_DROP_CONSOLE=false
```

## 🚀 生产环境部署

### 使用 PM2 管理 Node.js 进程

```bash
# 安装 PM2
npm install -g pm2

# 启动前端服务
cd frontend
pm2 start npm --name "hsystem-frontend" -- run dev

# 启动后端服务
cd ../backend
pm2 start "python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000" --name "hsystem-backend"

# 查看进程状态
pm2 status

# 保存进程配置
pm2 save
pm2 startup
```

### 使用 systemd 管理服务

创建服务文件 `/etc/systemd/system/hsystem-backend.service`：

```ini
[Unit]
Description=H-System Backend Service
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/your/project/backend
ExecStart=/path/to/your/project/backend/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

## 📚 更多资源

- [项目架构说明](ARCHITECTURE_COMPARISON.md)
- [集成检查清单](INTEGRATION_CHECKLIST.md)
- [后端API文档](http://localhost:8000/docs)
- [前端开发文档](frontend/README.md)

## 🤝 获取帮助

如果遇到问题，请：

1. 查看日志文件
2. 运行连通性测试
3. 检查系统依赖
4. 查看故障排除部分
5. 提交 Issue 到项目仓库

---

**注意**：本文档假设您在 Ubuntu 系统中运行。如果在其他 Linux 发行版中运行，可能需要调整相应的包管理器命令。
