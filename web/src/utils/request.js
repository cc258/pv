// src/utils/request.js
import axios from 'axios'

// 创建 axios 实例
const request = axios.create({
  baseURL: '/apis/v1',  // 后端 API 前缀
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 添加 token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器
request.interceptors.response.use(
  response => response.data,  // 直接返回 data
  error => {
    if (error.response?.status === 401) {
      // 未授权，清除 token 并跳转登录
      localStorage.removeItem('token')
    }
    return Promise.reject(error)
  }
)

export default request