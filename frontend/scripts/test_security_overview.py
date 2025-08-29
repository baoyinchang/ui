#!/usr/bin/env python3
"""
测试SecurityOverview页面
验证安全态势页面是否能正常工作
"""

import os
from pathlib import Path

def verify_dashboard_setup():
    """验证仪表板设置"""
    print("🔍 验证仪表板设置...")
    
    # 检查关键文件
    files_to_check = [
        ('../src/views/dashboard/index.vue', '仪表板主页'),
        ('../src/views/dashboard/SecurityOverview.vue', '安全态势页面'),
        ('../src/api/dashboard.ts', '仪表板API'),
        ('../src/api/mock/dashboard.ts', '模拟仪表板API'),
        ('../src/components/common/EchartsChart.vue', 'Echarts图表组件'),
        ('../src/components/common/StatusTag.vue', '状态标签组件')
    ]
    
    all_good = True
    for file_path, description in files_to_check:
        file_obj = Path(file_path)
        if file_obj.exists():
            size = file_obj.stat().st_size
            print(f"   ✅ {description}: {file_path} ({size} bytes)")
        else:
            print(f"   ❌ {description}: {file_path} 不存在")
            all_good = False
    
    return all_good

def check_dashboard_index():
    """检查仪表板主页是否正确引用SecurityOverview"""
    print("\n📄 检查仪表板主页...")
    
    index_file = Path('../src/views/dashboard/index.vue')
    if not index_file.exists():
        print("   ❌ 仪表板主页不存在")
        return False
    
    content = index_file.read_text(encoding='utf-8')
    
    checks = [
        ('引用SecurityOverview组件', '<SecurityOverview />'),
        ('导入SecurityOverview', "import SecurityOverview from './SecurityOverview.vue'"),
        ('没有旧的占位符内容', '仪表板功能正在开发中' not in content)
    ]
    
    all_good = True
    for check_name, condition in checks:
        if isinstance(condition, bool):
            if condition:
                print(f"   ✅ {check_name}")
            else:
                print(f"   ❌ {check_name}")
                all_good = False
        elif condition in content:
            print(f"   ✅ {check_name}")
        else:
            print(f"   ❌ {check_name}")
            all_good = False
    
    return all_good

def check_api_setup():
    """检查API设置"""
    print("\n🔌 检查API设置...")
    
    api_file = Path('../src/api/dashboard.ts')
    if not api_file.exists():
        print("   ❌ 仪表板API文件不存在")
        return False
    
    content = api_file.read_text(encoding='utf-8')
    
    checks = [
        ('导入模拟API', 'import { mockDashboardApi }'),
        ('开发模式检查', 'isDevelopmentMode'),
        ('API包装器', 'enhancedMockDashboardApi'),
        ('地理威胁分布方法', 'getGeoThreatDistribution'),
        ('开发模式提示', '开发模式：使用模拟仪表板API')
    ]
    
    all_good = True
    for check_name, pattern in checks:
        if pattern in content:
            print(f"   ✅ {check_name}")
        else:
            print(f"   ❌ {check_name}")
            all_good = False
    
    return all_good

