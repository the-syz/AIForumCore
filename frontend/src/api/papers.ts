import http from './http'
import { useMock, mockData } from './mock'

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

// 获取论文列表
export const getPapers = async (): Promise<Paper[]> => {
  if (useMock) {
    return Promise.resolve(mockData.papers)
  }
  return http.get('/papers/')
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
  const response = await fetch(`/api/papers/${id}/download`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`
    }
  })
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
