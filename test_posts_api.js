const axios = require('axios');

// 创建axios实例
const http = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 60000
});

// 测试获取经验贴列表
async function testGetPosts() {
  try {
    console.log('测试获取经验贴列表...');
    const response = await http.get('/posts/', {
      params: {
        category: '',
        skip: 0,
        limit: 20
      }
    });
    console.log('成功获取经验贴列表:', response.data);
  } catch (error) {
    console.error('获取经验贴列表失败:', error.response ? error.response.data : error.message);
  }
}

// 测试根路径
async function testRoot() {
  try {
    console.log('测试根路径...');
    const response = await axios.get('http://localhost:8000/');
    console.log('根路径响应:', response.data);
  } catch (error) {
    console.error('根路径测试失败:', error.message);
  }
}

// 运行测试
async function runTests() {
  await testRoot();
  await testGetPosts();
}

runTests();