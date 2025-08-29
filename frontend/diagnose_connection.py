#!/usr/bin/env python3
"""
诊断前后端连接问题
"""

import requests
import socket
import time
from pathlib import Path

def check_port_open(host, port):
    """检查端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def check_http_response(url):
    """检查HTTP响应"""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code, response.text[:200]
    except requests.exceptions.ConnectionError:
        return None, "连接被拒绝"
    except requests.exceptions.Timeout:
        return None, "请求超时"
    except Exception as e:
        return None, f"错误: {str(e)}"

def check_frontend_config():
    """检查前端配置"""
    print("🔍 检查前端配置...")
    
    # 检查环境文件
    env_files = ['.env', '.env.development', '.env.local']
    for env_file in env_files:
        env_path = Path(env_file)
        if env_path.exists():
            print(f"   ✅ 找到环境文件: {env_file}")
            content = env_path.read_text(encoding='utf-8')
            if 'VITE_API_BASE_URL' in content:
                for line in content.split('\n'):
                    if 'VITE_API_BASE_URL' in line and not line.strip().startswith('#'):
                        print(f"      API地址: {line.strip()}")
        else:
            print(f"   ❌ 未找到: {env_file}")

def main():
    """主函数"""
    print("🔍 H-System EDR 连接诊断")
    print("=" * 40)
    
    # 检查前端端口
    print("\n📡 检查前端服务 (端口3000)...")
    if check_port_open('localhost', 3000):
        print("   ✅ 端口3000已开放")
        
        status, content = check_http_response('http://localhost:3000')
        if status:
            print(f"   ✅ HTTP响应: {status}")
            if 'DOCTYPE html' in content or '<html' in content:
                print("   ✅ 返回HTML页面")
            else:
                print(f"   ⚠️  响应内容: {content}")
        else:
            print(f"   ❌ HTTP请求失败: {content}")
    else:
        print("   ❌ 端口3000未开放")
        print("   💡 请检查前端服务是否启动: npm run dev")
    
    # 检查后端端口
    print("\n📡 检查后端服务 (端口8000)...")
    if check_port_open('localhost', 8000):
        print("   ✅ 端口8000已开放")
        
        status, content = check_http_response('http://localhost:8000')
        if status:
            print(f"   ✅ HTTP响应: {status}")
            print(f"   📄 响应内容: {content}")
        else:
            print(f"   ❌ HTTP请求失败: {content}")
    else:
        print("   ❌ 端口8000未开放")
        print("   💡 请检查后端服务是否启动")
    
    # 检查API连接
    print("\n📡 检查API连接...")
    api_endpoints = [
        'http://localhost:8000/',
        'http://localhost:8000/api/v1/',
        'http://localhost:8000/docs',
    ]
    
    for endpoint in api_endpoints:
        status, content = check_http_response(endpoint)
        if status:
            print(f"   ✅ {endpoint}: {status}")
        else:
            print(f"   ❌ {endpoint}: {content}")
    
    # 检查前端配置
    print("\n⚙️ 检查前端配置...")
    check_frontend_config()
    
    # 检查跨域问题
    print("\n🌐 检查跨域配置...")
    if check_port_open('localhost', 3000) and check_port_open('localhost', 8000):
        print("   ✅ 前后端服务都在运行")
        print("   💡 如果页面仍然加载不出来，可能是以下问题:")
        print("      1. 浏览器缓存问题 - 尝试硬刷新 (Ctrl+F5)")
        print("      2. 代理配置问题 - 检查vite.config.ts中的proxy设置")
        print("      3. 防火墙阻止 - 检查Windows防火墙设置")
        print("      4. 路由问题 - 检查Vue Router配置")
    
    # 提供解决建议
    print("\n💡 解决建议:")
    print("   1. 在浏览器中分别访问:")
    print("      - http://localhost:3000 (前端)")
    print("      - http://localhost:8000 (后端)")
    print("   2. 打开浏览器开发者工具 (F12):")
    print("      - 查看Console标签页的错误信息")
    print("      - 查看Network标签页的网络请求")
    print("   3. 检查服务启动日志:")
    print("      - 前端: 查看npm run dev的输出")
    print("      - 后端: 查看Python服务的输出")

if __name__ == "__main__":
    main()
