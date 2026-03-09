import http from './http'
import { useUserStore } from '@/store/user'

interface UploadResponse {
  file_path: string
  file_name: string
  file_size: number
  message: string
}

// 上传附件
export const uploadAttachment = async (file: File): Promise<UploadResponse> => {
  const userStore = useUserStore()
  const token = userStore.token
  
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await fetch('/api/files/upload/attachment', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`
    },
    body: formData
  })
  
  if (!response.ok) {
    throw new Error('上传失败')
  }
  
  return response.json()
}

// 删除附件
export const deleteAttachment = async (filePath: string): Promise<{ message: string }> => {
  const userStore = useUserStore()
  const token = userStore.token
  
  const response = await fetch(`/api/files/upload/attachment?file_path=${encodeURIComponent(filePath)}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  
  if (!response.ok) {
    throw new Error('删除失败')
  }
  
  return response.json()
}