import { MockMethod } from 'vite-plugin-mock'
import Mock from 'mockjs'

// 定義 mock 請求參數類型
interface MockRequestConfig {
  body?: Record<string, any>
  query?: Record<string, any>
}

// 生成模擬用戶數據
const generateUser = () => Mock.mock({
  id: '@increment',
  username: '@name',
  email: '@email',
  role: '@pick(["admin", "user"])',
  created_at: '@datetime',
  enable: true
})

// 生成模擬實驗室數據
const generateLab = () => Mock.mock({
  id: 1,
  name: '@ctitle(5, 10)',
  description: '@cparagraph(2, 4)',
  address: '@county(true)',
  email: '@email',
  phone: /^1[3456789]\d{9}$/,
  website: '@url',
  logo_url: '/api/media/lab/logo.png',
  created_at: '@datetime',
  updated_at: '@datetime',
  enable: true
})

// 生成模擬課題組數據
const generateResearchGroup = () => Mock.mock({
  id: '@increment',
  name: '@ctitle(3, 8)',
  description: '@cparagraph(1, 3)',
  leader: '@cname',
  created_at: '@datetime',
  updated_at: '@datetime',
  enable: true
})

// 生成模擬成員數據
const generateMember = () => Mock.mock({
  id: '@increment',
  name: '@cname',
  member_type: '@pick(["teacher", "student", "alumni"])',
  'job_title|1': ['教授', '副教授', '講師', '助理研究員', '博士後'],
  'student_type|1': ['doctoral', 'master', 'undergraduate'],
  grade: '@pick(["大一", "大二", "大三", "大四", "研一", "研二", "研三", "博一", "博二", "博三", "博四"])',
  email: '@email',
  phone: /^1[3456789]\d{9}$/,
  personal_page: '@url',
  avatar_url: '/api/media/avatar/default.png',
  bio: '@cparagraph(3, 6)',
  research_group_id: '@integer(1, 5)',
  destination: '@ctitle(5, 10)',
  created_at: '@datetime',
  updated_at: '@datetime',
  enable: true
})

// 生成模擬論文數據
const generatePaper = () => Mock.mock({
  id: '@increment',
  title: '@ctitle(10, 20)',
  authors: '@cname, @cname, @cname',
  paper_type: '@pick(["journal", "conference", "thesis", "book", "other"])',
  venue: '@pick(["CVPR", "ICCV", "ECCV", "AAAI", "IJCAI", "NIPS", "ICML", "IEEE TPAMI", "Nature", "Science"])',
  year: '@integer(2018, 2024)',
  doi: '10.1000/@natural',
  url: '@url',
  status: '@pick(["accepted", "pending"])',
  abstract: '@cparagraph(3, 5)',
  created_at: '@datetime',
  updated_at: '@datetime',
  enable: true
})

// 生成模擬新聞數據
const generateNews = () => Mock.mock({
  id: '@increment',
  title: '@ctitle(5, 15)',
  content: '@cparagraph(3, 8)',
  news_type: '@pick(["paper", "award", "report", "other"])',
  author: '@cname',
  publish_date: '@date',
  image_url: '/api/media/news/default.jpg',
  created_at: '@datetime',
  updated_at: '@datetime',
  enable: true
})

// 生成模擬項目數據
const generateProject = () => Mock.mock({
  id: '@increment',
  title: '@ctitle(8, 15)',
  description: '@cparagraph(2, 4)',
  start_date: '@date',
  end_date: '@date',
  status: '@pick(["ongoing", "completed"])',
  funding: '@integer(10, 500)萬元',
  participants: '@cname, @cname, @cname',
  created_at: '@datetime',
  updated_at: '@datetime',
  enable: true
})

// 生成模擬編輯記錄數據
const generateEditRecord = () => Mock.mock({
  id: '@increment',
  admin_username: '@name',
  table_name: '@pick(["members", "papers", "news", "projects", "research_groups"])',
  record_id: '@integer(1, 100)',
  action: '@pick(["create", "update", "delete"])',
  old_data: {},
  new_data: {},
  timestamp: '@datetime'
})

