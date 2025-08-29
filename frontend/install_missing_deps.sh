#!/bin/bash

# 安装缺失的Vite插件依赖

echo "🔧 安装缺失的Vite插件依赖..."

# 检查npm是否可用
if ! command -v npm >/dev/null 2>&1; then
    echo "❌ npm未找到"
    exit 1
fi

# 安装缺失的依赖
echo "📦 安装开发依赖..."

npm install --save-dev \
  vite-plugin-html \
  vite-plugin-svg-icons \
  rollup-plugin-visualizer \
  @vitejs/plugin-vue-jsx \
  vite-plugin-compression2

echo "✅ 依赖安装完成"

# 检查安装结果
echo ""
echo "🔍 验证安装结果..."

packages=(
  "vite-plugin-html"
  "vite-plugin-svg-icons" 
  "rollup-plugin-visualizer"
  "@vitejs/plugin-vue-jsx"
  "vite-plugin-compression2"
)

for package in "${packages[@]}"; do
    if npm list "$package" >/dev/null 2>&1; then
        echo "✅ $package"
    else
        echo "❌ $package 安装失败"
    fi
done

echo ""
echo "🚀 现在可以尝试启动开发服务器:"
echo "   npm run dev"
echo "   或者 ./start.sh"
