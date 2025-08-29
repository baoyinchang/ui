@echo off
chcp 65001 >nul
title H-System EDR平台 - 生产构建

echo.
echo ========================================
echo   H-System EDR平台 - 生产构建
echo ========================================
echo.

echo [1/4] 检查构建环境...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到Node.js
    pause
    exit /b 1
)

for /f "tokens=1" %%i in ('node --version') do set NODE_VERSION=%%i
echo ✅ Node.js版本: %NODE_VERSION%

echo.
echo [2/4] 检查项目依赖...
if not exist "node_modules" (
    echo 📦 安装依赖包...
    npm ci
    if %errorlevel% neq 0 (
        echo ❌ 错误: 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo ✅ 依赖已存在
)

echo.
echo [3/4] 清理旧构建文件...
if exist "dist" (
    rmdir /s /q "dist"
    echo ✅ 已清理旧构建文件
) else (
    echo ✅ 无需清理
)

echo.
echo [4/4] 开始构建生产版本...
echo 🔨 正在构建，请稍候...

npm run build
if %errorlevel% neq 0 (
    echo.
    echo ❌ 构建失败
    echo    请检查代码错误或依赖问题
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ 构建完成！
echo ========================================
echo.
echo 📁 构建文件位置: dist/
echo 📊 构建统计信息:

if exist "dist" (
    for /f %%i in ('dir /s /b "dist\*.*" ^| find /c /v ""') do set FILE_COUNT=%%i
    echo    文件数量: %FILE_COUNT%
    
    for /f "tokens=3" %%i in ('dir "dist" /s /-c ^| find "个文件"') do set TOTAL_SIZE=%%i
    echo    总大小: %TOTAL_SIZE% 字节
)

echo.
echo 🚀 部署建议:
echo    1. 将dist目录内容上传到Web服务器
echo    2. 配置Nginx或Apache服务器
echo    3. 确保API服务器正常运行
echo    4. 配置HTTPS证书（生产环境）
echo.

echo 📋 预览构建结果:
echo    运行 'npm run preview' 可本地预览构建结果
echo.

pause
