#!/bin/bash

# H-System EDR平台服务启动脚本
# 在 Ubuntu 系统中运行此脚本来启动前后端服务

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    log_info "检查系统依赖..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 未安装，请先安装 Python3"
        exit 1
    fi
    
    # 检查Node.js
    if ! command -v node &> /dev/null; then
        log_error "Node.js 未安装，请先安装 Node.js"
        exit 1
    fi
    
    # 检查npm
    if ! command -v npm &> /dev/null; then
        log_error "npm 未安装，请先安装 npm"
        exit 1
    fi
    
    log_success "系统依赖检查通过"
}

# 安装Python依赖
install_python_deps() {
    log_info "安装Python依赖..."
    
    if [ -f "backend/requirements.txt" ]; then
        cd backend
        pip3 install --break-system-packages -r requirements.txt
        cd ..
        log_success "Python依赖安装完成"
    else
        log_warning "未找到 requirements.txt 文件"
    fi
}

# 安装Node.js依赖
install_node_deps() {
    log_info "安装Node.js依赖..."
    
    if [ -f "frontend/package.json" ]; then
        cd frontend
        npm install
        cd ..
        log_success "Node.js依赖安装完成"
    else
        log_warning "未找到 package.json 文件"
    fi
}

# 启动后端服务
start_backend() {
    log_info "启动后端服务..."
    
    cd backend
    
    # 检查是否有虚拟环境
    if [ -d "venv" ] || [ -d ".venv" ]; then
        log_info "检测到虚拟环境，激活中..."
        if [ -d "venv" ]; then
            source venv/bin/activate
        else
            source .venv/bin/activate
        fi
    fi
    
    # 启动后端服务
    nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > backend.pid
    
    cd ..
    
    # 等待服务启动
    log_info "等待后端服务启动..."
    sleep 5
    
    # 检查服务状态
    if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
        log_success "后端服务启动成功 (PID: $BACKEND_PID)"
    else
        log_error "后端服务启动失败，请检查日志文件 backend/backend.log"
        exit 1
    fi
}

# 启动前端服务
start_frontend() {
    log_info "启动前端服务..."
    
    cd frontend
    
    # 启动前端服务
    nohup npm run dev > frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > frontend.pid
    
    cd ..
    
    # 等待服务启动
    log_info "等待前端服务启动..."
    sleep 10
    
    # 检查服务状态
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        log_success "前端服务启动成功 (PID: $FRONTEND_PID)"
    else
        log_error "前端服务启动失败，请检查日志文件 frontend/frontend.log"
        exit 1
    fi
}

# 检查端口占用
check_ports() {
    log_info "检查端口占用..."
    
    # 检查端口8000
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        log_warning "端口8000已被占用，请先停止相关服务"
        exit 1
    fi
    
    # 检查端口3000
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        log_warning "端口3000已被占用，请先停止相关服务"
        exit 1
    fi
    
    log_success "端口检查通过"
}

# 显示服务状态
show_status() {
    log_info "服务状态:"
    
    if [ -f "backend/backend.pid" ]; then
        BACKEND_PID=$(cat backend/backend.pid)
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            log_success "后端服务运行中 (PID: $BACKEND_PID)"
        else
            log_error "后端服务未运行"
        fi
    else
        log_error "后端服务未启动"
    fi
    
    if [ -f "frontend/frontend.pid" ]; then
        FRONTEND_PID=$(cat frontend/frontend.pid)
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            log_success "前端服务运行中 (PID: $FRONTEND_PID)"
        else
            log_error "前端服务未运行"
        fi
    else
        log_error "前端服务未启动"
    fi
}

# 停止服务
stop_services() {
    log_info "停止服务..."
    
    # 停止后端服务
    if [ -f "backend/backend.pid" ]; then
        BACKEND_PID=$(cat backend/backend.pid)
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            kill $BACKEND_PID
            rm backend/backend.pid
            log_success "后端服务已停止"
        fi
    fi
    
    # 停止前端服务
    if [ -f "frontend/frontend.pid" ]; then
        FRONTEND_PID=$(cat frontend/frontend.pid)
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            kill $FRONTEND_PID
            rm frontend/frontend.pid
            log_success "前端服务已停止"
        fi
    fi
}

# 主函数
main() {
    case "${1:-start}" in
        "start")
            log_info "开始启动 H-System EDR 平台服务..."
            check_dependencies
            check_ports
            install_python_deps
            install_node_deps
            start_backend
            start_frontend
            log_success "所有服务启动完成！"
            log_info "前端地址: http://localhost:3000"
            log_info "后端地址: http://localhost:8000"
            log_info "API文档: http://localhost:8000/docs"
            ;;
        "stop")
            stop_services
            ;;
        "restart")
            stop_services
            sleep 2
            main start
            ;;
        "status")
            show_status
            ;;
        "test")
            log_info "运行连通性测试..."
            if [ -f "backend/test_connectivity.py" ]; then
                cd backend
                python3 test_connectivity.py
                cd ..
            else
                log_error "未找到测试脚本 backend/test_connectivity.py"
            fi
            ;;
        *)
            echo "用法: $0 {start|stop|restart|status|test}"
            echo "  start   - 启动所有服务"
            echo "  stop    - 停止所有服务"
            echo "  restart - 重启所有服务"
            echo "  status  - 显示服务状态"
            echo "  test    - 运行连通性测试"
            exit 1
            ;;
    esac
}

# 捕获中断信号
trap 'log_info "收到中断信号，正在停止服务..."; stop_services; exit 0' INT TERM

# 运行主函数
main "$@"
