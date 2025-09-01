// 前后端连通性测试脚本
// 在 Ubuntu 系统中运行此脚本来测试前后端是否正常通信

const axios = require('axios');

// 测试配置
const config = {
  frontend: {
    baseURL: 'http://localhost:3000',
    apiEndpoint: '/api/v1'
  },
  backend: {
    baseURL: 'http://localhost:8000',
    healthEndpoint: '/health',
    apiEndpoint: '/api/v1'
  }
};

// 测试后端健康状态
async function testBackendHealth() {
  try {
    console.log('🔍 测试后端健康状态...');
    const response = await axios.get(`${config.backend.baseURL}${config.backend.healthEndpoint}`, {
      timeout: 5000
    });
    console.log('✅ 后端健康检查通过:', response.status, response.data);
    return true;
  } catch (error) {
    console.log('❌ 后端健康检查失败:', error.message);
    return false;
  }
}

// 测试后端API端点
async function testBackendAPI() {
  try {
    console.log('🔍 测试后端API端点...');
    const response = await axios.get(`${config.backend.baseURL}${config.backend.apiEndpoint}`, {
      timeout: 5000
    });
    console.log('✅ 后端API端点可访问:', response.status);
    return true;
  } catch (error) {
    console.log('❌ 后端API端点不可访问:', error.message);
    return false;
  }
}

// 测试前端代理到后端
async function testFrontendProxy() {
  try {
    console.log('🔍 测试前端代理到后端...');
    const response = await axios.get(`${config.frontend.baseURL}${config.frontend.apiEndpoint}`, {
      timeout: 5000
    });
    console.log('✅ 前端代理到后端成功:', response.status);
    return true;
  } catch (error) {
    console.log('❌ 前端代理到后端失败:', error.message);
    return false;
  }
}

// 测试数据库连接
async function testDatabaseConnection() {
  try {
    console.log('🔍 测试数据库连接...');
    const response = await axios.get(`${config.backend.baseURL}/api/v1/system/status`, {
      timeout: 5000
    });
    console.log('✅ 数据库连接正常:', response.status);
    return true;
  } catch (error) {
    console.log('❌ 数据库连接失败:', error.message);
    return false;
  }
}

// 主测试函数
async function runTests() {
  console.log('🚀 开始前后端连通性测试...\n');
  
  const results = {
    backendHealth: await testBackendHealth(),
    backendAPI: await testBackendAPI(),
    frontendProxy: await testFrontendProxy(),
    database: await testDatabaseConnection()
  };
  
  console.log('\n📊 测试结果汇总:');
  console.log('后端健康状态:', results.backendHealth ? '✅' : '❌');
  console.log('后端API端点:', results.backendAPI ? '✅' : '❌');
  console.log('前端代理:', results.frontendProxy ? '✅' : '❌');
  console.log('数据库连接:', results.database ? '✅' : '❌');
  
  const allPassed = Object.values(results).every(result => result);
  if (allPassed) {
    console.log('\n🎉 所有测试通过！前后端连通性正常。');
  } else {
    console.log('\n⚠️  部分测试失败，请检查相关服务状态。');
  }
}

// 运行测试
if (require.main === module) {
  runTests().catch(console.error);
}

module.exports = { runTests };
