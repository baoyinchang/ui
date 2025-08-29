#!/bin/bash

# H-System EDR平台 - 项目管理脚本
# 统一的项目管理入口

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

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

print_header() {
    echo -e "${CYAN}$1${NC}"
}

show_banner() {
    echo ""
    echo "========================================"
    echo "  H-System EDR平台 - 项目管理"
    echo "========================================"
    echo ""
}

show_usage() {
    show_banner
    echo "使用方法:"
    echo "  ./manage.sh [命令] [选项]"
    echo ""
    echo "🚀 开发命令:"
    echo "  setup     - 初始化项目环境"
    echo "  dev       - 启动开发服务器"
    echo "  build     - 构建生产版本"
    echo "  preview   - 预览构建结果"
    echo ""
    echo "🧪 测试命令:"
    echo "  test      - 运行所有测试"
    echo "  test:unit - 运行单元测试"
    echo "  test:e2e  - 运行端到端测试"
    echo "  lint      - 代码检查"
    echo "  type      - 类型检查"
    echo ""
    echo "🔧 维护命令:"
    echo "  clean     - 清理项目文件"
    echo "  deps      - 更新依赖包"
    echo "  info      - 显示项目信息"
    echo "  doctor    - 项目健康检查"
    echo ""
    echo "📚 帮助命令:"
    echo "  help      - 显示此帮助信息"
    echo "  version   - 显示版本信息"
    echo ""
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

check_environment() {
    print_info "检查开发环境..."
    
    if ! command_exists node; then
        print_error "未找到Node.js，请先安装Node.js 18+"
        exit 1
    fi
    
    if ! command_exists npm; then
        print_error "未找到npm"
        exit 1
    fi
    
    NODE_VERSION=$(node --version)
    NPM_VERSION=$(npm --version)
    
    print_success "Node.js: $NODE_VERSION"
    print_success "npm: $NPM_VERSION"
}

setup_project() {
    show_banner
    print_header "🔧 初始化项目环境"
    echo ""
    
    check_environment
    
    print_info "安装项目依赖..."
    if [ ! -d "node_modules" ]; then
        npm install
    else
        npm update
    fi
    print_success "依赖安装完成"
    
    print_info "配置环境文件..."
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp ".env.example" ".env"
        else
            cat > .env << 'EOF'
# H-System EDR平台 - 开发环境配置
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=H-System EDR平台
VITE_APP_VERSION=1.0.0
VITE_APP_DESCRIPTION=蜜罐安全管理系统
VITE_DEV_MOCK=false
VITE_DEV_PROXY=true
VITE_BUILD_SOURCEMAP=false
VITE_BUILD_DROP_CONSOLE=true
EOF
        fi
        print_success "环境配置文件已创建"
    else
        print_success "环境配置文件已存在"
    fi
    
    # 设置脚本执行权限
    chmod +x *.sh 2>/dev/null || true
    
    print_success "项目初始化完成！"
    echo ""
    print_info "运行 './manage.sh dev' 启动开发服务器"
}

show_project_info() {
    show_banner
    print_header "📋 项目信息"
    echo ""
    
    if [ -f "package.json" ]; then
        NAME=$(grep '"name"' package.json | cut -d'"' -f4)
        VERSION=$(grep '"version"' package.json | cut -d'"' -f4)
        echo "项目名称: $NAME"
        echo "项目版本: $VERSION"
    fi
    
    if command_exists node; then
        echo "Node.js版本: $(node --version)"
    fi
    
    if command_exists npm; then
        echo "npm版本: $(npm --version)"
    fi
    
    if [ -d "node_modules" ]; then
        DEPS_COUNT=$(find node_modules -maxdepth 1 -type d | wc -l)
        echo "依赖包数量: $((DEPS_COUNT - 1))"
    fi
    
    if [ -d "dist" ]; then
        DIST_SIZE=$(du -sh dist 2>/dev/null | cut -f1 || echo "未知")
        echo "构建大小: $DIST_SIZE"
    fi
    
    echo ""
}

clean_project() {
    print_info "清理项目文件..."
    
    # 清理构建文件
    if [ -d "dist" ]; then
        rm -rf dist
        print_success "已清理构建文件"
    fi
    
    # 清理缓存
    if [ -d "node_modules/.cache" ]; then
        rm -rf node_modules/.cache
        print_success "已清理缓存文件"
    fi
    
    # 清理日志文件
    find . -name "*.log" -type f -delete 2>/dev/null || true
    
    print_success "项目清理完成"
}

doctor_check() {
    show_banner
    print_header "🏥 项目健康检查"
    echo ""
    
    local issues=0
    
    # 检查Node.js版本
    if command_exists node; then
        NODE_VERSION=$(node --version | sed 's/v//')
        MAJOR_VERSION=$(echo $NODE_VERSION | cut -d. -f1)
        if [ "$MAJOR_VERSION" -lt 18 ]; then
            print_warning "Node.js版本过低，建议升级到18+"
            issues=$((issues + 1))
        else
            print_success "Node.js版本正常"
        fi
    else
        print_error "未找到Node.js"
        issues=$((issues + 1))
    fi
    
    # 检查依赖
    if [ -d "node_modules" ]; then
        print_success "依赖已安装"
    else
        print_warning "依赖未安装，运行 './manage.sh setup'"
        issues=$((issues + 1))
    fi
    
    # 检查环境配置
    if [ -f ".env" ]; then
        print_success "环境配置文件存在"
    else
        print_warning "环境配置文件缺失"
        issues=$((issues + 1))
    fi
    
    # 检查TypeScript配置
    if [ -f "tsconfig.json" ]; then
        print_success "TypeScript配置正常"
    else
        print_warning "TypeScript配置缺失"
        issues=$((issues + 1))
    fi
    
    echo ""
    if [ $issues -eq 0 ]; then
        print_success "项目健康状况良好！"
    else
        print_warning "发现 $issues 个问题，建议修复"
    fi
}

# 主逻辑
case "${1:-help}" in
    "setup")
        setup_project
        ;;
    "dev")
        check_environment
        print_info "启动开发服务器..."
        npm run dev
        ;;
    "build")
        check_environment
        print_info "构建生产版本..."
        npm run build
        ;;
    "preview")
        check_environment
        print_info "预览构建结果..."
        npm run preview
        ;;
    "test")
        check_environment
        print_info "运行所有测试..."
        npm run test
        ;;
    "test:unit")
        check_environment
        npm run test:unit
        ;;
    "test:e2e")
        check_environment
        npm run test:e2e
        ;;
    "lint")
        check_environment
        npm run lint
        ;;
    "type")
        check_environment
        npm run type-check
        ;;
    "clean")
        clean_project
        ;;
    "deps")
        check_environment
        print_info "更新依赖包..."
        npm update
        print_success "依赖更新完成"
        ;;
    "info")
        show_project_info
        ;;
    "doctor")
        doctor_check
        ;;
    "version")
        if [ -f "package.json" ]; then
            VERSION=$(grep '"version"' package.json | cut -d'"' -f4)
            echo "H-System EDR平台 v$VERSION"
        else
            echo "H-System EDR平台"
        fi
        ;;
    "help"|*)
        show_usage
        ;;
esac
