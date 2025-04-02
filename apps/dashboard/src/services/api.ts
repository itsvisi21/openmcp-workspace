import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
})

export interface ContextData {
  content: string
  type: 'code' | 'documentation' | 'conversation' | 'other'
  metadata: Record<string, unknown>
}

export interface ContextResponse {
  id: string
  content: string
  type: string
  metadata: Record<string, unknown>
  created_at: string
  updated_at: string
}

export async function commitContext(data: ContextData): Promise<ContextResponse> {
  const response = await api.post<ContextResponse>('/context/commit', data)
  return response.data
}

export async function getContextHistory(): Promise<ContextResponse[]> {
  const response = await api.get<ContextResponse[]>('/context/list')
  return response.data
}

export async function getContextById(id: string): Promise<ContextResponse> {
  const response = await api.get<ContextResponse>(`/context/${id}`)
  return response.data
}

export async function deleteContext(id: string): Promise<void> {
  await api.delete(`/context/${id}`)
} 