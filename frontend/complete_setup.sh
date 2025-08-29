#!/bin/bash

# 完整的前端设置和启动脚本
# 适用于Ubuntu 24系统

set -e

echo "🚀 H-System EDR 前端完整设置"
echo "============================="

# 检查系统信息
echo "📋 系统信息:"
echo "   操作系统: $(uname -s)"
echo "   架构: $(uname -m)"
echo "   发行版: $(lsb_release -d 2>/dev/null | cut -f2 || echo 'Unknown')"

# 检查Node.js
echo ""
echo "🔍 检查Node.js环境..."

if ! command -v node >/dev/null 2>&1; then
    echo "❌ 未找到Node.js"
    echo "请安装Node.js:"
    echo "   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -"
    echo "   sudo apt-get install -y nodejs"
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node.js版本: $NODE_VERSION"

# 检查npm
if ! command -v npm >/dev/null 2>&1; then
    echo "❌ 未找到npm"
    echo "请安装npm:"
    echo "   sudo apt-get install -y npm"
    exit 1
fi

NPM_VERSION=$(npm --version)
echo "✅ npm版本: $NPM_VERSION"

# 检查当前目录
echo ""
echo "📁 检查项目文件..."

if [ ! -f "package.json" ]; then
    echo "❌ 未找到package.json"
    echo "请确保在frontend目录中运行此脚本"
    exit 1
fi

echo "✅ package.json存在"

# 清理旧的node_modules（如果存在）
if [ -d "node_modules" ]; then
    echo "🧹 清理旧的node_modules..."
    rm -rf node_modules
    echo "✅ 清理完成"
fi

# 清理package-lock.json（如果存在）
if [ -f "package-lock.json" ]; then
    echo "🧹 清理package-lock.json..."
    rm -f package-lock.json
    echo "✅ 清理完成"
fi

# 设置npm镜像（加速下载）
echo ""
echo "🔧 配置npm镜像..."
npm config set registry https://registry.npmmirror.com/
echo "✅ 已设置为淘宝镜像"

# 安装依赖
echo ""
echo "📦 安装项目依赖..."
echo "这可能需要几分钟时间，请耐心等待..."

if npm install; then
    echo "✅ 依赖安装成功"
else
    echo "❌ 依赖安装失败"
    echo ""
    echo "尝试解决方案:"
    echo "1. 清理npm缓存: npm cache clean --force"
    echo "2. 删除node_modules: rm -rf node_modules"
    echo "3. 重新安装: npm install"
    exit 1
fi

# 验证安装
echo ""
echo "🔍 验证安装结果..."

if [ ! -d "node_modules" ]; then
    echo "❌ node_modules目录不存在"
    exit 1
fi

# 检查关键包
key_packages=("vue" "vite" "element-plus" "typescript")
for package in "${key_packages[@]}"; do
    if [ -d "node_modules/$package" ]; then
        echo "✅ $package"
    else
        echo "❌ $package 缺失"
        exit 1
    fi
done

# 创建环境文件（如果不存在）
if [ ! -f ".env.development" ]; then
    echo ""
    echo "📝 创建环境配置..."
    cat > .env.development << 'EOF'
# 开发环境配置
VITE_APP_TITLE=H-System EDR平台
VITE_APP_DESCRIPTION=蜜罐安全管理系统
VITE_APP_VERSION=1.0.0

# API配置
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# 开发服务器配置
VITE_DEV_PORT=3000
VITE_DEV_OPEN=false
VITE_DEV_PROXY=true

# 构建配置
VITE_BUILD_SOURCEMAP=true
VITE_BUILD_DROP_CONSOLE=false

# 功能开关
VITE_DEV_MOCK=false
EOF
    echo "✅ 环境配置已创建"
fi

# 运行最终验证
echo ""
echo "🔍 运行最终验证..."
if python3 verify_setup.py; then
    echo "✅ 验证通过"
else
    echo "❌ 验证失败"
    exit 1
fi

# 启动开发服务器
echo ""
echo "🌐 启动开发服务器..."
echo "   前端地址: http://localhost:3000"
echo "   后端地址: http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

# 启动
exec npm run dev
