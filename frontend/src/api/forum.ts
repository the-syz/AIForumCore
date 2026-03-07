import http from './http'
import { useMock } from './mock'

interface Comment {
  id: number
  content: string
  user_id: number
  post_id: number
  parent_id: number | null
  created_at: string
  updated_at: string
}



interface Favorite {
  id: number
  user_id: number
  target_type: string
  target_id: number
  created_at: string
}

// 发表评论
export const createComment = async (content: string, postId: number, parentId?: number): Promise<Comment> => {
  if (useMock) {
    const newComment: Comment = {
      id: Math.floor(Math.random() * 1000),
      content,
      user_id: 1,
      post_id: postId,
      parent_id: parentId || null,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    return Promise.resolve(newComment)
  }
  return http.post('/forum/comments', {
    content,
    post_id: postId,
    parent_id: parentId
  })
}

// 获取评论列表
export const getComments = async (postId?: number): Promise<Comment[]> => {
  if (useMock) {
    return Promise.resolve([])
  }
  const url = postId ? `/forum/comments?post_id=${postId}` : '/forum/comments'
  return http.get(url)
}

// 点赞/取消点赞
export const toggleLike = async (targetType: string, targetId: number): Promise<{ message: string }> => {
  if (useMock) {
    return Promise.resolve({ message: '点赞成功' })
  }
  return http.post('/forum/likes', {
    target_type: targetType,
    target_id: targetId
  })
}

// 收藏/取消收藏
export const toggleFavorite = async (targetType: string, targetId: number): Promise<{ message: string }> => {
  if (useMock) {
    return Promise.resolve({ message: '收藏成功' })
  }
  return http.post('/forum/favorites', {
    target_type: targetType,
    target_id: targetId
  })
}

// 获取收藏列表
export const getFavorites = async (): Promise<Favorite[]> => {
  if (useMock) {
    return Promise.resolve([])
  }
  return http.get('/forum/favorites')
}
