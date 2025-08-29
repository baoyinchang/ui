#!/bin/bash

# H-System EDR平台 - 测试套件脚本

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

show_usage() {
    echo ""
    echo "========================================"
    echo "  H-System EDR平台 - 测试套件"
    echo "========================================"
    echo ""
    echo "使用方法:"
    echo "  ./test.sh [命令]"
    echo ""
    echo "可用命令:"
    echo "  unit      - 运行单元测试"
    echo "  e2e       - 运行端到端测试"
    echo "  coverage  - 运行测试覆盖率"
    echo "  lint      - 代码检查"
    echo "  type      - 类型检查"
    echo "  all       - 运行所有测试"
    echo "  watch     - 监视模式运行测试"
    echo ""
}

if [ $# -eq 0 ]; then
    show_usage
    exit 0
fi

echo ""
echo "========================================"
echo "  H-System EDR平台 - 测试套件"
echo "========================================"
echo ""

# 步骤1: 检查测试环境
print_step "[1/2] 检查测试环境..."
if ! command_exists node; then
    print_error "未找到Node.js"
    exit 1
fi

if ! command_exists npm; then
    print_error "未找到npm"
    exit 1
fi

if [ ! -d "node_modules" ]; then
    print_info "安装依赖包..."
    if ! npm install; then
        print_error "依赖安装失败"
        exit 1
    fi
fi

print_success "测试环境检查完成"
echo ""

# 步骤2: 执行测试命令
print_step "[2/2] 执行测试命令..."

case "$1" in
    "unit")
        print_info "运行单元测试..."
        npm run test:unit
        ;;
    "e2e")
        print_info "运行端到端测试..."
        npm run test:e2e
        ;;
    "coverage")
        print_info "运行测试覆盖率..."
        npm run test:coverage
        ;;
    "lint")
        print_info "代码检查..."
        npm run lint
        ;;
    "type")
        print_info "类型检查..."
        npm run type-check
        ;;
    "watch")
        print_info "监视模式运行测试..."
        npm run test:watch
        ;;
    "all")
        print_info "运行所有测试..."
        echo ""
        
        print_step "[1/5] 类型检查..."
        if ! npm run type-check; then
            print_error "类型检查失败"
            exit 1
        fi
        print_success "类型检查通过"
        echo ""
        
        print_step "[2/5] 代码检查..."
        if ! npm run lint; then
            print_error "代码检查失败"
            exit 1
        fi
        print_success "代码检查通过"
        echo ""
        
        print_step "[3/5] 单元测试..."
        if ! npm run test:unit; then
            print_error "单元测试失败"
            exit 1
        fi
        print_success "单元测试通过"
        echo ""
        
        print_step "[4/5] 测试覆盖率..."
        if ! npm run test:coverage; then
            print_error "测试覆盖率检查失败"
            exit 1
        fi
        print_success "测试覆盖率检查通过"
        echo ""
        
        print_step "[5/5] 构建测试..."
        if ! npm run build; then
            print_error "构建测试失败"
            exit 1
        fi
        print_success "构建测试通过"
        echo ""
        
        echo "========================================"
        print_success "所有测试通过！"
        echo "========================================"
        ;;
    *)
        print_error "未知命令: $1"
        show_usage
        exit 1
        ;;
esac

if [ $? -eq 0 ]; then
    echo ""
    print_success "测试完成"
else
    echo ""
    print_error "测试失败"
    exit 1
fi
