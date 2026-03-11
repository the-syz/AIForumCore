import http from './http'

interface ReferenceItem {
  type: string
  id: number
  title: string
  score: number
}

interface SelectedContent {
  type: string
  id: number
  title: string
}

interface ChatRequest {
  message: string
  conversation_id?: number
  selected_contents?: SelectedContent[]
}

interface ChatResponse {
  answer: string
  references: ReferenceItem[]
}

interface Conversation {
  id: number
  topic: string
  created_at: string
  updated_at: string
}

interface Message {
  id: number
  role: string
  content: string
  created_at: string
}

interface ConversationHistoryResponse {
  conversation: Conversation
  messages: Message[]
}

interface SearchKnowledgeBaseRequest {
  query: string
  top_k?: number
}

interface SearchKnowledgeBaseResponse {
  results: ReferenceItem[]
}

export const sendChatMessage = async (data: ChatRequest): Promise<ChatResponse> => {
  return http.post('/ai/chat', data)
}

export const searchKnowledgeBase = async (data: SearchKnowledgeBaseRequest): Promise<SearchKnowledgeBaseResponse> => {
  return http.post('/ai/search', data)
}

export const createNewConversation = async (topic?: string): Promise<Conversation> => {
  return http.post('/ai/chat/new', topic ? { topic } : {})
}

export const getChatHistory = async (conversation_id?: number): Promise<{ conversations?: Conversation[], conversation?: Conversation, messages?: Message[] }> => {
  const params = conversation_id ? { conversation_id } : {}
  return http.get('/ai/history', { params })
}

export const deleteConversation = async (conversation_id: number): Promise<{ message: string }> => {
  return http.delete(`/ai/conversation/${conversation_id}`)
}

export type { SelectedContent, ReferenceItem }
