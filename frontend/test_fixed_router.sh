#!/bin/bash

# 测试修复后的路由配置

echo "🔧 测试修复后的路由配置"
echo "========================"

# 备份simple路由
if [ -f "src/router/index.ts.simple" ]; then
    echo "✅ simple路由备份已存在"
else
    echo "📝 备份当前simple路由配置..."
    cp src/router/index.ts src/router/index.ts.simple
fi

# 恢复原始路由（如果有备份）
if [ -f "src/router/index.ts.backup" ]; then
    echo "📝 恢复原始路由配置..."
    cp src/router/index.ts.backup src/router/index.ts
    echo "✅ 原始路由已恢复"
else
    echo "✅ 使用当前修复后的路由配置"
fi

# 检查环境配置
echo ""
echo "🔍 检查环境配置..."
if grep -q "VITE_ENABLE_AUTH=false" .env.development; then
    echo "✅ 认证已禁用 (开发模式)"
else
    echo "⚠️  认证状态未知，添加配置..."
    echo "VITE_ENABLE_AUTH=false" >> .env.development
fi

# 显示当前配置
echo ""
echo "📋 当前配置:"
echo "   认证状态: $(grep VITE_ENABLE_AUTH .env.development || echo '未设置')"
echo "   API地址: $(grep VITE_API_BASE_URL .env.development)"
echo "   代理状态: $(grep VITE_DEV_PROXY .env.development)"

echo ""
echo "🚀 现在可以重新启动前端服务:"
echo "   npm run dev"
echo ""
echo "💡 如果需要启用认证，修改 .env.development:"
echo "   VITE_ENABLE_AUTH=true"
