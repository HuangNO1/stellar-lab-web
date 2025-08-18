import axios from 'axios';
import Cookies from 'js-cookie';
import { getConfig } from '@/config/runtime';
import type { 
  ApiResponse, 
  PaginatedResponse, 
  Lab, 
  ResearchGroup, 
  ResearchGroupQueryParams,
  Member, 
  MemberQueryParams,
  Paper, 
  PaperQueryParams,
  News, 
  NewsQueryParams,
  Project, 
  ProjectQueryParams,
  Resource,
  ResourceQueryParams,
  Admin,
  AdminQueryParams,
  EditRecord,
  EditRecordQueryParams,
  LoginResponse
} from '@/types/api';

// Get runtime configuration
const config = getConfig();

// Debug: 打印配置資訊
if (process.env.NODE_ENV === 'development') {
    console.log('=== API Configuration Debug ===');
    console.log('BACKEND_URL:', config.BACKEND_URL);
    console.log('API_BASE_URL (Full URL):', config.API_BASE_URL);
    console.log('Final baseURL:', config.API_BASE_URL);
    console.log('================================');
}

// 創建 axios 實例
const api = axios.create({
    baseURL: config.API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
    // 安全配置
    withCredentials: false, // 關閉自動發送cookies，使用token認證更安全
    maxRedirects: 3, // 限制重定向次數
});

