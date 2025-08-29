@echo off
chcp 65001 >nul
title H-System EDR平台 - 前端开发环境

echo.
echo ========================================
echo   H-System EDR平台 - 前端开发环境
echo ========================================
echo.

echo [1/5] 检查Node.js环境...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到Node.js
    echo    请先安装Node.js 18.0.0或更高版本
    echo    下载地址: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

for /f "tokens=1" %%i in ('node --version') do set NODE_VERSION=%%i
echo ✅ Node.js版本: %NODE_VERSION%

echo.
echo [2/5] 检查npm版本...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到npm
    pause
    exit /b 1
)

for /f "tokens=1" %%i in ('npm --version') do set NPM_VERSION=%%i
echo ✅ npm版本: %NPM_VERSION%

echo.
echo [3/5] 检查项目依赖...
if not exist "node_modules" (
    echo 📦 首次运行，正在安装依赖包...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ 错误: 依赖安装失败
        echo    请检查网络连接或尝试使用淘宝镜像:
        echo    npm config set registry https://registry.npmmirror.com/
        echo.
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
) else (
    echo ✅ 依赖已存在，跳过安装
)

echo.
echo [4/5] 检查环境配置...
if not exist ".env" (
    if exist ".env.example" (
        echo 📝 复制环境配置文件...
        copy ".env.example" ".env" >nul
        echo ✅ 环境配置文件已创建
    ) else (
        echo 📝 创建默认环境配置...
        echo # H-System EDR平台 - 开发环境配置 > .env
        echo VITE_API_BASE_URL=http://localhost:8000 >> .env
        echo VITE_APP_TITLE=H-System EDR平台 >> .env
        echo VITE_APP_VERSION=1.0.0 >> .env
        echo ✅ 默认环境配置已创建
    )
) else (
    echo ✅ 环境配置文件已存在
)

echo.
echo [5/5] 启动开发服务器...
echo 🚀 正在启动前端开发服务器...
echo    访问地址: http://localhost:3000
echo    API地址: http://localhost:8000
echo.
echo 按 Ctrl+C 停止服务器
echo.

npm run dev

if %errorlevel% neq 0 (
    echo.
    echo ❌ 开发服务器启动失败
    echo    请检查端口3000是否被占用
    echo    或查看上方错误信息
    echo.
    pause
    exit /b 1
)

pause
