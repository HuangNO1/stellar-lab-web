import axios from 'axios'
import type { 
  LoginCredentials, LoginResponse, User, Lab, ResearchGroup, 
  Member, Paper, News, Project, EditRecord, PaginatedResponse, ApiResponse 
} from '@/types'
import { transformMembers, transformMember } from './memberTransform'

// 創建 axios 實例
const api = axios.create({
  baseURL: (import.meta as any)?.env?.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: (credentials: LoginCredentials): Promise<ApiResponse<LoginResponse>> => 
    api.post('/admin/login', credentials),
  
  logout: (): Promise<ApiResponse<void>> => 
    api.post('/auth/logout'),
  
  getProfile: (): Promise<ApiResponse<User>> => 
    api.get('/auth/me'),
}

export const labAPI = {
  getLab: (): Promise<ApiResponse<Lab>> => 
    api.get('/lab'),
  
  updateLab: (data: Partial<Lab>): Promise<ApiResponse<Lab>> => 
    api.put('/lab', data),
}

export const researchGroupAPI = {
  getGroups: (params?: any): Promise<ApiResponse<PaginatedResponse<ResearchGroup>>> => 
    api.get('/research_groups', { params }),
  
  getGroup: (id: number): Promise<ApiResponse<ResearchGroup>> => 
    api.get(`/research_groups/${id}`),
  
  createGroup: (data: Partial<ResearchGroup>): Promise<ApiResponse<ResearchGroup>> => 
    api.post('/research_groups', data),
  
  updateGroup: (id: number, data: Partial<ResearchGroup>): Promise<ApiResponse<ResearchGroup>> => 
    api.put(`/research_groups/${id}`, data),
  
  deleteGroup: (id: number): Promise<ApiResponse<void>> => 
    api.delete(`/research_groups/${id}`),
}

export const memberAPI = {
  getMembers: async (params?: any): Promise<ApiResponse<PaginatedResponse<Member>>> => {
    const response = await api.get('/members', { params }) as any as ApiResponse<PaginatedResponse<any>>
    const locale = localStorage.getItem('locale') || 'zh-CN'
    
    // 轉換成員數據
    const transformedData = transformMembers(response.data.data, locale)
    
    return {
      code: response.code,
      message: response.message,
      data: {
        ...response.data,
        data: transformedData
      }
    }
  },
  
  getMember: async (id: number): Promise<ApiResponse<Member>> => {
    const response = await api.get(`/members/${id}`) as any as ApiResponse<any>
    const locale = localStorage.getItem('locale') || 'zh-CN'
    
    // 轉換成員數據
    const transformedData = transformMember(response.data, locale)
    
    return {
      code: response.code,
      message: response.message,
      data: transformedData
    }
  },
  
  createMember: (data: Partial<Member>): Promise<ApiResponse<Member>> => 
    api.post('/members', data),
  
  updateMember: (id: number, data: Partial<Member>): Promise<ApiResponse<Member>> => 
    api.put(`/members/${id}`, data),
  
  deleteMember: (id: number): Promise<ApiResponse<void>> => 
    api.delete(`/members/${id}`),
  
  uploadAvatar: (id: number, file: File): Promise<ApiResponse<{ avatar_url: string }>> => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post(`/members/${id}/avatar`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
}

export const paperAPI = {
  getPapers: (params?: any): Promise<ApiResponse<PaginatedResponse<Paper>>> => 
    api.get('/papers', { params }),
  
  getPaper: (id: number): Promise<ApiResponse<Paper>> => 
    api.get(`/papers/${id}`),
  
  createPaper: (data: Partial<Paper>): Promise<ApiResponse<Paper>> => 
    api.post('/papers', data),
  
  updatePaper: (id: number, data: Partial<Paper>): Promise<ApiResponse<Paper>> => 
    api.put(`/papers/${id}`, data),
  
  deletePaper: (id: number): Promise<ApiResponse<void>> => 
    api.delete(`/papers/${id}`),
}

export const newsAPI = {
  getNews: (params?: any): Promise<ApiResponse<PaginatedResponse<News>>> => 
    api.get('/news', { params }),
  
  getNewsItem: (id: number): Promise<ApiResponse<News>> => 
    api.get(`/news/${id}`),
  
  createNews: (data: Partial<News>): Promise<ApiResponse<News>> => 
    api.post('/news', data),
  
  updateNews: (id: number, data: Partial<News>): Promise<ApiResponse<News>> => 
    api.put(`/news/${id}`, data),
  
  deleteNews: (id: number): Promise<ApiResponse<void>> => 
    api.delete(`/news/${id}`),
  
  uploadImage: (file: File): Promise<ApiResponse<{ image_url: string }>> => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/news/upload_image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
}

export const projectAPI = {
  getProjects: (params?: any): Promise<ApiResponse<PaginatedResponse<Project>>> => 
    api.get('/projects', { params }),
  
  getProject: (id: number): Promise<ApiResponse<Project>> => 
    api.get(`/projects/${id}`),
  
  createProject: (data: Partial<Project>): Promise<ApiResponse<Project>> => 
    api.post('/projects', data),
  
  updateProject: (id: number, data: Partial<Project>): Promise<ApiResponse<Project>> => 
    api.put(`/projects/${id}`, data),
  
  deleteProject: (id: number): Promise<ApiResponse<void>> => 
    api.delete(`/projects/${id}`),
}

export const adminAPI = {
  getAdmins: (params?: any): Promise<ApiResponse<PaginatedResponse<User>>> => 
    api.get('/admins', { params }),
  
  createAdmin: (data: { admin_name: string; admin_pass: string }): Promise<ApiResponse<User>> => 
    api.post('/admins', data),
  
  updateAdmin: (id: number, data: Partial<User>): Promise<ApiResponse<User>> => 
    api.put(`/admins/${id}`, data),
  
  deleteAdmin: (id: number): Promise<ApiResponse<void>> => 
    api.delete(`/admins/${id}`),
}

export const editRecordAPI = {
  getRecords: (params?: any): Promise<ApiResponse<PaginatedResponse<EditRecord>>> => 
    api.get('/edit_records', { params }),
}

export default api