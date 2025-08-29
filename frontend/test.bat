@echo off
chcp 65001 >nul
title H-System EDR平台 - 测试套件

echo.
echo ========================================
echo   H-System EDR平台 - 测试套件
echo ========================================
echo.

if "%1"=="" (
    echo 使用方法:
    echo   test.bat [命令]
    echo.
    echo 可用命令:
    echo   unit      - 运行单元测试
    echo   e2e       - 运行端到端测试
    echo   coverage  - 运行测试覆盖率
    echo   lint      - 代码检查
    echo   type      - 类型检查
    echo   all       - 运行所有测试
    echo   watch     - 监视模式运行测试
    echo.
    pause
    exit /b 0
)

echo [1/2] 检查测试环境...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到Node.js
    pause
    exit /b 1
)

if not exist "node_modules" (
    echo 📦 安装依赖包...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ 错误: 依赖安装失败
        pause
        exit /b 1
    )
)

echo ✅ 测试环境检查完成
echo.

echo [2/2] 执行测试命令...

if "%1"=="unit" (
    echo 🧪 运行单元测试...
    npm run test:unit
) else if "%1"=="e2e" (
    echo 🔄 运行端到端测试...
    npm run test:e2e
) else if "%1"=="coverage" (
    echo 📊 运行测试覆盖率...
    npm run test:coverage
) else if "%1"=="lint" (
    echo 🔍 代码检查...
    npm run lint
) else if "%1"=="type" (
    echo 📝 类型检查...
    npm run type-check
) else if "%1"=="watch" (
    echo 👀 监视模式运行测试...
    npm run test:watch
) else if "%1"=="all" (
    echo 🚀 运行所有测试...
    echo.
    echo [1/5] 类型检查...
    npm run type-check
    if %errorlevel% neq 0 (
        echo ❌ 类型检查失败
        pause
        exit /b 1
    )
    echo ✅ 类型检查通过
    echo.
    
    echo [2/5] 代码检查...
    npm run lint
    if %errorlevel% neq 0 (
        echo ❌ 代码检查失败
        pause
        exit /b 1
    )
    echo ✅ 代码检查通过
    echo.
    
    echo [3/5] 单元测试...
    npm run test:unit
    if %errorlevel% neq 0 (
        echo ❌ 单元测试失败
        pause
        exit /b 1
    )
    echo ✅ 单元测试通过
    echo.
    
    echo [4/5] 测试覆盖率...
    npm run test:coverage
    if %errorlevel% neq 0 (
        echo ❌ 测试覆盖率检查失败
        pause
        exit /b 1
    )
    echo ✅ 测试覆盖率检查通过
    echo.
    
    echo [5/5] 构建测试...
    npm run build
    if %errorlevel% neq 0 (
        echo ❌ 构建测试失败
        pause
        exit /b 1
    )
    echo ✅ 构建测试通过
    echo.
    
    echo ========================================
    echo ✅ 所有测试通过！
    echo ========================================
) else (
    echo ❌ 未知命令: %1
    echo 运行 'test.bat' 查看可用命令
    pause
    exit /b 1
)

if %errorlevel% neq 0 (
    echo.
    echo ❌ 测试失败
    pause
    exit /b 1
) else (
    echo.
    echo ✅ 测试完成
)

pause
