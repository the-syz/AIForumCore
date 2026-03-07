import http from './http'
import { useMock, mockData } from './mock'

interface Post {
  id: number
  title: string
  content: string
  category: string
  author_id: number
  created_at: string
  updated_at: string
  is_pinned: boolean
  is_draft: boolean
  view_count: number
  like_count: number
  comment_count: number
}

// 获取经验贴列表
export const getPosts = async (): Promise<Post[]> => {
  if (useMock) {
    return Promise.resolve(mockData.posts)
  }
  return http.get('/posts/')
}

// 获取经验贴详情
export const getPostById = async (id: number): Promise<Post> => {
  if (useMock) {
    const post = mockData.posts.find(p => p.id === id)
    if (!post) {
      throw new Error('经验贴不存在')
    }
    // 模拟浏览次数增加
    post.view_count++
    return Promise.resolve(post)
  }
  return http.get(`/posts/${id}`)
}

// 获取草稿列表
export const getDrafts = async (): Promise<Post[]> => {
  if (useMock) {
    const drafts = mockData.posts.filter(p => p.is_draft)
    return Promise.resolve(drafts)
  }
  return http.get('/posts/drafts')
}

// 发布经验贴
export const createPost = async (formData: FormData): Promise<Post> => {
  if (useMock) {
    const newPost: Post = {
      id: mockData.posts.length + 1,
      title: formData.get('title') as string,
      content: formData.get('content') as string,
      category: formData.get('category') as string,
      author_id: 1,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      is_pinned: false,
      is_draft: formData.get('is_draft') === 'true',
      view_count: 0,
      like_count: 0,
      comment_count: 0
    }
    mockData.posts.push(newPost)
    return Promise.resolve(newPost)
  }
  return http.post('/posts/', formData)
}

// 更新经验贴
export const updatePost = async (id: number, data: Partial<Post>): Promise<Post> => {
  if (useMock) {
    const index = mockData.posts.findIndex(p => p.id === id)
    if (index === -1) {
      throw new Error('经验贴不存在')
    }
    const updatedPost = { ...mockData.posts[index], ...data, updated_at: new Date().toISOString() } as Post
    mockData.posts[index] = updatedPost
    return Promise.resolve(updatedPost)
  }
  return http.put(`/posts/${id}`, data)
}

// 删除经验贴
export const deletePost = async (id: number): Promise<{ message: string }> => {
  if (useMock) {
    const index = mockData.posts.findIndex(p => p.id === id)
    if (index === -1) {
      throw new Error('经验贴不存在')
    }
    mockData.posts.splice(index, 1)
    return Promise.resolve({ message: '经验贴删除成功' })
  }
  return http.delete(`/posts/${id}`)
}

// 置顶/取消置顶经验贴
export const pinPost = async (id: number, isPinned: boolean): Promise<{ message: string }> => {
  if (useMock) {
    const index = mockData.posts.findIndex(p => p.id === id)
    if (index === -1) {
      throw new Error('经验贴不存在')
    }
    const post = mockData.posts[index]
    if (post) {
      post.is_pinned = isPinned
    }
    return Promise.resolve({ message: '置顶状态更新成功' })
  }
  return http.put(`/posts/${id}/pin`, { is_pinned: isPinned })
}
