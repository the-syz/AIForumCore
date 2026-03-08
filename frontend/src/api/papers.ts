import http from './http'
import { useMock, mockData } from './mock'
import { useUserStore } from '@/store/user'

interface Paper {
  id: number
  title: string
  authors: string
  abstract: string
  keywords: string
  doi: string
  paper_type: string
  category: string
  file_path: string
  uploader_id: number
  upload_time: string
  download_count: number
}

interface PapersResponse {
  items: Paper[]
  total: number
  page: number
  page_size: number
}

// 获取论文列表
export const getPapers = async (params?: {
  page?: number
  page_size?: number
  keyword?: string
}): Promise<PapersResponse> => {
  if (useMock) {
    let filteredPapers = [...mockData.papers]
    
    // 搜索功能
    if (params?.keyword) {
      const keyword = params.keyword.toLowerCase()
      filteredPapers = filteredPapers.filter(p => 
        p.title.toLowerCase().includes(keyword) || 
        p.abstract.toLowerCase().includes(keyword) || 
        p.authors.toLowerCase().includes(keyword)
      )
    }
    
    // 分页功能
    const page = params?.page || 1
    const page_size = params?.page_size || 10
    const start = (page - 1) * page_size
    const end = start + page_size
    const paginatedPapers = filteredPapers.slice(start, end)
    
    return Promise.resolve({
      items: paginatedPapers,
      total: filteredPapers.length,
      page,
      page_size
    })
  }
  
  // 调用真实后端API
  const response = await http.get('/papers/', { params })
  console.log('后端返回的论文列表数据:', response)
  
  // 检查后端返回的数据结构并适配
  if (Array.isArray(response)) {
    // 如果后端直接返回论文数组
    return {
      items: response,
      total: response.length,
      page: params?.page || 1,
      page_size: params?.page_size || 10
    }
  } else if (response.items && Array.isArray(response.items)) {
    // 如果后端返回的是符合PapersResponse接口的数据结构
    return response
  } else {
    // 其他情况，返回空数据
    console.warn('后端返回的数据结构不符合预期:', response)
    return {
      items: [],
      total: 0,
      page: params?.page || 1,
      page_size: params?.page_size || 10
    }
  }
}

// 获取论文详情
export const getPaperById = async (id: number): Promise<Paper> => {
  if (useMock) {
    const paper = mockData.papers.find(p => p.id === id)
    if (!paper) {
      throw new Error('论文不存在')
    }
    return Promise.resolve(paper)
  }
  return http.get(`/papers/${id}`)
}

// 上传论文
export const uploadPaper = async (formData: FormData): Promise<Paper> => {
  if (useMock) {
    const newPaper: Paper = {
      id: mockData.papers.length + 1,
      title: formData.get('title') as string,
      authors: formData.get('authors') as string,
      abstract: formData.get('abstract') as string,
      keywords: formData.get('keywords') as string,
      doi: formData.get('doi') as string,
      paper_type: formData.get('paper_type') as string,
      category: formData.get('category') as string,
      file_path: '/papers/new_paper.pdf',
      uploader_id: 1,
      upload_time: new Date().toISOString(),
      download_count: 0
    }
    mockData.papers.push(newPaper)
    return Promise.resolve(newPaper)
  }
  return http.post('/papers/', formData)
}

// 创建论文
export const createPaper = async (data: Partial<Paper>): Promise<Paper> => {
  if (useMock) {
    const newPaper: Paper = {
      id: mockData.papers.length + 1,
      title: data.title || '',
      authors: data.authors || '',
      abstract: data.abstract || '',
      keywords: data.keywords || '',
      doi: data.doi || '',
      paper_type: data.paper_type || '',
      category: data.category || '',
      file_path: '/papers/new_paper.pdf',
      uploader_id: 1,
      upload_time: new Date().toISOString(),
      download_count: 0
    }
    mockData.papers.push(newPaper)
    return Promise.resolve(newPaper)
  }
  return http.post('/papers/', data)
}

// 更新论文信息
export const updatePaper = async (id: number, data: Partial<Paper>): Promise<Paper> => {
  if (useMock) {
    const index = mockData.papers.findIndex(p => p.id === id)
    if (index === -1) {
      throw new Error('论文不存在')
    }
    const updatedPaper = { ...mockData.papers[index], ...data } as Paper
    mockData.papers[index] = updatedPaper
    return Promise.resolve(updatedPaper)
  }
  return http.put(`/papers/${id}`, data)
}

// 删除论文
export const deletePaper = async (id: number): Promise<{ message: string }> => {
  if (useMock) {
    const index = mockData.papers.findIndex(p => p.id === id)
    if (index === -1) {
      throw new Error('论文不存在')
    }
    mockData.papers.splice(index, 1)
    return Promise.resolve({ message: '论文删除成功' })
  }
  return http.delete(`/papers/${id}`)
}

// 下载论文
export const downloadPaper = async (id: number): Promise<void> => {
  if (useMock) {
    // 模拟下载
    console.log(`下载论文 ID: ${id}`)
    return Promise.resolve()
  }
  // 真实API需要处理文件下载
  const userStore = useUserStore()
  const token = userStore.token
  
  const response = await fetch(`/api/papers/${id}/download`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  
  if (!response.ok) {
    throw new Error(`下载失败: ${response.status}`)
  }
  
  const blob = await response.blob()
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `paper_${id}.pdf`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  window.URL.revokeObjectURL(url)
}

// 搜索论文
export const searchPapers = async (keyword: string): Promise<Paper[]> => {
  if (useMock) {
    const results = mockData.papers.filter(p => 
      p.title.includes(keyword) || 
      p.abstract.includes(keyword) || 
      p.authors.includes(keyword)
    )
    return Promise.resolve(results)
  }
  return http.get(`/papers/search?keyword=${encodeURIComponent(keyword)}`)
}

// 解析论文
export const parsePaper = async (fileId: number): Promise<Partial<Paper>> => {
  if (useMock) {
    // 模拟解析结果
    return Promise.resolve({
      title: '模拟论文标题',
      authors: '作者1, 作者2',
      abstract: '这是论文摘要...',
      keywords: '关键词1, 关键词2, 关键词3',
      doi: '',
      paper_type: 'journal',
      category: 'computer_vision'
    })
  }
  // 尝试使用URL参数格式
  return http.post(`/papers/parse/${fileId}`)
}
