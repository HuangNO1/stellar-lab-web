// API 響應格式
export interface ApiResponse<T = any> {
  code: number;
  message: string;
  data: T;
}

// 分頁響應格式
export interface PaginatedResponse<T = any> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
  has_prev: boolean;
  has_next: boolean;
}

// 實驗室信息
export interface Lab {
  lab_id: number;
  lab_logo_path?: string;
  carousel_img_1?: string;
  carousel_img_2?: string;
  carousel_img_3?: string;
  carousel_img_4?: string;
  lab_zh: string;
  lab_en: string;
  lab_desc_zh?: string;
  lab_desc_en?: string;
  lab_address_zh?: string;
  lab_address_en?: string;
  lab_email?: string;
  lab_phone?: string;
  enable: number;
}

// 課題組負責人簡化信息
export interface Leader {
  mem_id: number;
  mem_name_zh: string;
  mem_name_en: string;
}

// 課題組信息
export interface ResearchGroup {
  research_group_id: number;
  lab_id: number;
  research_group_name_zh: string;
  research_group_name_en: string;
  research_group_desc_zh?: string;
  research_group_desc_en?: string;
  mem_id?: number;
  enable: number;
  leader?: Leader | Member; // 支持兩種類型
}

// 成員信息
export interface Member {
  mem_id: number;
  mem_avatar_path?: string;
  mem_name_zh: string;
  mem_name_en: string;
  mem_desc_zh?: string;
  mem_desc_en?: string;
  mem_email: string;
  mem_type: number; // 0=教師, 1=學生, 2=其他
  job_type?: number; // 0=教授, 1=副教授, 2=講師, 3=助理教授, 4=其他
  student_type?: number; // 0=博士, 1=碩士, 2=本科
  student_grade?: number;
  destination_zh?: string;
  destination_en?: string;
  research_group_id?: number;
  lab_id: number;
  enable: number;
  created_at: string;
}

// 論文信息
export interface Paper {
  paper_id: number;
  research_group_id?: number;
  lab_id: number;
  paper_date: string;
  paper_title_zh: string;
  paper_title_en?: string;
  paper_desc_zh?: string;
  paper_desc_en?: string;
  paper_type: number; // 0=會議, 1=期刊, 2=專利, 3=書籍, 4=其他
  paper_venue?: string;
  paper_accept: number; // 0=投稿中, 1=已接收
  paper_file_path?: string;
  paper_url?: string;
  enable: number;
  authors?: PaperAuthor[];
}

// 論文作者關聯
export interface PaperAuthor {
  paper_id: number;
  mem_id: number;
  author_order: number;
  is_corresponding: number;
  member?: Member;
}

// 新聞信息
export interface News {
  news_id: number;
  news_type: number; // 0=論文發表, 1=獲獎消息, 2=學術活動
  news_content_zh: string;
  news_content_en?: string;
  news_date: string;
  enable: number;
  created_at: string;
}

// 項目信息
export interface Project {
  project_id: number;
  project_url?: string;
  project_name_zh: string;
  project_name_en?: string;
  project_desc_zh?: string;
  project_desc_en?: string;
  project_date_start?: string;
  is_end: number; // 0=進行中, 1=已完成
  enable: number;
}

// 管理員信息
export interface Admin {
  admin_id: number;
  admin_name: string;
  is_super: number;
  enable: number;
  created_at: string;
}

// 登錄響應
export interface LoginResponse {
  access_token: string;
  expires_in: number;
  admin: Admin;
}

// 查詢參數基類
export interface BaseQueryParams {
  q?: string;
  show_all?: boolean;
  page?: number;
  per_page?: number;
}

// 課題組查詢參數
export interface ResearchGroupQueryParams extends BaseQueryParams {
  lab_id?: number;
}

// 成員查詢參數
export interface MemberQueryParams extends BaseQueryParams {
  type?: number;
  research_group_id?: number;
  lab_id?: number;
  sort_by?: string;
  order?: string;
}

// 論文查詢參數
export interface PaperQueryParams extends BaseQueryParams {
  paper_type?: number;
  paper_accept?: number;
  start_date?: string;
  end_date?: string;
  sort_by?: string;
  order?: string;
}

// 新聞查詢參數
export interface NewsQueryParams extends BaseQueryParams {
  news_type?: number;
  start_date?: string;
  end_date?: string;
}

// 項目查詢參數
export interface ProjectQueryParams extends BaseQueryParams {
  is_end?: number;
  start_date?: string;
  end_date?: string;
  sort_by?: string;
  order?: string;
}