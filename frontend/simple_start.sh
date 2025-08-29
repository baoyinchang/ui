#!/bin/bash

# 简化的前端启动脚本
# 用于快速启动和调试

set -e

echo "🚀 H-System EDR 前端快速启动"
echo "================================"

# 检查Node.js
if ! command -v node >/dev/null 2>&1; then
    echo "❌ 未找到Node.js，请先安装Node.js"
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node.js版本: $NODE_VERSION"

# 检查npm
if ! command -v npm >/dev/null 2>&1; then
    echo "❌ 未找到npm"
    exit 1
fi

NPM_VERSION=$(npm --version)
echo "✅ npm版本: $NPM_VERSION"

# 检查package.json
if [ ! -f "package.json" ]; then
    echo "❌ 未找到package.json文件"
    echo "请确保在frontend目录中运行此脚本"
    exit 1
fi

# 安装依赖（如果需要）
if [ ! -d "node_modules" ]; then
    echo "📦 安装依赖包..."
    npm install
    echo "✅ 依赖安装完成"
else
    echo "✅ 依赖已存在"
fi

# 创建环境文件（如果不存在）
if [ ! -f ".env.development" ]; then
    echo "📝 创建环境配置文件..."
    cat > .env.development << EOF
# 开发环境配置
VITE_APP_TITLE=H-System EDR平台
VITE_APP_DESCRIPTION=蜜罐安全管理系统
VITE_APP_VERSION=1.0.0

# API配置
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# 开发服务器配置
VITE_DEV_PORT=3000
VITE_DEV_OPEN=true
VITE_DEV_PROXY=true

# 构建配置
VITE_BUILD_SOURCEMAP=true
VITE_BUILD_DROP_CONSOLE=false

# 功能开关
VITE_DEV_MOCK=false
EOF
    echo "✅ 环境配置文件已创建"
fi

echo ""
echo "🌐 启动开发服务器..."
echo "   前端地址: http://localhost:3000"
echo "   后端地址: http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

# 启动开发服务器
exec npm run dev
