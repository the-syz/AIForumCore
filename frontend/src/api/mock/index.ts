// Mock数据配置
import { paperMockData } from './papers'
import { postMockData } from './posts'
import { downloadMockData } from './downloads'
import { userMockData } from './user'

// 是否使用mock数据
export const useMock = true

// Mock数据导出
export const mockData = {
  papers: paperMockData,
  posts: postMockData,
  downloads: downloadMockData,
  user: userMockData
}
