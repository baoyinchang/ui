#!/usr/bin/env python3
"""
前后端连通性测试脚本
在 Ubuntu 系统中运行此脚本来测试前后端是否正常通信
"""

import asyncio
import aiohttp
import time
from typing import Dict, Any
import json

# 测试配置
CONFIG = {
    "frontend": {
        "base_url": "http://localhost:3000",
        "api_endpoint": "/api/v1"
    },
    "backend": {
        "base_url": "http://localhost:8000",
        "health_endpoint": "/health",
        "api_endpoint": "/api/v1"
    }
}

async def test_backend_health(session: aiohttp.ClientSession) -> bool:
    """测试后端健康状态"""
    try:
        print("🔍 测试后端健康状态...")
        async with session.get(f"{CONFIG['backend']['base_url']}{CONFIG['backend']['health_endpoint']}", 
                              timeout=aiohttp.ClientTimeout(total=5)) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ 后端健康检查通过: {response.status} {data}")
                return True
            else:
                print(f"❌ 后端健康检查失败: HTTP {response.status}")
                return False
    except Exception as e:
        print(f"❌ 后端健康检查失败: {str(e)}")
        return False

async def test_backend_api(session: aiohttp.ClientSession) -> bool:
    """测试后端API端点"""
    try:
        print("🔍 测试后端API端点...")
        async with session.get(f"{CONFIG['backend']['base_url']}{CONFIG['backend']['api_endpoint']}", 
                              timeout=aiohttp.ClientTimeout(total=5)) as response:
            if response.status in [200, 401, 403]:  # 这些状态码表示API端点可访问
                print(f"✅ 后端API端点可访问: HTTP {response.status}")
                return True
            else:
                print(f"❌ 后端API端点不可访问: HTTP {response.status}")
                return False
    except Exception as e:
        print(f"❌ 后端API端点不可访问: {str(e)}")
        return False

async def test_frontend_proxy(session: aiohttp.ClientSession) -> bool:
    """测试前端代理到后端"""
    try:
        print("🔍 测试前端代理到后端...")
        async with session.get(f"{CONFIG['frontend']['base_url']}{CONFIG['frontend']['api_endpoint']}", 
                              timeout=aiohttp.ClientTimeout(total=5)) as response:
            if response.status in [200, 401, 403]:  # 这些状态码表示代理成功
                print(f"✅ 前端代理到后端成功: HTTP {response.status}")
                return True
            else:
                print(f"❌ 前端代理到后端失败: HTTP {response.status}")
                return False
    except Exception as e:
        print(f"❌ 前端代理到后端失败: {str(e)}")
        return False

async def test_database_connection(session: aiohttp.ClientSession) -> bool:
    """测试数据库连接"""
    try:
        print("🔍 测试数据库连接...")
        async with session.get(f"{CONFIG['backend']['base_url']}/api/v1/system/status", 
                              timeout=aiohttp.ClientTimeout(total=5)) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ 数据库连接正常: HTTP {response.status}")
                return True
            else:
                print(f"❌ 数据库连接失败: HTTP {response.status}")
                return False
    except Exception as e:
        print(f"❌ 数据库连接失败: {str(e)}")
        return False

async def test_backend_startup() -> bool:
    """测试后端启动状态"""
    try:
        print("🔍 测试后端启动状态...")
        # 尝试连接后端，如果连接成功说明后端已启动
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{CONFIG['backend']['base_url']}/docs", 
                                  timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status in [200, 404]:  # 404表示API文档不存在但服务在运行
                    print("✅ 后端服务已启动")
                    return True
                else:
                    print(f"❌ 后端服务未正常启动: HTTP {response.status}")
                    return False
    except Exception as e:
        print(f"❌ 后端服务未启动: {str(e)}")
        return False

async def run_tests() -> None:
    """运行所有测试"""
    print("🚀 开始前后端连通性测试...\n")
    
    # 创建HTTP会话
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # 运行测试
        results = {
            "backend_startup": await test_backend_startup(),
            "backend_health": await test_backend_health(session),
            "backend_api": await test_backend_api(session),
            "frontend_proxy": await test_frontend_proxy(session),
            "database": await test_database_connection(session)
        }
    
    # 输出测试结果
    print("\n📊 测试结果汇总:")
    print(f"后端启动状态: {'✅' if results['backend_startup'] else '❌'}")
    print(f"后端健康状态: {'✅' if results['backend_health'] else '❌'}")
    print(f"后端API端点: {'✅' if results['backend_api'] else '❌'}")
    print(f"前端代理: {'✅' if results['frontend_proxy'] else '❌'}")
    print(f"数据库连接: {'✅' if results['database'] else '❌'}")
    
    # 计算成功率
    passed = sum(results.values())
    total = len(results)
    success_rate = (passed / total) * 100
    
    print(f"\n📈 测试成功率: {passed}/{total} ({success_rate:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有测试通过！前后端连通性正常。")
    elif passed >= total * 0.6:
        print("\n⚠️  大部分测试通过，但存在一些问题需要修复。")
    else:
        print("\n❌ 多个测试失败，请检查服务配置和网络连接。")
    
    # 提供诊断建议
    print("\n🔧 诊断建议:")
    if not results['backend_startup']:
        print("- 检查后端服务是否已启动")
        print("- 检查端口8000是否被占用")
        print("- 查看后端日志文件")
    
    if not results['backend_health']:
        print("- 检查后端配置文件")
        print("- 检查环境变量设置")
        print("- 检查数据库连接配置")
    
    if not results['frontend_proxy']:
        print("- 检查前端服务是否已启动")
        print("- 检查Vite代理配置")
        print("- 检查端口3000是否被占用")

def main():
    """主函数"""
    try:
        asyncio.run(run_tests())
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {str(e)}")

if __name__ == "__main__":
    main()
