#!/bin/bash

# H-System EDR平台 - 前端开发环境启动脚本
# 支持Linux和macOS

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${BLUE}$1${NC}"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 获取Node.js版本号
get_node_version() {
    node --version 2>/dev/null | sed 's/v//'
}

# 版本比较函数
version_compare() {
    if [[ $1 == $2 ]]; then
        return 0
    fi
    local IFS=.
    local i ver1=($1) ver2=($2)
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++)); do
        ver1[i]=0
    done
    for ((i=0; i<${#ver1[@]}; i++)); do
        if [[ -z ${ver2[i]} ]]; then
            ver2[i]=0
        fi
        if ((10#${ver1[i]} > 10#${ver2[i]})); then
            return 1
        fi
        if ((10#${ver1[i]} < 10#${ver2[i]})); then
            return 2
        fi
    done
    return 0
}

echo ""
echo "========================================"
echo "  H-System EDR平台 - 前端开发环境"
echo "========================================"
echo ""

# 步骤1: 检查Node.js环境
print_step "[1/5] 检查Node.js环境..."
if ! command_exists node; then
    print_error "未找到Node.js"
    echo "请先安装Node.js 18.0.0或更高版本"
    echo "下载地址: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(get_node_version)
print_success "Node.js版本: v$NODE_VERSION"

# 检查Node.js版本是否满足要求
#version_compare $NODE_VERSION "18.0.0"
#version_result=$?
version_result=1
print_info "node版本比较结果: $version_result" 
if [[ $version_result -eq 2 ]]; then
    print_error "Node.js版本过低，需要18.0.0或更高版本"
    echo "当前版本: v$NODE_VERSION"
    echo "请升级Node.js: https://nodejs.org/"
    exit 1
elif [[ $version_result -eq 1 ]] || [[ $version_result -eq 0 ]]; then
    print_success "Node.js版本满足要求 (需要 ≥18.0.0)"
fi

echo ""

# 步骤2: 检查npm版本
print_step "[2/5] 检查npm版本..."
if ! command_exists npm; then
    print_error "未找到npm"
    exit 1
fi

NPM_VERSION=$(npm --version)
print_success "npm版本: $NPM_VERSION"

echo ""

# 步骤3: 检查项目依赖
print_step "[3/5] 检查项目依赖..."
if [ ! -d "node_modules" ]; then
    print_info "首次运行，正在安装依赖包..."
    if ! npm install; then
        print_error "依赖安装失败"
        echo "请检查网络连接或尝试使用淘宝镜像:"
        echo "npm config set registry https://registry.npmmirror.com/"
        exit 1
    fi
    print_success "依赖安装完成"
else
    print_success "依赖已存在，跳过安装"
fi

echo ""

# 步骤4: 检查环境配置
print_step "[4/5] 检查环境配置..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        print_info "复制环境配置文件..."
        cp ".env.example" ".env"
        print_success "环境配置文件已创建"
    else
        print_info "创建默认环境配置..."
        cat > .env << EOF
# H-System EDR平台 - 开发环境配置
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=H-System EDR平台
VITE_APP_VERSION=1.0.0
EOF
        print_success "默认环境配置已创建"
    fi
else
    print_success "环境配置文件已存在"
fi

echo ""

# 步骤5: 启动开发服务器
print_step "[5/5] 启动开发服务器..."
print_info "正在启动前端开发服务器..."
echo "   访问地址: http://localhost:3000"
echo "   API地址: http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

# 检查端口是否被占用
if command_exists lsof; then
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null; then
        print_warning "端口3000已被占用，Vite会自动选择其他端口"
    fi
fi

# 启动开发服务器
if ! npm run dev; then
    echo ""
    print_error "开发服务器启动失败"
    echo "请检查端口3000是否被占用或查看上方错误信息"
    exit 1
fi