// 請求攔截器
api.interceptors.request.use(
    (config) => {
        // 優先使用管理員token
        const adminToken = localStorage.getItem('admin_token');
        const userToken = localStorage.getItem('token');
        
        const token = adminToken || userToken;
        if (token) {
            config.headers.Authorization = token.startsWith('Bearer ') ? token : `Bearer ${token}`;
        }
        
        // 添加語言設置頭部
        const currentLanguage = Cookies.get('language') || 'zh';
        config.headers['Accept-Language'] = currentLanguage;
        config.headers['X-Language'] = currentLanguage;
        
        // 安全檢查：清理請求數據中的潛在XSS
        if (config.data && typeof config.data === 'object') {
            config.data = sanitizeRequestData(config.data);
        }
        
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 輸入清理函數
function sanitizeRequestData(data: unknown): unknown {
    // 跳過 FormData, File, Blob 等二進制數據類型
    if (data instanceof FormData || data instanceof File || data instanceof Blob) {
        return data;
    }
    
    if (typeof data === 'string') {
        // 移除潛在的腳本標籤和事件處理器
        return data
            .replace(/<script[^>]*>.*?<\/script>/gi, '')
            .replace(/on\w+\s*=\s*["'][^"']*["']/gi, '')
            .replace(/javascript:/gi, '');
    } else if (Array.isArray(data)) {
        return data.map(sanitizeRequestData);
    } else if (typeof data === 'object' && data !== null) {
        const sanitized: Record<string, unknown> = {};
        for (const key in data) {
            if (Object.prototype.hasOwnProperty.call(data, key)) {
                sanitized[key] = sanitizeRequestData((data as Record<string, unknown>)[key]);
            }
        }
        return sanitized;
    }
    return data;
}

// 響應攔截器
api.interceptors.response.use(
    (response) => {
        return response.data;
    },
    (error) => {
        // 401 未授權處理
        if (error.response?.status === 401) {
            // 清除所有token
            localStorage.removeItem('token');
            localStorage.removeItem('admin_token');
            localStorage.removeItem('admin_info');
            
            // 根據當前路徑跳轉
            const currentPath = window.location.pathname;
            if (currentPath.startsWith('/admin')) {
                window.location.href = '/admin/login';
            }
        }
        
        // 創建包含服務器消息的錯誤對象
        const errorResponse = {
            code: error.response?.data?.code || error.response?.status || -1,
            message: error.response?.data?.message || error.response?.statusText || error.message || 'Unknown error',
            data: error.response?.data?.data || null,
            status: error.response?.status
        };
        
        return Promise.reject(errorResponse);
    }
);

/**
 * 實驗室相關 API
 */
export const labApi = {
  // 獲取實驗室資訊
  getLab(): Promise<ApiResponse<Lab>> {
    return api.get('/lab');
  },
  
  // 更新實驗室資訊
  updateLab(data: FormData | Partial<Lab>): Promise<ApiResponse<Lab>> {
    if (data instanceof FormData) {
      return api.put('/lab', data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    } else {
      return api.put('/lab', data);
    }
  },
  
  // 刪除實驗室
  deleteLab(): Promise<ApiResponse<null>> {
    return api.delete('/lab');
  }
};

/**
 * 課題組相關 API
 */
export const researchGroupApi = {
  // 獲取課題組列表
  getResearchGroups(params?: ResearchGroupQueryParams): Promise<ApiResponse<PaginatedResponse<ResearchGroup>>> {
    return api.get('/research-groups', { params });
  },
  
  // 獲取課題組詳情
  getResearchGroup(groupId: number): Promise<ApiResponse<ResearchGroup>> {
    return api.get(`/research-groups/${groupId}`);
  },
  
  // 創建課題組
  createResearchGroup(data: Partial<ResearchGroup>): Promise<ApiResponse<ResearchGroup>> {
    return api.post('/research-groups', data);
  },
  
  // 更新課題組
  updateResearchGroup(groupId: number, data: Partial<ResearchGroup>): Promise<ApiResponse<ResearchGroup>> {
    return api.put(`/research-groups/${groupId}`, data);
  },
  
  // 刪除課題組
  deleteResearchGroup(groupId: number): Promise<ApiResponse<null>> {
    return api.delete(`/research-groups/${groupId}`);
  }
};

/**
 * 成員相關 API
 */
export const memberApi = {
  // 獲取成員列表
  getMembers(params?: MemberQueryParams): Promise<ApiResponse<PaginatedResponse<Member>>> {
    return api.get('/members', { params });
  },
  
  // 獲取成員詳情
  getMember(memberId: number): Promise<ApiResponse<Member>> {
    return api.get(`/members/${memberId}`);
  },
  
  // 創建成員
  createMember(data: FormData | Partial<Member>): Promise<ApiResponse<Member>> {
    if (data instanceof FormData) {
      return api.post('/members', data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    } else {
      return api.post('/members', data);
    }
  },
  
  // 更新成員
  updateMember(memberId: number, data: FormData | Partial<Member>): Promise<ApiResponse<Member>> {
    if (data instanceof FormData) {
      return api.put(`/members/${memberId}`, data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    } else {
      return api.put(`/members/${memberId}`, data);
    }
  },
  
  // 刪除成員
  deleteMember(memberId: number): Promise<ApiResponse<null>> {
    return api.delete(`/members/${memberId}`);
  },
  
  // 批量刪除成員
  deleteMembersBatch(memberIds: number[]): Promise<ApiResponse<null>> {
    return api.delete('/members/batch', { data: { member_ids: memberIds } });
  },
  
  // 批量更新成員
  updateMembersBatch(memberIds: number[], updates: Partial<Member>): Promise<ApiResponse<null>> {
    return api.put('/members/batch', { member_ids: memberIds, updates });
  }
};

/**
 * 論文相關 API
 */
export const paperApi = {
  // 獲取論文列表
  getPapers(params?: PaperQueryParams): Promise<ApiResponse<PaginatedResponse<Paper>>> {
    return api.get('/papers', { params });
  },
  
  // 獲取論文詳情
  getPaper(paperId: number): Promise<ApiResponse<Paper>> {
    return api.get(`/papers/${paperId}`);
  },
  
  // 創建論文
  createPaper(data: FormData | Partial<Paper>): Promise<ApiResponse<Paper>> {
    if (data instanceof FormData) {
      return api.post('/papers', data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    } else {
      return api.post('/papers', data);
    }
  },
  
  // 更新論文
  updatePaper(paperId: number, data: FormData | Partial<Paper>): Promise<ApiResponse<Paper>> {
    if (data instanceof FormData) {
      return api.put(`/papers/${paperId}`, data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    } else {
      return api.put(`/papers/${paperId}`, data);
    }
  },
  
  // 刪除論文
  deletePaper(paperId: number): Promise<ApiResponse<null>> {
    return api.delete(`/papers/${paperId}`);
  }
};

/**
 * 新聞相關 API
 */
export const newsApi = {
  // 獲取新聞列表
  getNews(params?: NewsQueryParams): Promise<ApiResponse<PaginatedResponse<News>>> {
    return api.get('/news', { params });
  },
  
  // 獲取新聞詳情
  getNewsItem(newsId: number): Promise<ApiResponse<News>> {
    return api.get(`/news/${newsId}`);
  },
  
  // 創建新聞
  createNews(data: Partial<News>): Promise<ApiResponse<News>> {
    return api.post('/news', data);
  },
  
  // 更新新聞
  updateNews(newsId: number, data: Partial<News>): Promise<ApiResponse<News>> {
    return api.put(`/news/${newsId}`, data);
  },
  
  // 刪除新聞
  deleteNews(newsId: number): Promise<ApiResponse<null>> {
    return api.delete(`/news/${newsId}`);
  }
};

/**
 * 項目相關 API
 */
export const projectApi = {
  // 獲取項目列表
  getProjects(params?: ProjectQueryParams): Promise<ApiResponse<PaginatedResponse<Project>>> {
    return api.get('/projects', { params });
  },
  
  // 獲取項目詳情
  getProject(projectId: number): Promise<ApiResponse<Project>> {
    return api.get(`/projects/${projectId}`);
  },
  
  // 創建項目
  createProject(data: Partial<Project>): Promise<ApiResponse<Project>> {
    return api.post('/projects', data);
  },
  
  // 更新項目
  updateProject(projectId: number, data: Partial<Project>): Promise<ApiResponse<Project>> {
    return api.put(`/projects/${projectId}`, data);
  },
  
  // 刪除項目
  deleteProject(projectId: number): Promise<ApiResponse<null>> {
    return api.delete(`/projects/${projectId}`);
  }
};

/**
 * 資源相關 API
 */
export const resourceApi = {
  // 獲取資源列表（公開訪問）
  getResources(params?: ResourceQueryParams): Promise<ApiResponse<PaginatedResponse<Resource>>> {
    return api.get('/resources', { params });
  },
  
  // 獲取資源列表（管理員）
  getAdminResources(params?: ResourceQueryParams): Promise<ApiResponse<PaginatedResponse<Resource>>> {
    return api.get('/admin/resources', { params });
  },
  
  // 獲取資源詳情
  getResource(resourceId: number): Promise<ApiResponse<Resource>> {
    return api.get(`/resources/${resourceId}`);
  },
  
  // 創建資源
  createResource(data: FormData | Partial<Resource>): Promise<ApiResponse<Resource>> {
    if (data instanceof FormData) {
      return api.post('/admin/resources', data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    } else {
      return api.post('/admin/resources', data);
    }
  },
  
  // 更新資源
  updateResource(resourceId: number, data: FormData | Partial<Resource>): Promise<ApiResponse<Resource>> {
    if (data instanceof FormData) {
      return api.put(`/admin/resources/${resourceId}`, data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    } else {
      return api.put(`/admin/resources/${resourceId}`, data);
    }
  },
  
  // 刪除資源
  deleteResource(resourceId: number): Promise<ApiResponse<null>> {
    return api.delete(`/admin/resources/${resourceId}`);
  },
  
  // 批量刪除資源
  batchDeleteResources(resourceIds: number[]): Promise<ApiResponse<null>> {
    return api.delete('/admin/resources/batch', { data: { resource_ids: resourceIds } });
  }
};

/**
 * 認證相關 API
 */
export const authApi = {
  // 管理員登錄
  login(adminName: string, adminPass: string): Promise<ApiResponse<LoginResponse>> {
    return api.post('/admin/login', { admin_name: adminName, admin_pass: adminPass });
  },
  
  // 管理員登出
  logout(): Promise<ApiResponse<null>> {
    return api.post('/admin/logout');
  },
  
  // 修改密碼
  changePassword(oldPassword: string, newPassword: string): Promise<ApiResponse<null>> {
    return api.post('/admin/change-password', { 
      old_password: oldPassword, 
      new_password: newPassword 
    });
  },
  
  // 獲取個人資訊
  getProfile(): Promise<ApiResponse<Admin>> {
    return api.get('/admin/profile');
  },
  
  // 更新個人資訊
  updateProfile(data: Partial<Admin>): Promise<ApiResponse<Admin>> {
    return api.put('/admin/profile', data);
  }
};

/**
 * 媒體文件相關 API
 */
export const mediaApi = {
  // 上傳文件
  uploadFile(file: File, type: 'lab_logo' | 'member_avatar' | 'paper' | 'other'): Promise<ApiResponse<{ filename: string; url: string }>> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);
    
    return api.post('/media/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  // 獲取文件資訊
  getFileInfo(filePath: string): Promise<ApiResponse<{ filename: string; size: number; mime_type: string; created_at: string; url: string }>> {
    return api.get(`/media/info/${filePath}`);
  },
  
  // 健康檢查
  healthCheck(): Promise<ApiResponse<{ status: string; upload_path: string; disk_space: string }>> {
    return api.get('/media/health');
  }
};

/**
 * 管理員相關 API
 */
export const adminApi = {
  // 獲取管理員列表
  getAdmins(params?: AdminQueryParams): Promise<ApiResponse<PaginatedResponse<Admin>>> {
    return api.get('/admins', { params });
  },
  
  // 創建管理員
  createAdmin(data: {
    admin_name: string;
    admin_pass: string;
    is_super?: number;
  }): Promise<ApiResponse<Admin>> {
    return api.post('/admins', data);
  },
  
  // 更新管理員
  updateAdmin(adminId: number, data: {
    admin_name?: string;
    is_super?: number;
    enable?: number;
  }): Promise<ApiResponse<Admin>> {
    return api.put(`/admins/${adminId}`, data);
  },
  
  // 刪除管理員
  deleteAdmin(adminId: number): Promise<ApiResponse<null>> {
    return api.delete(`/admins/${adminId}`);
  },

  // 重置管理員密碼（超級管理員功能）
  resetAdminPassword(adminId: number, newPassword: string): Promise<ApiResponse<null>> {
    return api.post(`/admins/${adminId}/reset-password`, { new_password: newPassword });
  }
};

/**
 * 操作日誌相關 API
 */
export const editRecordApi = {
  // 獲取編輯記錄列表
  getEditRecords(params?: EditRecordQueryParams): Promise<ApiResponse<PaginatedResponse<EditRecord>>> {
    return api.get('/edit-records', { params });
  },
  
  // 獲取編輯記錄詳情
  getEditRecord(editId: number): Promise<ApiResponse<EditRecord>> {
    return api.get(`/edit-records/${editId}`);
  }
};

/**
 * 圖片上傳相關 API
 */
export const imageApi = {
  // 上傳圖片（用於Markdown編輯器）
  uploadImage(file: File, entityType?: string, entityId?: number, fieldName?: string): Promise<ApiResponse<{
    file_url: string;
    filename: string;
    file_path: string;
  }>> {
    const formData = new FormData();
    formData.append('file', file);
    if (entityType) formData.append('entity_type', entityType);
    if (entityId) formData.append('entity_id', entityId.toString());
    if (fieldName) formData.append('field_name', fieldName);

    return api.post('/images/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }
};

/**
 * 系統相關 API
 */
export const systemApi = {
  // 健康檢查 - 注意：此接口直接返回數據，不是標準的ApiResponse格式
  healthCheck(): Promise<{ message: string; status: string; timestamp: string; version: string }> {
    return api.get('/health');
  }
};