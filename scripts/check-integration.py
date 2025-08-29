#!/usr/bin/env python3
"""
前后端集成检查脚本
检查前后端通信、API接口、数据格式等关键问题
"""

import json
import requests
import asyncio
import aiohttp
from typing import Dict, List, Any
import sys
import os

class IntegrationChecker:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        self.issues = []
        
    def log_issue(self, level: str, component: str, message: str):
        """记录问题"""
        self.issues.append({
            "level": level,
            "component": component,
            "message": message
        })
        
    def check_backend_health(self) -> bool:
        """检查后端健康状态"""
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ 后端服务正常运行")
                return True
            else:
                self.log_issue("ERROR", "Backend", f"健康检查失败: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_issue("ERROR", "Backend", f"无法连接后端服务: {e}")
            return False
    
    def check_api_endpoints(self) -> Dict[str, bool]:
        """检查API端点"""
        endpoints = {
            "/api/v1/auth/login": "POST",
            "/api/v1/auth/register": "POST", 
            "/api/v1/auth/refresh": "POST",
            "/api/v1/users/me": "GET",
            "/api/v1/alerts": "GET",
            "/api/v1/assets": "GET"
        }
        
        results = {}
        
        for endpoint, method in endpoints.items():
            try:
                url = f"{self.backend_url}{endpoint}"
                
                if method == "GET":
                    # GET请求需要认证，这里只检查端点是否存在
                    response = requests.get(url, timeout=5)
                    # 401是预期的，说明端点存在但需要认证
                    if response.status_code in [200, 401, 422]:
                        results[endpoint] = True
                        print(f"✅ {endpoint} 端点可访问")
                    else:
                        results[endpoint] = False
                        self.log_issue("WARNING", "API", f"{endpoint} 返回异常状态码: {response.status_code}")
                        
                elif method == "POST":
                    # POST请求发送空数据，检查是否返回422（验证错误）
                    response = requests.post(url, json={}, timeout=5)
                    if response.status_code in [422, 400]:
                        results[endpoint] = True
                        print(f"✅ {endpoint} 端点可访问")
                    else:
                        results[endpoint] = False
                        self.log_issue("WARNING", "API", f"{endpoint} 返回异常状态码: {response.status_code}")
                        
            except requests.exceptions.RequestException as e:
                results[endpoint] = False
                self.log_issue("ERROR", "API", f"{endpoint} 无法访问: {e}")
                
        return results
    
    def check_cors_configuration(self) -> bool:
        """检查CORS配置"""
        try:
            headers = {
                'Origin': self.frontend_url,
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type,Authorization'
            }
            
            response = requests.options(
                f"{self.backend_url}/api/v1/auth/login",
                headers=headers,
                timeout=5
            )
            
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }
            
            if cors_headers['Access-Control-Allow-Origin']:
                print("✅ CORS配置正常")
                return True
            else:
                self.log_issue("ERROR", "CORS", "CORS头部缺失")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_issue("ERROR", "CORS", f"CORS检查失败: {e}")
            return False
    
    def test_login_flow(self) -> bool:
        """测试登录流程"""
        try:
            # 测试登录请求格式
            login_data = {
                "username": "test_user",
                "password": "test_password"
            }
            
            response = requests.post(
                f"{self.backend_url}/api/v1/auth/login",
                json=login_data,
                timeout=5
            )
            
            # 检查响应格式
            if response.status_code == 422:
                # 验证错误是预期的，检查错误格式
                error_data = response.json()
                if 'detail' in error_data:
                    print("✅ 登录端点响应格式正确")
                    return True
                else:
                    self.log_issue("WARNING", "Auth", "登录错误响应格式异常")
                    return False
            elif response.status_code == 401:
                # 认证失败也是预期的
                print("✅ 登录端点正常处理认证失败")
                return True
            else:
                self.log_issue("WARNING", "Auth", f"登录端点返回异常状态码: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_issue("ERROR", "Auth", f"登录流程测试失败: {e}")
            return False
    
    def check_response_format(self) -> bool:
        """检查响应格式一致性"""
        try:
            # 测试一个简单的GET请求
            response = requests.get(f"{self.backend_url}/api/v1/alerts", timeout=5)
            
            if response.status_code == 401:
                # 检查401错误的响应格式
                error_data = response.json()
                expected_fields = ['detail']  # FastAPI默认错误格式
                
                if all(field in error_data for field in expected_fields):
                    print("✅ 错误响应格式符合FastAPI标准")
                    return True
                else:
                    self.log_issue("WARNING", "Response", "错误响应格式不标准")
                    return False
            else:
                self.log_issue("INFO", "Response", f"意外的响应状态码: {response.status_code}")
                return True
                
        except requests.exceptions.RequestException as e:
            self.log_issue("ERROR", "Response", f"响应格式检查失败: {e}")
            return False
    
    def check_database_connection(self) -> bool:
        """检查数据库连接"""
        try:
            # 通过健康检查端点间接检查数据库
            response = requests.get(f"{self.backend_url}/health/db", timeout=5)
            
            if response.status_code == 200:
                print("✅ 数据库连接正常")
                return True
            elif response.status_code == 404:
                # 如果没有数据库健康检查端点，跳过
                print("⚠️  数据库健康检查端点不存在，跳过检查")
                return True
            else:
                self.log_issue("ERROR", "Database", "数据库连接异常")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_issue("WARNING", "Database", f"数据库检查失败: {e}")
            return True  # 不阻塞其他检查
    
    def generate_report(self):
        """生成检查报告"""
        print("\n" + "="*60)
        print("🔍 前后端集成检查报告")
        print("="*60)
        
        if not self.issues:
            print("✅ 所有检查项目都通过了！")
            return
        
        # 按级别分组问题
        errors = [issue for issue in self.issues if issue['level'] == 'ERROR']
        warnings = [issue for issue in self.issues if issue['level'] == 'WARNING']
        infos = [issue for issue in self.issues if issue['level'] == 'INFO']
        
        if errors:
            print(f"\n❌ 严重问题 ({len(errors)}个):")
            for issue in errors:
                print(f"   [{issue['component']}] {issue['message']}")
        
        if warnings:
            print(f"\n⚠️  警告 ({len(warnings)}个):")
            for issue in warnings:
                print(f"   [{issue['component']}] {issue['message']}")
        
        if infos:
            print(f"\n💡 信息 ({len(infos)}个):")
            for issue in infos:
                print(f"   [{issue['component']}] {issue['message']}")
        
        print(f"\n总计: {len(errors)}个错误, {len(warnings)}个警告, {len(infos)}个信息")
        
        # 提供修复建议
        if errors or warnings:
            print("\n🔧 修复建议:")
            print("1. 确保后端服务正在运行 (python -m uvicorn app.main:app --reload)")
            print("2. 检查数据库连接配置")
            print("3. 验证CORS设置")
            print("4. 确认API路径配置")
            print("5. 检查响应格式一致性")
    
    def run_all_checks(self):
        """运行所有检查"""
        print("🚀 开始前后端集成检查...\n")
        
        # 基础检查
        backend_ok = self.check_backend_health()
        if not backend_ok:
            print("❌ 后端服务不可用，跳过其他检查")
            self.generate_report()
            return False
        
        # API端点检查
        print("\n📡 检查API端点...")
        self.check_api_endpoints()
        
        # CORS检查
        print("\n🌐 检查CORS配置...")
        self.check_cors_configuration()
        
        # 认证流程检查
        print("\n🔐 检查认证流程...")
        self.test_login_flow()
        
        # 响应格式检查
        print("\n📋 检查响应格式...")
        self.check_response_format()
        
        # 数据库检查
        print("\n🗄️  检查数据库连接...")
        self.check_database_connection()
        
        # 生成报告
        self.generate_report()
        
        return len([issue for issue in self.issues if issue['level'] == 'ERROR']) == 0

def main():
    """主函数"""
    checker = IntegrationChecker()
    success = checker.run_all_checks()
    
    if success:
        print("\n🎉 集成检查完成，系统可以正常运行！")
        sys.exit(0)
    else:
        print("\n💥 发现严重问题，请修复后重试！")
        sys.exit(1)

if __name__ == "__main__":
    main()
