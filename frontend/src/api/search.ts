import http from './http'
import { useMock, mockData } from './mock'

interface SearchResult {
  total: number
  page: number
  page_size: number
  items: any[]
}

// 搜索论文
export const searchPapers = async (keyword: string, page: number = 1, pageSize: number = 20): Promise<SearchResult> => {
  if (useMock) {
    const results = mockData.papers.filter(p => 
      p.title.includes(keyword) || 
      p.abstract.includes(keyword) || 
      p.authors.includes(keyword)
    )
    return Promise.resolve({
      total: results.length,
      page,
      page_size: pageSize,
      items: results
    })
  }
  return http.get(`/search/papers?keyword=${encodeURIComponent(keyword)}&page=${page}&page_size=${pageSize}`)
}

// 搜索经验贴
export const searchPosts = async (keyword: string, page: number = 1, pageSize: number = 20): Promise<SearchResult> => {
  if (useMock) {
    const results = mockData.posts.filter(p => 
      p.title.includes(keyword) || 
      p.content.includes(keyword)
    )
    return Promise.resolve({
      total: results.length,
      page,
      page_size: pageSize,
      items: results
    })
  }
  return http.get(`/search/posts?keyword=${encodeURIComponent(keyword)}&page=${page}&page_size=${pageSize}`)
}

// 搜索下载中心
export const searchDownloads = async (keyword: string, page: number = 1, pageSize: number = 20): Promise<SearchResult> => {
  if (useMock) {
    const results = mockData.downloads.filter(d => 
      d.title.includes(keyword) || 
      d.description.includes(keyword)
    )
    return Promise.resolve({
      total: results.length,
      page,
      page_size: pageSize,
      items: results
    })
  }
  return http.get(`/search/downloads?keyword=${encodeURIComponent(keyword)}&page=${page}&page_size=${pageSize}`)
}

// 综合搜索
export const searchAll = async (keyword: string, page: number = 1, pageSize: number = 20): Promise<SearchResult> => {
  if (useMock) {
    const paperResults = mockData.papers.filter(p => 
      p.title.includes(keyword) || 
      p.abstract.includes(keyword) || 
      p.authors.includes(keyword)
    )
    const postResults = mockData.posts.filter(p => 
      p.title.includes(keyword) || 
      p.content.includes(keyword)
    )
    const downloadResults = mockData.downloads.filter(d => 
      d.title.includes(keyword) || 
      d.description.includes(keyword)
    )
    const allResults = [...paperResults, ...postResults, ...downloadResults]
    return Promise.resolve({
      total: allResults.length,
      page,
      page_size: pageSize,
      items: allResults
    })
  }
  return http.get(`/search/all?keyword=${encodeURIComponent(keyword)}&page=${page}&page_size=${pageSize}`)
}
