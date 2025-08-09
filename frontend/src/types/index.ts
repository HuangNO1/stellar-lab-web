// 用戶相關
export interface User {
  id: number
  username: string
  role: 'admin' | 'user'
  email?: string
  created_at: string
  enable: boolean
}

export interface LoginCredentials {
  admin_name: string
  admin_pass: string
}

export interface LoginResponse {
  access_token: string
  expires_in: number
  admin: {
    admin_id: number
    admin_name: string
    is_super: number
  }
}

// 實驗室相關
export interface Lab {
  lab_id: number
  lab_logo_path?: string
  lab_zh?: string
  lab_en?: string
  lab_desc_zh?: string
  lab_desc_en?: string
  lab_address_zh?: string
  lab_address_en?: string
  lab_email?: string
  lab_phone?: string
  enable: number
}

// 課題組相關
export interface ResearchGroup {
  research_group_id: number
  lab_id: number
  research_group_name_zh?: string
  research_group_name_en?: string
  research_group_desc_zh?: string
  research_group_desc_en?: string
  mem_id?: number
  enable: number
  created_at?: string
  updated_at?: string
}

// 成員相關
export interface Member {
  mem_id: number
  mem_avatar_path?: string
  mem_name_zh?: string
  mem_name_en?: string
  mem_desc_zh?: string
  mem_desc_en?: string
  mem_email?: string
  mem_type: number // 0:教師 1:學生 2:校友
  job_type?: number // 0:教授 1:副教授 2:講師 3:助理研究員 4:博士後
  student_type?: number // 0:博士生 1:碩士生 2:大學生
  student_grade?: number
  destination_zh?: string
  destination_en?: string
  research_group_id: number
  lab_id: number
  enable: number
  created_at?: string
  updated_at?: string
  
  // 計算屬性或前端使用的便利屬性
  id: number // 等同於 mem_id
  name: string // 基於當前語言的名稱 (mem_name_zh 或 mem_name_en)
  job_title?: string // 基於job_type或student_type的職稱
  bio?: string // 基於當前語言的描述 (mem_desc_zh 或 mem_desc_en)
  member_type: 'teacher' | 'student' | 'alumni' // 基於mem_type的字符串表示
  avatar_url?: string // 基於 mem_avatar_path 的完整URL
  grade?: string // 基於 student_grade 的字符串表示
}

// 論文相關
export interface Paper {
  paper_id: number
  research_group_id?: number
  lab_id?: number
  paper_date: string
  paper_title_zh?: string
  paper_title_en?: string
  paper_desc_zh?: string
  paper_desc_en?: string
  paper_type: number // 0:期刊論文 1:會議論文 2:學位論文 3:專題著作 4:其它
  paper_venue?: string
  paper_accept: number // 0:未接收 1:已接收
  paper_blob?: string
  paper_url?: string
  enable: number
  created_at?: string
  updated_at?: string
}

// 新聞相關
export interface News {
  news_id: number
  news_type: number // 0:論文 1:獎項 2:報告 3:其它
  news_content_zh?: string
  news_content_en?: string
  news_date?: string
  enable: number
  created_at?: string
  updated_at?: string
}

// 項目相關
export interface Project {
  project_id: number
  project_url?: string
  project_name_zh?: string
  project_name_en?: string
  project_desc_zh?: string
  project_desc_en?: string
  project_date_start?: string
  is_end: number // 0:未結項 1:已結項
  enable: number
  created_at?: string
  updated_at?: string
}

// 編輯記錄相關
export interface EditRecord {
  edit_id: number
  admin_id: number
  edit_type: string // CREATE, UPDATE, DELETE
  edit_module: number // 0:實驗室 1:課題組 2:成員 3:論文
  edit_content?: any
  edit_date: string
}

// API 響應格式
export interface ApiResponse<T> {
  code: number
  message?: string
  data: T
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  per_page: number
  totalPages: number
}