export default [
  // 認證相關
  {
    url: '/api/admin/login',
    method: 'post',
    response: ({ body }: MockRequestConfig) => {
      const { admin_name, admin_pass } = body
      if (admin_name === 'admin' && admin_pass === 'admin123') {
        return {
          code: 0,
          message: 'OK',
          data: {
            access_token: 'Bearer ' + Mock.Random.string('lower', 32),
            expires_in: 3600,
            admin: {
              admin_id: 1,
              admin_name: 'admin',
              is_super: 1
            }
          }
        }
      }
      return {
        code: 1000,
        message: '用戶名或密碼錯誤'
      }
    }
  },
  {
    url: '/api/auth/login',
    method: 'post',
    response: ({ body }: MockRequestConfig) => {
      const { admin_name, admin_pass } = body
      if (admin_name === 'admin' && admin_pass === 'admin123') {
        return {
          code: 0,
          message: 'OK',
          data: {
            access_token: 'Bearer ' + Mock.Random.string('lower', 32),
            expires_in: 3600,
            admin: {
              admin_id: 1,
              admin_name: 'admin',
              is_super: 1
            }
          }
        }
      }
      return {
        code: 1000,
        message: '用戶名或密碼錯誤'
      }
    }
  },
  {
    url: '/api/auth/me',
    method: 'get',
    response: () => ({
      code: 0,
      data: generateUser()
    })
  },

  // 實驗室相關
  {
    url: '/api/lab',
    method: 'get',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generateLab()
    })
  },
  {
    url: '/api/lab',
    method: 'put',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generateLab()
    })
  },

  // 課題組相關
  {
    url: '/api/research_groups',
    method: 'get',
    response: ({ query }: MockRequestConfig) => {
      const page = Number(query.page) || 1
      const limit = Number(query.limit) || 10
      const total = 20
      
      return {
        code: 0,
        message: 'OK',
        data: {
          data: Mock.mock({
            [`items|${limit}`]: [generateResearchGroup]
          }).items,
          total,
          page,
          per_page: limit,
          totalPages: Math.ceil(total / limit)
        }
      }
    }
  },
  {
    url: /\/api\/research_groups\/\d+/,
    method: 'get',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generateResearchGroup()
    })
  },
  {
    url: '/api/research_groups',
    method: 'post',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generateResearchGroup()
    })
  },
  {
    url: /\/api\/research_groups\/\d+/,
    method: 'put',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generateResearchGroup()
    })
  },
  {
    url: /\/api\/research_groups\/\d+/,
    method: 'delete',
    response: () => ({
      code: 0,
      message: 'OK'
    })
  },

  // 成員相關
  {
    url: '/api/members',
    method: 'get',
    response: ({ query }: MockRequestConfig) => {
      const page = Number(query.page) || 1
      const limit = Number(query.limit) || 10
      const total = 50
      
      return {
        code: 0,
        message: 'OK',
        data: {
          data: Mock.mock({
            [`items|${limit}`]: [generateMember]
          }).items,
          total,
          page,
          per_page: limit,
          totalPages: Math.ceil(total / limit)
        }
      }
    }
  },
  {
    url: /\/api\/members\/\d+/,
    method: 'get',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generateMember()
    })
  },
  {
    url: '/api/members',
    method: 'post',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generateMember()
    })
  },
  {
    url: /\/api\/members\/\d+/,
    method: 'put',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generateMember()
    })
  },
  {
    url: /\/api\/members\/\d+/,
    method: 'delete',
    response: () => ({
      code: 0,
      message: 'OK'
    })
  },
  {
    url: /\/api\/members\/\d+\/avatar/,
    method: 'post',
    response: () => ({
      code: 0,
      message: 'OK',
      data: {
        avatar_url: '/api/media/avatar/uploaded.png'
      }
    })
  },

  // 論文相關
  {
    url: '/api/papers',
    method: 'get',
    response: ({ query }: MockRequestConfig) => {
      const page = Number(query.page) || 1
      const limit = Number(query.limit) || 10
      const total = 30
      
      return {
        code: 0,
        message: 'OK',
        data: {
          data: Mock.mock({
            [`items|${limit}`]: [generatePaper]
          }).items,
          total,
          page,
          per_page: limit,
          totalPages: Math.ceil(total / limit)
        }
      }
    }
  },
  {
    url: /\/api\/papers\/\d+/,
    method: 'get',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generatePaper()
    })
  },
  {
    url: '/api/papers',
    method: 'post',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generatePaper()
    })
  },
  {
    url: /\/api\/papers\/\d+/,
    method: 'put',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generatePaper()
    })
  },
  {
    url: /\/api\/papers\/\d+/,
    method: 'delete',
    response: () => ({
      code: 0,
      message: 'OK'
    })
  },

  // 新聞相關
  {
    url: '/api/news',
    method: 'get',
    response: ({ query }: MockRequestConfig) => {
      const page = Number(query.page) || 1
      const limit = Number(query.limit) || 10
      const total = 25
      
      return {
        code: 0,
        message: 'OK',
        data: {
          data: Mock.mock({
            [`items|${limit}`]: [generateNews]
          }).items,
          total,
          page,
          per_page: limit,
          totalPages: Math.ceil(total / limit)
        }
      }
    }
  },
  {
    url: /\/api\/news\/\d+/,
    method: 'get',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generateNews()
    })
  },
  {
    url: '/api/news',
    method: 'post',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generateNews()
    })
  },
  {
    url: /\/api\/news\/\d+/,
    method: 'put',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generateNews()
    })
  },
  {
    url: /\/api\/news\/\d+/,
    method: 'delete',
    response: () => ({
      code: 0,
      message: 'OK'
    })
  },
  {
    url: '/api/news/upload_image',
    method: 'post',
    response: () => ({
      code: 0,
      message: 'OK',
      data: {
        image_url: '/api/media/news/uploaded.jpg'
      }
    })
  },

  // 項目相關
  {
    url: '/api/projects',
    method: 'get',
    response: ({ query }: MockRequestConfig) => {
      const page = Number(query.page) || 1
      const limit = Number(query.limit) || 10
      const total = 15
      
      return {
        code: 0,
        message: 'OK',
        data: {
          data: Mock.mock({
            [`items|${limit}`]: [generateProject]
          }).items,
          total,
          page,
          per_page: limit,
          totalPages: Math.ceil(total / limit)
        }
      }
    }
  },
  {
    url: /\/api\/projects\/\d+/,
    method: 'get',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generateProject()
    })
  },
  {
    url: '/api/projects',
    method: 'post',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generateProject()
    })
  },
  {
    url: /\/api\/projects\/\d+/,
    method: 'put',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generateProject()
    })
  },
  {
    url: /\/api\/projects\/\d+/,
    method: 'delete',
    response: () => ({
      code: 0,
      message: 'OK'
    })
  },

  // 管理員相關
  {
    url: '/api/admins',
    method: 'get',
    response: ({ query }: MockRequestConfig) => {
      const page = Number(query.page) || 1
      const limit = Number(query.limit) || 10
      const total = 5
      
      return {
        code: 0,
        message: 'OK',
        data: {
          data: Mock.mock({
            [`items|${limit}`]: [generateUser]
          }).items,
          total,
          page,
          per_page: limit,
          totalPages: Math.ceil(total / limit)
        }
      }
    }
  },
  {
    url: '/api/admins',
    method: 'post',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generateUser()
    })
  },
  {
    url: /\/api\/admins\/\d+/,
    method: 'put',
    response: () => ({
      code: 0,
      message: 'OK',
      data: generateUser()
    })
  },
  {
    url: /\/api\/admins\/\d+/,
    method: 'delete',
    response: () => ({
      code: 0,
      message: 'OK'
    })
  },
  {
    url: '/api/auth/logout',
    method: 'post',
    response: () => ({
      code: 0,
      message: 'OK'
    })
  },

  // 編輯記錄相關
  {
    url: '/api/edit_records',
    method: 'get',
    response: ({ query }: MockRequestConfig) => {
      const page = Number(query.page) || 1
      const limit = Number(query.limit) || 10
      const total = 100
      
      return {
        code: 0,
        message: 'OK',
        data: {
          data: Mock.mock({
            [`items|${limit}`]: [generateEditRecord]
          }).items,
          total,
          page,
          per_page: limit,
          totalPages: Math.ceil(total / limit)
        }
      }
    }
  }
] as MockMethod[]