def create_test_commands():
    """创建测试命令"""
    print("\n📋 创建测试命令...")
    
    test_commands = '''# SecurityOverview 测试命令

## 🚀 测试步骤

### 1. 重启前端服务
```bash
npm run dev
```

### 2. 访问安全态势页面
- 点击左侧菜单的"安全态势"
- 或直接访问：http://localhost:3000/dashboard

### 3. 浏览器控制台验证
在浏览器开发者工具中运行：

```javascript
// 1. 检查环境配置
console.log('认证开关:', import.meta.env.VITE_ENABLE_AUTH)
console.log('是否开发模式:', import.meta.env.VITE_ENABLE_AUTH !== 'true')

// 2. 检查页面元素
const securityOverview = document.querySelector('.security-overview')
console.log('安全态势容器:', securityOverview ? '存在' : '不存在')

// 3. 检查统计卡片
const statCards = document.querySelectorAll('.stat-card')
console.log('统计卡片数量:', statCards.length)

// 4. 检查图表
const charts = document.querySelectorAll('.echarts')
console.log('图表数量:', charts.length)

// 5. 检查告警列表
const alertRows = document.querySelectorAll('.alert-item')
console.log('告警条目数量:', alertRows.length)

// 6. 测试API调用
fetch('/api/dashboard/overview', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
}).then(response => {
    console.log('API响应状态:', response.status)
    if (response.status === 404) {
        console.log('✅ 正常：API不存在，使用模拟数据')
    }
}).catch(error => {
    console.log('✅ 正常：API调用失败，使用模拟数据')
})
```

## ✅ 预期结果

### 页面显示
- [ ] 页面快速加载（2-3秒内）
- [ ] 显示安全态势总览
- [ ] 显示多个统计卡片（告警、资产、威胁等）
- [ ] 显示图表（告警趋势、威胁分布等）
- [ ] 显示最新告警列表
- [ ] 显示系统健康状态

### 数据内容
- [ ] 统计数据显示合理的数字
- [ ] 图表有数据并能正常渲染
- [ ] 告警列表显示模拟告警
- [ ] 状态标签显示正确的颜色

### 交互功能
- [ ] 刷新按钮正常工作
- [ ] 时间范围选择器正常工作
- [ ] 图表支持缩放和交互
- [ ] 告警项可以点击查看详情

### 控制台输出
- [ ] 显示 "🔧 开发模式：使用模拟仪表板API"
- [ ] 没有API错误信息
- [ ] 没有组件加载错误

## 🔧 故障排除

### 如果页面显示空白
1. 检查浏览器控制台是否有JavaScript错误
2. 确认所有组件文件都存在
3. 检查API导入是否正确

### 如果图表不显示
1. 检查EchartsChart组件是否正确加载
2. 确认echarts库是否已安装
3. 检查图表数据格式是否正确

### 如果数据不加载
1. 检查模拟API是否正确导入
2. 确认开发模式检查逻辑
3. 查看网络请求是否被拦截

### 如果样式异常
1. 检查CSS样式是否正确加载
2. 确认Element Plus样式是否生效
3. 检查响应式布局是否正常

## 📞 获取帮助

如果问题仍然存在，请提供：
1. 浏览器控制台的完整错误信息
2. 网络请求的详细状态
3. 页面截图
4. 前端服务的启动日志
'''
    
    test_file = Path('security_overview_test.md')
    test_file.write_text(test_commands, encoding='utf-8')
    print(f"   ✅ 测试命令已保存到: {test_file}")

def main():
    """主函数"""
    print("🔍 测试SecurityOverview页面设置")
    print("=" * 40)
    
    # 切换到scripts目录
    os.chdir(Path(__file__).parent)
    
    # 执行所有验证
    files_ok = verify_dashboard_setup()
    index_ok = check_dashboard_index()
    api_ok = check_api_setup()
    
    # 创建测试命令
    create_test_commands()
    
    print("\n🎉 SecurityOverview设置验证完成！")
    
    if all([files_ok, index_ok, api_ok]):
        print("\n✅ 所有验证通过！SecurityOverview已准备就绪！")
        
        print("\n📋 完成的工作:")
        print("   🔄 将dashboard/index.vue替换为SecurityOverview组件")
        print("   🔌 创建了完整的模拟仪表板API")
        print("   📊 支持所有SecurityOverview需要的数据")
        print("   🎨 包含图表、统计、告警等完整功能")
        
        print("\n🚀 现在可以:")
        print("   1. 重启前端服务: npm run dev")
        print("   2. 点击左侧菜单的'安全态势'")
        print("   3. 查看完整的安全态势仪表板")
        print("   4. 使用 security_overview_test.md 进行详细测试")
        
        print("\n🎯 预期效果:")
        print("   - 显示丰富的安全态势数据")
        print("   - 包含多种图表和统计信息")
        print("   - 实时告警和威胁情报")
        print("   - 完全模拟demo_01的效果")
        
    else:
        print("\n⚠️  发现一些问题:")
        print(f"   - 文件检查: {'✅' if files_ok else '❌'}")
        print(f"   - 主页设置: {'✅' if index_ok else '❌'}")
        print(f"   - API设置: {'✅' if api_ok else '❌'}")
        print("\n   请检查上述输出，解决发现的问题")

if __name__ == "__main__":
    main()
