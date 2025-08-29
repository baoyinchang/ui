# SecurityOverview 测试命令

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
