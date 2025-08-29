#!/bin/bash

# H-System EDR平台 - 生产构建脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${BLUE}$1${NC}"
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo ""
echo "========================================"
echo "  H-System EDR平台 - 生产构建"
echo "========================================"
echo ""

# 步骤1: 检查构建环境
print_step "[1/4] 检查构建环境..."
if ! command_exists node; then
    print_error "未找到Node.js"
    exit 1
fi

NODE_VERSION=$(node --version)
print_success "Node.js版本: $NODE_VERSION"

if ! command_exists npm; then
    print_error "未找到npm"
    exit 1
fi

NPM_VERSION=$(npm --version)
print_success "npm版本: $NPM_VERSION"

echo ""

# 步骤2: 检查项目依赖
print_step "[2/4] 检查项目依赖..."
if [ ! -d "node_modules" ]; then
    print_info "安装依赖包..."
    if ! npm ci; then
        print_error "依赖安装失败"
        exit 1
    fi
    print_success "依赖安装完成"
else
    print_success "依赖已存在"
fi

echo ""

# 步骤3: 清理旧构建文件
print_step "[3/4] 清理旧构建文件..."
if [ -d "dist" ]; then
    rm -rf dist
    print_success "已清理旧构建文件"
else
    print_success "无需清理"
fi

echo ""

# 步骤4: 开始构建
print_step "[4/4] 开始构建生产版本..."
print_info "正在构建，请稍候..."

# 设置生产环境
export NODE_ENV=production

# 执行构建
if ! npm run build; then
    echo ""
    print_error "构建失败"
    echo "请检查代码错误或依赖问题"
    exit 1
fi

echo ""
echo "========================================"
print_success "构建完成！"
echo "========================================"
echo ""

# 显示构建统计信息
if [ -d "dist" ]; then
    echo "📁 构建文件位置: dist/"
    echo "📊 构建统计信息:"
    
    FILE_COUNT=$(find dist -type f | wc -l)
    echo "   文件数量: $FILE_COUNT"
    
    if command_exists du; then
        TOTAL_SIZE=$(du -sh dist | cut -f1)
        echo "   总大小: $TOTAL_SIZE"
    fi
    
    echo ""
    echo "📋 主要文件:"
    if [ -f "dist/index.html" ]; then
        echo "   ✅ index.html"
    fi
    
    if [ -d "dist/assets" ]; then
        JS_COUNT=$(find dist/assets -name "*.js" | wc -l)
        CSS_COUNT=$(find dist/assets -name "*.css" | wc -l)
        echo "   ✅ JavaScript文件: $JS_COUNT"
        echo "   ✅ CSS文件: $CSS_COUNT"
    fi
fi

echo ""
echo "🚀 部署建议:"
echo "   1. 将dist目录内容上传到Web服务器"
echo "   2. 配置Nginx或Apache服务器"
echo "   3. 确保API服务器正常运行"
echo "   4. 配置HTTPS证书（生产环境）"
echo ""

echo "📋 预览构建结果:"
echo "   运行 'npm run preview' 可本地预览构建结果"
echo ""

# 检查是否需要预览
read -p "是否要预览构建结果？(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "启动预览服务器..."
    npm run preview
fi
