#!/bin/bash

# 前端启动调试脚本
# 用于诊断start.sh脚本的问题

set -x  # 启用调试模式，显示每个命令的执行

echo "🔍 前端启动调试脚本"
echo "===================="

# 检查当前目录
echo "当前目录: $(pwd)"
echo "目录内容:"
ls -la

# 检查Node.js环境
echo ""
echo "Node.js环境检查:"
echo "Node.js路径: $(which node)"
echo "Node.js版本: $(node --version)"
echo "npm路径: $(which npm)"
echo "npm版本: $(npm --version)"

# 检查package.json
echo ""
echo "package.json检查:"
if [ -f "package.json" ]; then
    echo "✅ package.json存在"
    echo "项目名称: $(cat package.json | grep '"name"' | head -1)"
    echo "项目版本: $(cat package.json | grep '"version"' | head -1)"
else
    echo "❌ package.json不存在"
fi

# 检查node_modules
echo ""
echo "依赖检查:"
if [ -d "node_modules" ]; then
    echo "✅ node_modules存在"
    echo "node_modules大小: $(du -sh node_modules 2>/dev/null || echo '无法计算')"
else
    echo "❌ node_modules不存在，需要运行 npm install"
fi

# 检查关键文件
echo ""
echo "关键文件检查:"
files=("vite.config.ts" "tsconfig.json" "index.html" "src/main.ts")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file 缺失"
    fi
done

# 测试版本比较函数
echo ""
echo "版本比较函数测试:"

version_compare() {
    local version1=$1
    local version2=$2
    
    # 移除v前缀
    version1=${version1#v}
    version2=${version2#v}
    
    if [[ "$version1" == "$version2" ]]; then
        return 0
    fi
    
    local IFS=.
    local i ver1=($version1) ver2=($version2)
    
    # 填充较短的版本号
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++)); do
        ver1[i]=0
    done
    for ((i=${#ver2[@]}; i<${#ver1[@]}; i++)); do
        ver2[i]=0
    done
    
    # 比较每个部分
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

NODE_VERSION=$(node --version)
echo "测试版本比较: $NODE_VERSION vs 18.0.0"
version_compare "$NODE_VERSION" "18.0.0"
result=$?
echo "比较结果: $result"
case $result in
    0) echo "版本相等" ;;
    1) echo "当前版本更高 ✅" ;;
    2) echo "当前版本更低 ❌" ;;
esac

# 尝试直接运行npm命令
echo ""
echo "直接测试npm命令:"
echo "npm --version:"
npm --version

echo ""
echo "npm run dev --help:"
npm run dev --help 2>&1 | head -10

echo ""
echo "🎯 调试完成！"
echo ""
echo "如果以上检查都正常，可以尝试:"
echo "1. 直接运行: npm run dev"
echo "2. 或使用简化脚本: ./simple_start.sh"
