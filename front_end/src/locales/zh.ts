export default {
  nav: {
    home: '首頁',
    members: '成員',
    research: '研究',
    projects: '項目',
    papers: '論文',
    news: '新聞',
    about: '關於'
  },
  common: {
    language: '語言',
    theme: '主題',
    light: '明亮模式',
    dark: '暗黑模式',
    loading: '載入中...',
    error: '錯誤',
    success: '成功',
    confirm: '確認',
    cancel: '取消',
    contact: '聯繫我們',
    retry: '重試',
    viewDetails: '查看詳情',
    fetchError: '獲取數據失敗',
    goBack: '返回'
  },
  defaults: {
    labName: '實驗室',
    labDescription: '本實驗室專注於前沿科技研究',
    labFallbackName: '智慧實驗室',
    carousel: {
      alt1: '實驗室輪播圖1',
      alt2: '實驗室輪播圖2', 
      alt3: '實驗室輪播圖3',
      alt4: '實驗室輪播圖4',
      defaultAlt1: '默認輪播圖1',
      defaultAlt2: '默認輪播圖2'
    }
  },
  home: {
    title: '歡迎來到實驗室',
    subtitle: '探索科學，創造未來',
    description: '我們是一個專注於前沿科技研究的實驗室'
  },
  members: {
    title: '團隊成員',
    professor: '教授',
    postdoc: '博士後',
    phd: '博士生',
    master: '碩士生',
    undergraduate: '本科生',
    alumni: '校友',
    others: '其他成員',
    description: '個人簡介',
    relatedPapers: '相關論文'
  },
  research: {
    title: '研究領域',
    projects_title: '研究項目',
    papers_title: '學術論文',
    ongoing: '進行中',
    completed: '已完成'
  },
  news: {
    title: '實驗室新聞',
    latest: '最新消息',
    date: '日期',
    description: '查看實驗室最新動態',
    type: '類型',
    empty: '暫無新聞數據',
    paperPublished: '論文發表',
    award: '獲獎消息',
    academic: '學術活動',
    other: '其他'
  },
  about: {
    title: '關於我們',
    mission: '使命',
    vision: '願景',
    contact: '聯繫我們'
  },
  researchGroups: {
    title: '研究課題組',
    viewDetails: '查看詳情',
    leader: '課題組負責人',
    members: '成員數量',
    projects: '項目數量'
  },
  papers: {
    title: '論文成果',
    accepted: '已接收',
    submitted: '投稿中',
    description: '查看實驗室發表的學術論文',
    type: '論文類型',
    status: '狀態',
    viewOnline: '在線查看',
    download: '下載',
    empty: '暫無論文數據',
    conference: '會議論文',
    journal: '期刊論文',
    patent: '專利',
    book: '書籍',
    other: '其他',
    date: '發表日期',
    venue: '發表期刊/會議'
  },
  groups: {
    title: '研究課題組',
    leader: '課題組負責人',
    description: '課題組簡介',
    members: '成員列表'
  },
  projects: {
    title: '研究項目',
    description: '查看實驗室的研究項目',
    status: '狀態',
    startDate: '開始日期',
    viewRepository: '查看代碼庫',
    empty: '暫無項目數據',
    ongoing: '進行中',
    completed: '已完成',
    name: '項目名稱'
  },
  search: {
    placeholder: '搜索...',
    advanced: '高級搜索',
    dateRange: '日期範圍',
    startDate: '開始日期',
    endDate: '結束日期',
    all: '全部',
    sortBy: '排序方式',
    default: '默認',
    desc: '降序',
    asc: '升序',
    search: '搜索'
  },
  emptyStates: {
    noMembers: '暫無成員數據',
    noGroupMembers: '該課題組暫無成員',
    groupNotFound: '未找到該課題組',
    memberNotFound: '未找到該成員'
  },
  errorMessages: {
    fetchGroupDetail: '獲取課題組詳情失敗',
    fetchMemberDetail: '獲取成員詳情失敗'
  },
  language: {
    chinese: '中文',
    english: 'English'
  },
  admin: {
    layout: {
      title: '管理後台',
      dashboard: '儀表板',
      languageChanged: '語言已切換'
    },
    menu: {
      dashboard: '儀表板',
      content: '內容管理',
      members: '成員管理',
      groups: '課題組管理',
      papers: '論文管理',
      projects: '項目管理',
      news: '新聞管理',
      lab: '實驗室管理',
      system: '系統管理'
    },
    login: {
      title: '管理員登錄',
      subtitle: '歡迎回到實驗室管理系統',
      usernamePlaceholder: '請輸入管理員用戶名',
      passwordPlaceholder: '請輸入管理員密碼',
      loginButton: '登錄',
      footer: '實驗室管理系統 v1.0',
      usernameRequired: '請輸入用戶名',
      passwordRequired: '請輸入密碼',
      loginSuccess: '登錄成功',
      loginFailed: '登錄失敗'
    },
    user: {
      profile: '個人資料',
      changePassword: '修改密碼',
      logout: '退出登錄',
      logoutSuccess: '已安全退出'
    },
    dashboard: {
      totalMembers: '總成員數',
      totalPapers: '總論文數',
      totalProjects: '總項目數',
      totalNews: '總新聞數',
      quickActions: '快速操作',
      addMember: '添加成員',
      addPaper: '添加論文',
      addProject: '添加項目',
      addNews: '添加新聞',
      systemStatus: '系統狀態',
      apiStatus: 'API服務',
      databaseStatus: '數據庫',
      mediaStatus: '媒體服務',
      online: '在線',
      normal: '正常',
      recentActivities: '最近活動',
      noActivities: '暫無活動記錄',
      todoList: '待辦事項',
      reviewPapers: '審核新提交的論文',
      updateLabInfo: '更新實驗室基本信息',
      checkNews: '檢查新聞內容'
    },
    common: {
      enabled: '啟用',
      disabled: '禁用',
      edit: '編輯',
      delete: '刪除',
      confirmDelete: '確認刪除',
      actions: '操作',
      comingSoon: '功能開發中',
      comingSoonDesc: '此功能正在開發中，敬請期待！'
    },
    members: {
      addMember: '添加成員',
      editMember: '編輯成員',
      searchPlaceholder: '搜索成員姓名或郵箱...',
      filterByType: '按類型篩選',
      filterByGroup: '按課題組篩選',
      avatar: '頭像',
      name: '姓名',
      email: '郵箱',
      type: '類型',
      group: '課題組',
      status: '狀態',
      fetchError: '獲取成員列表失敗',
      deleteConfirmText: '確定要刪除這個成員嗎？此操作不可撤銷。',
      deleteSuccess: '成員刪除成功',
      deleteError: '刪除成員失敗'
    },
    groups: {
      addGroup: '添加課題組',
      editGroup: '編輯課題組'
    },
    papers: {
      addPaper: '添加論文',
      editPaper: '編輯論文'
    },
    projects: {
      addProject: '添加項目',
      editProject: '編輯項目'
    },
    news: {
      addNews: '添加新聞',
      editNews: '編輯新聞'
    }
  }
}