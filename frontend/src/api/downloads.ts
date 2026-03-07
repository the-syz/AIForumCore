import http from './http'
import { useMock, mockData } from './mock'

interface Download {
  id: number
  title: string
  description: string
  category: string
  file_path: string
  file_name: string
  uploader_id: number
  upload_time: string
  download_count: number
}

// 获取下载资源列表
export const getDownloads = async (): Promise<Download[]> => {
  if (useMock) {
    return Promise.resolve(mockData.downloads)
  }
  return http.get('/downloads/')
}

// 获取下载资源详情
export const getDownloadById = async (id: number): Promise<Download> => {
  if (useMock) {
    const download = mockData.downloads.find(d => d.id === id)
    if (!download) {
      throw new Error('资源不存在')
    }
    return Promise.resolve(download)
  }
  return http.get(`/downloads/${id}`)
}

// 上传下载资源
export const uploadDownload = async (formData: FormData): Promise<Download> => {
  if (useMock) {
    const newDownload: Download = {
      id: mockData.downloads.length + 1,
      title: formData.get('title') as string,
      description: formData.get('description') as string,
      category: formData.get('category') as string,
      file_path: '/downloads/new_resource.pdf',
      file_name: 'new_resource.pdf',
      uploader_id: 1,
      upload_time: new Date().toISOString(),
      download_count: 0
    }
    mockData.downloads.push(newDownload)
    return Promise.resolve(newDownload)
  }
  return http.post('/downloads/', formData)
}

// 更新下载资源
export const updateDownload = async (id: number, data: Partial<Download>): Promise<Download> => {
  if (useMock) {
    const index = mockData.downloads.findIndex(d => d.id === id)
    if (index === -1) {
      throw new Error('资源不存在')
    }
    const updatedDownload = { ...mockData.downloads[index], ...data } as Download
    mockData.downloads[index] = updatedDownload
    return Promise.resolve(updatedDownload)
  }
  return http.put(`/downloads/${id}`, data)
}

// 删除下载资源
export const deleteDownload = async (id: number): Promise<{ message: string }> => {
  if (useMock) {
    const index = mockData.downloads.findIndex(d => d.id === id)
    if (index === -1) {
      throw new Error('资源不存在')
    }
    mockData.downloads.splice(index, 1)
    return Promise.resolve({ message: '资源删除成功' })
  }
  return http.delete(`/downloads/${id}`)
}

// 下载资源
export const downloadResource = async (id: number): Promise<void> => {
  if (useMock) {
    // 模拟下载
    const download = mockData.downloads.find(d => d.id === id)
    if (download) {
      download.download_count++
    }
    console.log(`下载资源 ID: ${id}`)
    return Promise.resolve()
  }
  // 真实API需要处理文件下载
  const response = await fetch(`/api/downloads/${id}/download`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`
    }
  })
  const blob = await response.blob()
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `resource_${id}.pdf`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  window.URL.revokeObjectURL(url)
}
