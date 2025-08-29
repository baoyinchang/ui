@echo off
chcp 65001 >nul
title H-System EDR平台 - 项目初始化

echo.
echo ========================================
echo   H-System EDR平台 - 项目初始化
echo ========================================
echo.
echo 此脚本将帮助您完成项目的初始化设置
echo.

echo [1/6] 检查系统环境...

:: 检查Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Node.js
    echo.
    echo 请先安装Node.js 18.0.0或更高版本:
    echo 1. 访问 https://nodejs.org/
    echo 2. 下载LTS版本
    echo 3. 安装后重新运行此脚本
    echo.
    pause
    exit /b 1
)

for /f "tokens=1" %%i in ('node --version') do set NODE_VERSION=%%i
echo ✅ Node.js: %NODE_VERSION%

:: 检查Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  未找到Git（可选）
    echo    建议安装Git用于版本控制: https://git-scm.com/
) else (
    for /f "tokens=3" %%i in ('git --version') do set GIT_VERSION=%%i
    echo ✅ Git: %GIT_VERSION%
)

echo.
echo [2/6] 安装项目依赖...
if exist "node_modules" (
    echo 📦 依赖已存在，正在更新...
    npm update
) else (
    echo 📦 首次安装依赖包...
    npm install
)

if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    echo.
    echo 可能的解决方案:
    echo 1. 检查网络连接
    echo 2. 使用淘宝镜像: npm config set registry https://registry.npmmirror.com/
    echo 3. 清除npm缓存: npm cache clean --force
    echo.
    pause
    exit /b 1
)

echo ✅ 依赖安装完成

echo.
echo [3/6] 配置环境文件...
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo ✅ 从模板创建环境配置文件
    ) else (
        echo # H-System EDR平台 - 开发环境配置 > .env
        echo # API服务器地址 >> .env
        echo VITE_API_BASE_URL=http://localhost:8000 >> .env
        echo. >> .env
        echo # 应用信息 >> .env
        echo VITE_APP_TITLE=H-System EDR平台 >> .env
        echo VITE_APP_VERSION=1.0.0 >> .env
        echo VITE_APP_DESCRIPTION=蜜罐安全管理系统 >> .env
        echo. >> .env
        echo # 开发模式配置 >> .env
        echo VITE_DEV_MOCK=false >> .env
        echo VITE_DEV_PROXY=true >> .env
        echo. >> .env
        echo # 构建配置 >> .env
        echo VITE_BUILD_SOURCEMAP=false >> .env
        echo VITE_BUILD_DROP_CONSOLE=true >> .env
        echo ✅ 创建默认环境配置文件
    )
) else (
    echo ✅ 环境配置文件已存在
)

echo.
echo [4/6] 设置Git钩子（如果可用）...
if exist ".git" (
    if not exist ".husky" (
        echo 📝 初始化Git钩子...
        npx husky-init >nul 2>&1
        if %errorlevel% equ 0 (
            echo ✅ Git钩子设置完成
        ) else (
            echo ⚠️  Git钩子设置跳过
        )
    ) else (
        echo ✅ Git钩子已存在
    )
) else (
    echo ⚠️  不是Git仓库，跳过Git钩子设置
)

echo.
echo [5/6] 验证项目配置...
echo 🔍 运行类型检查...
npm run type-check >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 类型检查通过
) else (
    echo ⚠️  类型检查有警告，请查看详细信息
)

echo 🔍 运行代码检查...
npm run lint -- --max-warnings 0 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 代码检查通过
) else (
    echo ⚠️  代码检查有警告，请查看详细信息
)

echo.
echo [6/6] 项目初始化完成！
echo.
echo ========================================
echo ✅ 初始化成功！
echo ========================================
echo.
echo 📋 下一步操作:
echo.
echo 1. 开发环境:
echo    运行 'start.bat' 启动开发服务器
echo.
echo 2. 生产构建:
echo    运行 'build.bat' 构建生产版本
echo.
echo 3. 运行测试:
echo    运行 'test.bat all' 执行完整测试
echo.
echo 4. 配置说明:
echo    编辑 '.env' 文件修改配置
echo    编辑 'vite.config.ts' 修改构建配置
echo.
echo 📚 文档和帮助:
echo    - README.md: 项目说明
echo    - QUICK_START.md: 快速开始指南
echo    - docs/: 详细文档
echo.

pause
