/**
 * 威胁情报API接口
 */

import request from '@/utils/request'

// 威胁情报API接口
export const intelligenceApi = {
  // 获取情报统计数据
  getIntelligenceStats() {
    return request({
      url: '/api/intelligence/stats',
      method: 'get'
    })
  },

  // 获取最近更新的IOC
  getRecentIocs(limit: number = 8) {
    return request({
      url: '/api/intelligence/recent',
      method: 'get',
      params: { limit }
    })
  },

  // 获取情报列表
  getIntelligenceList(params: any) {
    return request({
      url: '/api/intelligence/list',
      method: 'get',
      params
    })
  },

  // 添加威胁情报
  addIntelligence(data: any) {
    return request({
      url: '/api/intelligence/add',
      method: 'post',
      data
    })
  },

  // 更新威胁情报
  updateIntelligence(id: string, data: any) {
    return request({
      url: `/api/intelligence/${id}`,
      method: 'put',
      data
    })
  },

  // 删除威胁情报
  deleteIntelligence(id: string) {
    return request({
      url: `/api/intelligence/${id}`,
      method: 'delete'
    })
  },

  // 获取IOC详情
  getIocDetail(id: string) {
    return request({
      url: `/api/intelligence/${id}`,
      method: 'get'
    })
  },

  // 批量导入IOC
  importIocs(file: File) {
    const formData = new FormData()
    formData.append('file', file)
    
    return request({
      url: '/api/intelligence/import',
      method: 'post',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 导出威胁情报
  exportIntelligence(params: any) {
    return request({
      url: '/api/intelligence/export',
      method: 'get',
      params,
      responseType: 'blob'
    })
  }
}
