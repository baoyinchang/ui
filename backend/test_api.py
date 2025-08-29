#!/usr/bin/env python3
"""
API测试脚本
用于测试后端API接口的基本功能
"""

import requests
import json
import sys
from typing import Optional

# API基础URL
BASE_URL = "http://localhost:8000/api/v1"

class APITester:
    """API测试类"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token: Optional[str] = None
    
    def test_health_check(self) -> bool:
        """测试健康检查"""
        try:
            response = self.session.get(f"{self.base_url.replace('/api/v1', '')}/")
            if response.status_code == 200:
                print("✅ 健康检查通过")
                print(f"   响应: {response.json()}")
                return True
            else:
                print(f"❌ 健康检查失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 健康检查异常: {e}")
            return False
    
    def test_login(self, username: str = "admin", password: str = "admin123456") -> bool:
        """测试用户登录"""
        try:
            login_data = {
                "username": username,
                "password": password
            }
            
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json=login_data
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                
                # 设置认证头
                self.session.headers.update({
                    "Authorization": f"Bearer {self.access_token}"
                })
                
                print("✅ 用户登录成功")
                print(f"   用户: {data.get('user', {}).get('username')}")
                print(f"   令牌: {self.access_token[:20]}...")
                return True
            else:
                print(f"❌ 用户登录失败: {response.status_code}")
                print(f"   错误: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 用户登录异常: {e}")
            return False
    
    def test_get_current_user(self) -> bool:
        """测试获取当前用户信息"""
        try:
            response = self.session.get(f"{self.base_url}/auth/me")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 获取用户信息成功")
                print(f"   用户名: {data.get('username')}")
                print(f"   全名: {data.get('full_name')}")
                print(f"   角色: {[role['name'] for role in data.get('roles', [])]}")
                print(f"   权限数量: {len(data.get('permissions', []))}")
                return True
            else:
                print(f"❌ 获取用户信息失败: {response.status_code}")
                print(f"   错误: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 获取用户信息异常: {e}")
            return False
    
    def test_get_security_metrics(self) -> bool:
        """测试获取安全态势指标"""
        try:
            response = self.session.get(f"{self.base_url}/dashboard/metrics")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 获取安全态势指标成功")
                print(f"   今日新增告警: {data.get('today_alerts')}")
                print(f"   未处理告警: {data.get('unhandled_alerts')}")
                print(f"   受影响资产: {data.get('affected_assets')}")
                print(f"   活跃狩猎任务: {data.get('active_hunting_tasks')}")
                return True
            else:
                print(f"❌ 获取安全态势指标失败: {response.status_code}")
                print(f"   错误: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 获取安全态势指标异常: {e}")
            return False
    
    def test_get_users_list(self) -> bool:
        """测试获取用户列表"""
        try:
            response = self.session.get(f"{self.base_url}/users/")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 获取用户列表成功")
                print(f"   用户总数: {data.get('total')}")
                print(f"   当前页用户数: {len(data.get('items', []))}")
                return True
            else:
                print(f"❌ 获取用户列表失败: {response.status_code}")
                print(f"   错误: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 获取用户列表异常: {e}")
            return False
    
    def test_create_user(self) -> bool:
        """测试创建用户"""
        try:
            user_data = {
                "username": "test_user",
                "password": "test123456",
                "full_name": "测试用户",
                "email": "test@hsystem.com",
                "is_active": True
            }
            
            response = self.session.post(
                f"{self.base_url}/users/",
                json=user_data
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 创建用户成功")
                print(f"   用户ID: {data.get('id')}")
                print(f"   用户名: {data.get('username')}")
                return True
            elif response.status_code == 400:
                print("⚠️  用户可能已存在")
                return True  # 认为测试通过
            else:
                print(f"❌ 创建用户失败: {response.status_code}")
                print(f"   错误: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 创建用户异常: {e}")
            return False
    
    def test_get_alerts(self) -> bool:
        """测试获取告警列表"""
        try:
            response = self.session.get(f"{self.base_url}/alerts/")

            if response.status_code == 200:
                data = response.json()
                print("✅ 获取告警列表成功")
                print(f"   告警总数: {data.get('total')}")
                print(f"   当前页告警数: {len(data.get('items', []))}")
                return True
            else:
                print(f"❌ 获取告警列表失败: {response.status_code}")
                print(f"   错误: {response.text}")
                return False

        except Exception as e:
            print(f"❌ 获取告警列表异常: {e}")
            return False

    def test_get_assets(self) -> bool:
        """测试获取资产列表"""
        try:
            response = self.session.get(f"{self.base_url}/assets/")

            if response.status_code == 200:
                data = response.json()
                print("✅ 获取资产列表成功")
                print(f"   资产总数: {data.get('total')}")
                print(f"   当前页资产数: {len(data.get('items', []))}")
                return True
            else:
                print(f"❌ 获取资产列表失败: {response.status_code}")
                print(f"   错误: {response.text}")
                return False

        except Exception as e:
            print(f"❌ 获取资产列表异常: {e}")
            return False

    def test_get_hunting_tasks(self) -> bool:
        """测试获取狩猎任务列表"""
        try:
            response = self.session.get(f"{self.base_url}/hunting/")

            if response.status_code == 200:
                data = response.json()
                print("✅ 获取狩猎任务列表成功")
                print(f"   任务总数: {data.get('total')}")
                print(f"   当前页任务数: {len(data.get('items', []))}")
                return True
            else:
                print(f"❌ 获取狩猎任务列表失败: {response.status_code}")
                print(f"   错误: {response.text}")
                return False

        except Exception as e:
            print(f"❌ 获取狩猎任务列表异常: {e}")
            return False

    def test_get_intelligence_iocs(self) -> bool:
        """测试获取威胁情报IOC列表"""
        try:
            response = self.session.get(f"{self.base_url}/intelligence/iocs")

            if response.status_code == 200:
                data = response.json()
                print("✅ 获取IOC列表成功")
                print(f"   IOC总数: {data.get('total')}")
                print(f"   当前页IOC数: {len(data.get('items', []))}")
                return True
            else:
                print(f"❌ 获取IOC列表失败: {response.status_code}")
                print(f"   错误: {response.text}")
                return False

        except Exception as e:
            print(f"❌ 获取IOC列表异常: {e}")
            return False

    def test_system_health(self) -> bool:
        """测试系统健康检查"""
        try:
            response = self.session.get(f"{self.base_url}/system/health")

            if response.status_code == 200:
                data = response.json()
                print("✅ 系统健康检查成功")
                print(f"   系统状态: {data.get('status')}")
                print(f"   数据库状态: {data.get('database')}")
                return True
            else:
                print(f"❌ 系统健康检查失败: {response.status_code}")
                print(f"   错误: {response.text}")
                return False

        except Exception as e:
            print(f"❌ 系统健康检查异常: {e}")
            return False

    def run_all_tests(self) -> bool:
        """运行所有测试"""
        print("🚀 开始API功能测试...\n")

        tests = [
            ("健康检查", self.test_health_check),
            ("用户登录", self.test_login),
            ("获取当前用户信息", self.test_get_current_user),
            ("获取安全态势指标", self.test_get_security_metrics),
            ("获取用户列表", self.test_get_users_list),
            ("创建用户", self.test_create_user),
            ("获取告警列表", self.test_get_alerts),
            ("获取资产列表", self.test_get_assets),
            ("获取狩猎任务列表", self.test_get_hunting_tasks),
            ("获取威胁情报IOC", self.test_get_intelligence_iocs),
            ("系统健康检查", self.test_system_health),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 测试: {test_name}")
            print("-" * 40)
            
            if test_func():
                passed += 1
            
            print()
        
        print("=" * 50)
        print(f"📊 测试结果: {passed}/{total} 通过")
        
        if passed == total:
            print("🎉 所有测试通过！")
            return True
        else:
            print("⚠️  部分测试失败，请检查服务状态")
            return False

def main():
    """主函数"""
    print("H-System 蜜罐EDR平台 - API测试工具")
    print("=" * 50)
    
    # 检查服务器是否运行
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code != 200:
            print("❌ 服务器未正常运行，请先启动后端服务")
            print("   运行命令: python start_server.py")
            sys.exit(1)
    except requests.exceptions.RequestException:
        print("❌ 无法连接到服务器，请确保后端服务已启动")
        print("   运行命令: python start_server.py")
        sys.exit(1)
    
    # 运行测试
    tester = APITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ API测试完成，后端服务运行正常！")
        sys.exit(0)
    else:
        print("\n❌ API测试失败，请检查服务配置")
        sys.exit(1)

if __name__ == "__main__":
    main()
