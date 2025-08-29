#!/bin/bash

# 最终设置和启动脚本
# 完成最后的依赖安装并启动开发服务器

set -e

echo "🎉 H-System EDR 前端最终设置"
echo "============================"

# 检查Node.js环境
echo "🔍 检查Node.js环境..."
if ! command -v node >/dev/null 2>&1; then
    echo "❌ 未找到Node.js"
    exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
    echo "❌ 未找到npm"
    exit 1
fi

NODE_VERSION=$(node --version)
NPM_VERSION=$(npm --version)
echo "✅ Node.js: $NODE_VERSION"
echo "✅ npm: $NPM_VERSION"

# 检查项目文件
echo ""
echo "📁 检查项目文件..."
if [ ! -f "package.json" ]; then
    echo "❌ package.json不存在"
    exit 1
fi
echo "✅ package.json存在"

# 运行最终验证
echo ""
echo "🔍 运行最终验证..."
if ! python3 verify_setup.py | grep -q "总计: 5个通过, 1个失败"; then
    echo "❌ 项目验证失败，请检查文件结构"
    exit 1
fi
echo "✅ 项目结构验证通过"

# 安装依赖（如果需要）
if [ ! -d "node_modules" ]; then
    echo ""
    echo "📦 安装项目依赖..."
    echo "这可能需要几分钟时间..."
    
    # 设置npm镜像
    npm config set registry https://registry.npmmirror.com/
    
    if npm install; then
        echo "✅ 依赖安装成功"
    else
        echo "❌ 依赖安装失败"
        echo ""
        echo "尝试解决方案:"
        echo "1. 清理缓存: npm cache clean --force"
        echo "2. 删除node_modules: rm -rf node_modules"
        echo "3. 重新安装: npm install"
        exit 1
    fi
else
    echo "✅ 依赖已存在"
fi

# 最终验证
echo ""
echo "🔍 最终验证..."
if python3 verify_setup.py | grep -q "🎉 所有检查都通过了"; then
    echo "✅ 所有检查通过"
else
    echo "❌ 最终验证失败"
    exit 1
fi

# 显示项目信息
echo ""
echo "📊 项目信息:"
echo "   项目名称: H-System EDR 前端"
echo "   开发框架: Vue 3 + TypeScript + Element Plus"
echo "   构建工具: Vite"
echo "   包管理器: npm"

# 启动开发服务器
echo ""
echo "🚀 启动开发服务器..."
echo "   前端地址: http://localhost:3000"
echo "   后端地址: http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

# 启动
exec npm run dev
