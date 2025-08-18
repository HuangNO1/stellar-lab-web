export default {
    nav: {
        home: '首页',
        members: '成员',
        research: '研究',
        projects: '项目',
        papers: '论文',
        resources: '资源',
        news: '新闻',
        about: '关于',
        menu: '导航菜单'
    },
    common: {
        language: '语言',
        theme: '主题',
        light: '明亮模式',
        dark: '暗黑模式',
        loading: '载入中...',
        error: '错误',
        success: '成功',
        confirm: '确认',
        cancel: '取消',
        contact: '联系我们',
        retry: '重试',
        viewDetails: '查看详情',
        fetchError: '获取数据失败',
        goBack: '返回',
        back: '返回',
        page: '页',
        noData: '暂无数据',
        itemsPerPage: '每页条数'
    },
    auth: {
        loginFailed: '登录失败',
        loginNetworkError: '登录失败，请检查网络连接',
        logoutFailed: '登出请求失败',
        updateProfileFailed: '更新个人资讯失败',
        updateFailed: '更新失败，请重试',
        changePasswordFailed: '修改密码失败',
        changePasswordSuccess: '密码修改成功',
        changeFailed: '修改失败，请重试'
    },
    defaults: {
        labName: '实验室',
        labDescription: '本实验室专注于前沿科技研究',
        labFallbackName: '智慧实验室',
        carousel: {
            alt1: '实验室轮播图1',
            alt2: '实验室轮播图2',
            alt3: '实验室轮播图3',
            alt4: '实验室轮播图4',
            defaultAlt1: '默认轮播图1',
            defaultAlt2: '默认轮播图2'
        }
    },
    home: {
        title: '欢迎来到实验室',
        subtitle: '探索科学，创造未来',
        description: '我们是一个专注于前沿科技研究的实验室'
    },
    members: {
        title: '团队成员',
        description: '认识我们的研究团队成员',
        teachers: '教师',
        professor: '教授',
        postdoc: '博士后',
        phd: '博士生',
        master: '硕士生',
        undergraduate: '本科生',
        alumni: '校友',
        others: '其他成员',
        profile: '个人简介',
        relatedPapers: '相关论文',
        positions: {
            professor: '教授',
            associateProfessor: '副教授',
            lecturer: '讲师',
            assistantProfessor: '助理教授',
            postdoc: '博士后',
            phdStudent: '博士生',
            masterStudent: '硕士生',
            undergraduate: '本科生',
            alumni: '校友',
            other: '其他',
            year: '年级',
            // 校友身份类型
            phdGraduate: '博士毕业生',
            masterGraduate: '硕士毕业生',
            undergraduateGraduate: '本科毕业生',
            faculty: '教职员工',
            graduateYear: '年毕业',
            graduate: '毕业'
        },
        // 研究领域相关
        researchAreas: '研究領域'
    },
    research: {
        title: '研究领域',
        projects_title: '研究项目',
        papers_title: '学术论文',
        ongoing: '进行中',
        completed: '已完成'
    },
    news: {
        title: '实验室新闻',
        latest: '最新消息',
        date: '日期',
        description: '查看实验室最新动态',
        type: '类型',
        empty: '暂无新闻数据',
        paperPublished: '论文发表',
        award: '获奖消息',
        academic: '学术活动',
        other: '其他',
        viewMore: '查看更多',
        notFound: '未找到该新闻',
        invalidId: '无效的新闻ID',
        fetchError: '获取新闻详情失败',
        noContent: '无内容',
        noContentTitle: '新闻内容为空',
        noContentMessage: '这条新闻暂时没有可显示的内容。',
        types: {
            publication: '论文发表',
            award: '获奖消息',
            activity: '学术活动'
        }
    },
    about: {
        title: '关于我们',
        mission: '使命',
        vision: '愿景',
        contact: '联系我们'
    },
    researchGroups: {
        title: '研究课题组',
        viewDetails: '查看详情',
        leader: '课题组负责人',
        members: '成员数量',
        projects: '项目数量'
    },
    papers: {
        title: '论文成果',
        accepted: '已接收',
        submitted: '投稿中',
        description: '查看实验室发表的学术论文',
        searchPlaceholder: '搜索论文...',
        filterByType: '按类型筛选',
        filterByStatus: '按状态筛选',
        type: '论文类型',
        status: '状态',
        viewOnline: '在线查看',
        download: '下载',
        empty: '暂无论文数据',
        conference: '会议论文',
        journal: '期刊论文',
        patent: '专利',
        book: '书籍',
        other: '其他',
        date: '发表日期',
        venue: '发表期刊/会议',
        andOthers: '等',
        authors: '作者',
        allAuthors: '全部作者',
        noPreview: '无预览图片',
        abstract: '摘要',
        correspondingAuthor: '通讯作者',
        notFound: '未找到该论文',
        invalidId: '无效的论文ID',
        fetchError: '获取论文详情失败',
        types: {
            conference: '会议论文',
            journal: '期刊论文',
            patent: '专利',
            book: '书籍',
            other: '其他'
        }
    },
    projects: {
        title: '研究项目',
        description: '查看实验室的研究项目',
        status: '状态',
        startDate: '开始日期',
        viewRepository: '查看代码库',
        empty: '暂无项目数据',
        ongoing: '进行中',
        completed: '已完成',
        name: '项目名称',
        notFound: '未找到该项目',
        invalidId: '无效的项目ID',
        fetchError: '获取项目详情失败'
    },
    resources: {
        title: '实验室资源',
        description: '管理实验室设备、软件和数据库资源',
        name: '资源名称',
        resourceType: '资源类型',
        availabilityStatus: '可用状态',
        location: '位置',
        contact: '联系方式',
        url: '访问链接',
        empty: '暂无资源数据',
        notFound: '未找到该资源',
        fetchError: '获取资源详情失败',
        types: {
            equipment: '设备',
            software: '软件',
            database: '数据库',
            dataset: '数据集',
            other: '其他'
        },
        status: {
            unavailable: '不可用',
            available: '可用',
            maintenance: '维护中'
        }
    },
    groups: {
        title: '研究课题组',
        leader: '课题组负责人',
        description: '课题组简介',
        members: '成员列表'
    },
    search: {
        placeholder: '搜索...',
        advanced: '高级搜索',
        dateRange: '日期范围',
        startDate: '开始日期',
        endDate: '结束日期',
        all: '全部',
        sortBy: '排序方式',
        default: '默认',
        desc: '降序',
        asc: '升序',
        search: '搜索'
    },
    emptyStates: {
        noMembers: '暂无成员数据',
        noGroupMembers: '该课题组暂无成员',
        groupNotFound: '未找到该课题组',
        memberNotFound: '未找到该成员'
    },
    errorMessages: {
        fetchGroupDetail: '获取课题组详情失败',
        fetchMemberDetail: '获取成员详情失败',
        invalidMemberId: '无效的成员ID',
        invalidGroupId: '无效的课题组ID',
        networkError: '网络连接错误'
    },
    language: {
        chinese: '中文',
        english: 'English'
    },
    admin: {
        layout: {
            title: '管理后台',
            dashboard: '仪表板',
            languageChanged: '语言已切换'
        },
        menu: {
            dashboard: '仪表板',
            content: '内容管理',
            members: '成员管理',
            groups: '课题组管理',
            papers: '论文管理',
            projects: '项目管理',
            news: '新闻管理',
            resources: '资源管理',
            lab: '实验室管理',
            admins: '管理员管理',
            system: '系统管理'
        },
        login: {
            title: '管理员登录',
            subtitle: '欢迎回到实验室管理系统',
            usernamePlaceholder: '请输入管理员用户名',
            passwordPlaceholder: '请输入管理员密码',
            loginButton: '登录',
            footer: '实验室管理系统 v1.0',
            usernameRequired: '请输入用户名',
            passwordRequired: '请输入密码',
            loginSuccess: '登录成功',
            loginFailed: '登录失败'
        },
        user: {
            profile: '个人资料',
            changePassword: '修改密码',
            logout: '退出登录',
            logoutSuccess: '已安全退出'
        },
        dashboard: {
            totalMembers: '总成员数',
            totalPapers: '总论文数',
            totalProjects: '总项目数',
            totalNews: '总新闻数',
            totalResources: '总资源数',
            totalGroups: '总课题组数',
            quickActions: '快速操作',
            addMember: '添加成员',
            addPaper: '添加论文',
            addProject: '添加项目',
            addNews: '添加新闻',
            addResource: '添加资源',
            systemStatus: '系统状态',
            apiStatus: 'API服务',
            databaseStatus: '数据库',
            mediaStatus: '媒体服务',
            online: '在线',
            offline: '离线',
            normal: '正常',
            error: '异常',
            unknown: '未知',
            checking: '检查中...',
            recentActivities: '最近活动',
            noActivities: '暂无活动记录',
            todoList: '待办事项',
            reviewPapers: '审核新提交的论文',
            updateLabInfo: '更新实验室基本信息',
            checkNews: '检查新闻内容'
        },
        common: {
            enabled: '启用',
            disabled: '禁用',
            edit: '编辑',
            delete: '删除',
            confirmDelete: '确认删除',
            actions: '操作',
            comingSoon: '功能开发中',
            comingSoonDesc: '此功能正在开发中，敬请期待！',
            create: '创建',
            update: '更新',
            cancel: '取消',
            submit: '提交',
            loading: '载入中...',
            success: '成功',
            failed: '失败',
            batchEdit: '批量编辑',
            batchDelete: '批量删除',
            noPermission: '无权限',
            status: '状态',
            // 表单选项
            memberTypes: {
                teacher: '教师',
                student: '学生',
                alumni: '校友'
            },
            jobTypes: {
                professor: '教授',
                associateProfessor: '副教授',
                lecturer: '讲师',
                assistantResearcher: '助理研究员',
                postdoc: '博士后'
            },
            studentTypes: {
                phd: '博士生',
                master: '硕士生',
                undergraduate: '本科生'
            },
            alumniIdentity: {
                phd: '博士毕业生',
                master: '硕士毕业生',
                undergraduate: '本科毕业生',
                teacher: '教职员工',
                other: '其他'
            },
            paperTypes: {
                conference: '会议',
                journal: '期刊',
                patent: '专利',
                book: '书籍',
                other: '其他'
            },
            paperStatus: {
                submitting: '投稿中',
                accepted: '已接收'
            },
            projectStatus: {
                ongoing: '进行中',
                completed: '已完成'
            },
            newsTypes: {
                publication: '论文发表',
                award: '获奖消息',
                activity: '学术活动'
            },
            resourceTypes: {
                equipment: '设备',
                software: '软件',
                database: '数据库',
                dataset: '数据集',
                other: '其他'
            },
            resourceStatus: {
                unavailable: '不可用',
                available: '可用',
                maintenance: '维护中'
            },
            validationMessages: {
                required: '此栏位为必填项',
                invalidEmail: '请输入有效的电子信箱',
                invalidUrl: '请输入有效的URL'
            },
            fileUpload: {
                selectImage: '选择图片',
                selectPdf: '选择 PDF 文件',
                selectFile: '选择文件',
                uploadSuccess: '文件上传成功',
                uploadError: '文件上传失败'
            },
            viewDetails: '查看详情',
            avatarPreview: '头像预览'
        },
        members: {
            addMember: '添加成员',
            editMember: '编辑成员',
            searchPlaceholder: '搜索成员姓名或邮箱...',
            filterByType: '按类型筛选',
            filterByGroup: '按课题组筛选',
            avatar: '头像',
            name: '姓名',
            email: '邮箱',
            type: '类型',
            group: '课题组',
            status: '状态',
            details: '详情',
            studentGrade: '年级',
            jobType: '职位',
            studentType: '学位类型',
            grade: '年级',
            fetchError: '获取成员列表失败',
            deleteConfirmText: '确定要删除这个成员吗？此操作不可撤销。',
            deleteSuccess: '成员删除成功',
            deleteError: '删除成员失败',
            batchEdit: '批量编辑',
            batchEditTip: '将对选中的 {count} 位成员进行批量修改',
            batchDeleteConfirmText: '确定要删除选中的 {count} 位成员吗？此操作不可撤销。',
            batchDeleteWarning: '批量删除操作将无法恢复，请谨慎操作！',
            batchDeleteSuccess: '成功删除 {count} 位成员',
            batchUpdateSuccess: '成功更新 {count} 位成员',
            updateError: '更新成员失败',
            noUpdatesSelected: '请至少选择一个要更新的字段',
            jobTypes: {
                professor: '教授',
                assocProfessor: '副教授',
                lecturer: '讲师',
                assistantProfessor: '助理教授',
                postdoc: '博士后'
            },
            studentTypes: {
                phd: '博士',
                master: '硕士',
                undergraduate: '本科'
            },
            placeholders: {
                studentGrade: '请输入年级 (1-6)',
                jobType: '请选择职位类型',
                studentType: '请选择学位类型',
                status: '请选择状态'
            },
            // QuickActionModal 相关
            form: {
                nameZh: '中文姓名',
                nameEn: '英文姓名',
                email: '电子信箱',
                type: '成员类型',
                jobType: '职务类型',
                studentType: '学生类型',
                studentGrade: '年级',
                graduationYear: '毕业年份',
                alumniIdentity: '校友身份',
                destinationZh: '去向（中文）',
                destinationEn: '去向（英文）',
                group: {
                    label: '课题组',
                    none: '无'
                },
                description: '成员描述（中文）',
                descriptionEn: '成员描述（英文）',
                avatar: '头像上传',
                descriptionTemplate: `## 個人簡介

[在此處介紹您的研究背景和學術經歷]

## 研究領域

@{research: 機器學習, 深度學習, 計算機視覺, 自然語言處理}

## 個人主頁

@{github: https://github.com/your-username}
@{scholar: https://scholar.google.com/citations?user=YOUR_ID}
@{linkedin: https://linkedin.com/in/your-profile}
@{researchgate: https://researchgate.net/profile/your-profile}
@{website: https://your-personal-website.com}

## 教育背景

- **年份-年份**: 學位, 學校/機構名稱
- **年份-年份**: 學位, 學校/機構名稱

## 代表性成果

### 實驗室論文
@{papers: 1,2,3}

### 其他論文發表
- [論文標題], [期刊/會議名稱], [發表年份]
- [論文標題], [期刊/會議名稱], [發表年份]

### 項目經歷
- **項目名稱**: [項目描述] ([起始年份-結束年份])

---

### 📝 Markdown 語法說明：

**🏷️ 研究領域標籤**：
\`@{research: 領域1, 領域2, 領域3}\`
- 自動循環顯示不同顏色（藍色、資訊藍、綠色、橙色、紅色）
- 支持自定義顏色：\`@{research: 機器學習#3b82f6, 深度學習#8b5cf6, 計算機視覺#10b981}\`
- 自定義顏色格式：領域名#六位HEX顏色碼（如 #ff0000 代表紅色）
- 支持容器背景色：\`@{research: 機器學習, 深度學習[bg:#f0f9ff]}\`
- 背景色格式：在標籤組最後添加 [bg:#六位HEX顏色碼]

**🔗 個人主頁連結**：
- \`@{github: https://github.com/username}\` - GitHub 頁面（灰色）
- \`@{scholar: https://scholar.google.com/citations?user=ID}\` - Google Scholar（藍色）
- \`@{linkedin: https://linkedin.com/in/profile}\` - LinkedIn（藍色）
- \`@{researchgate: https://researchgate.net/profile/name}\` - ResearchGate（綠色）
- \`@{website: https://your-site.com}\` - 個人網站（主色調）
- \`@{任意標籤名: https://連結地址}\` - 通用連結（如 \`@{個人博客: https://blog.example.com}\`）

**📚 論文列表**：
\`@{papers: 1,2,3}\`
- 填入實驗室論文的ID編號（以逗號分隔）

## 榮譽獎項

- [獎項名稱], [頒發機構], [獲獎年份]

## 聯繫方式

- **郵箱**: [您的郵箱]`,
                descriptionTemplateEn: `## Profile

[Introduce your research background and academic experience here]

## Research Areas

@{research: Machine Learning, Deep Learning, Computer Vision, Natural Language Processing}

## Homepage

@{homepage: https://scholar.google.com/citations?user=YOUR_ID}
@{homepage: https://github.com/your-username}
@{homepage: https://your-personal-website.com}

## Education

- **Year-Year**: Degree, Institution Name
- **Year-Year**: Degree, Institution Name

## Representative Achievements

### Lab Publications
@{papers: 1,2,3}

### Other Publications
- [Paper Title], [Journal/Conference Name], [Publication Year]
- [Paper Title], [Journal/Conference Name], [Publication Year]

### Project Experience
- **Project Name**: [Project Description] ([Start Year-End Year])

## Honors & Awards

- [Award Name], [Awarding Institution], [Year]

## Contact

- **Email**: [Your Email]`,
                placeholders: {
                    nameZh: '请输入中文姓名',
                    nameEn: '请输入英文姓名',
                    email: '请输入电子信箱',
                    type: '请选择成员类型',
                    jobType: '请选择职务类型',
                    studentType: '请选择学生类型',
                    studentGrade: '请输入年级（1-10）',
                    graduationYear: '请输入毕业年份',
                    alumniIdentity: '请选择校友身份',
                    destinationZh: '请输入去向（中文）',
                    destinationEn: '请输入去向（英文）',
                    group: '请选择课题组',
                    description: '请输入成员中文描述（支持 Markdown 语法）',
                    descriptionEn: '请输入成员英文描述（支持 Markdown 语法）'
                },
                validation: {
                    nameZhRequired: '请输入中文姓名',
                    nameEnRequired: '请输入英文姓名',
                    emailRequired: '请输入电子信箱',
                    typeRequired: '请选择成员类型',
                    groupRequired: '请选择课题组',
                    jobTypeRequired: '请选择职务类型',
                    studentTypeRequired: '请选择学生类型',
                    studentGradeRequired: '请输入有效年级（1-10）'
                }
            }
        },
        papers: {
            addPaper: '添加论文',
            editPaper: '编辑论文',
            searchPlaceholder: '搜索论文标题...',
            filterByType: '按类型筛选',
            filterByStatus: '按状态筛选',
            fetchError: '获取论文列表失败',
            deleteConfirmText: '确定要删除这篇论文吗？此操作不可撤销。',
            deleteSuccess: '论文删除成功',
            deleteError: '删除论文失败',
            form: {
                titleZh: '中文标题',
                titleEn: '英文标题',
                description: '论文描述（中文）',
                descriptionEn: '论文描述（英文）',
                venue: '期刊/会议',
                type: '论文类型',
                date: '发表日期',
                status: '接收状态',
                url: '论文连结',
                file: '论文文件',
                previewImg: '预览图片',
                previewImgAlt: '论文预览图片',
                authors: '作者',
                labAuthors: '實驗室作者',
                allAuthors: '全部作者',
                allAuthorsZh: '全部作者（中文）',
                allAuthorsEn: '全部作者（英文）',
                placeholders: {
                    titleZh: '请输入论文中文标题',
                    titleEn: '请输入论文英文标题',
                    description: '请输入论文中文描述（支持 Markdown 语法）',
                    descriptionEn: '请输入论文英文描述（支持 Markdown 语法）',
                    venue: '请输入发表期刊或会议',
                    type: '请选择论文类型',
                    date: '请选择发表日期',
                    status: '请选择接收状态',
                    url: '请输入论文连结URL',
                    authors: '请选择论文作者',
                    allAuthorsZh: '请输入全部作者中文名称（例如：张三, 李四, 王五）',
                    allAuthorsEn: '请输入全部作者英文名称（例如：John Smith, Jane Doe）'
                },
                validation: {
                    titleZhRequired: '请输入中文标题',
                    typeRequired: '请选择论文类型',
                    statusRequired: '请选择接收状态',
                    dateRequired: '请选择发表日期'
                }
            }
        },
        projects: {
            addProject: '添加项目',
            editProject: '编辑项目',
            searchPlaceholder: '搜索项目名称...',
            filterByStatus: '按状态筛选',
            fetchError: '获取项目列表失败',
            deleteConfirmText: '确定要删除这个项目吗？此操作不可撤销。',
            deleteSuccess: '项目删除成功',
            deleteError: '删除项目失败',
            form: {
                nameZh: '中文名称',
                nameEn: '英文名称',
                description: '项目描述（中文）',
                descriptionEn: '项目描述（英文）',
                url: '项目URL',
                startDate: '开始日期',
                status: '项目状态',
                placeholders: {
                    nameZh: '请输入项目中文名称',
                    nameEn: '请输入项目英文名称',
                    description: '请输入项目描述（支持 Markdown 语法）',
                    descriptionEn: '请输入项目英文描述（支持 Markdown 语法）',
                    url: '请输入项目URL',
                    startDate: '请选择开始日期',
                    status: '请选择项目状态'
                },
                validation: {
                    nameZhRequired: '请输入项目中文名称'
                }
            }
        },
        resources: {
            addResource: '添加资源',
            editResource: '编辑资源',
            searchPlaceholder: '搜索资源名称...',
            filterByType: '按类型筛选',
            filterByStatus: '按状态筛选',
            fetchError: '获取资源列表失败',
            deleteConfirmText: '确定要删除这个资源吗？此操作不可撤销。',
            deleteSuccess: '资源删除成功',
            deleteError: '删除资源失败',
            form: {
                nameZh: '中文名称',
                nameEn: '英文名称',
                descriptionZh: '中文描述',
                descriptionEn: '英文描述',
                type: '资源类型',
                locationZh: '中文位置',
                locationEn: '英文位置',
                url: '资源链接',
                file: '资源文件',
                image: '资源图片',
                imageAlt: '资源图片预览',
                availabilityStatus: '可用状态',
                contactInfo: '联系方式',
                placeholders: {
                    nameZh: '请输入资源中文名称',
                    nameEn: '请输入资源英文名称',
                    descriptionZh: '请输入资源中文描述',
                    descriptionEn: '请输入资源英文描述',
                    type: '请选择资源类型',
                    locationZh: '请输入中文位置',
                    locationEn: '请输入英文位置',
                    url: '请输入资源链接',
                    availabilityStatus: '请选择可用状态',
                    contactInfo: '请输入联系方式'
                },
                validation: {
                    nameZhRequired: '请输入中文名称',
                    typeRequired: '请选择资源类型',
                    availabilityStatusRequired: '请选择可用状态'
                }
            }
        },
        news: {
            addNews: '添加新闻',
            editNews: '编辑新闻',
            searchPlaceholder: '搜索新闻内容...',
            filterByType: '按类型筛选',
            fetchError: '获取新闻列表失败',
            deleteConfirmText: '确定要删除这条新闻吗？此操作不可撤销。',
            deleteSuccess: '新闻删除成功',
            deleteError: '删除新闻失败',
            form: {
                type: '新闻类型',
                titleZh: '中文标题',
                titleEn: '英文标题',
                contentZh: '中文内容',
                contentEn: '英文内容',
                date: '新闻日期',
                placeholders: {
                    type: '请选择新闻类型',
                    titleZh: '请输入新闻中文标题',
                    titleEn: '请输入新闻英文标题',
                    contentZh: '请输入新闻中文内容（支持 Markdown 语法）',
                    contentEn: '请输入新闻英文内容（支持 Markdown 语法）',
                    date: '请选择新闻日期'
                },
                validation: {
                    typeRequired: '请选择新闻类型',
                    titleRequired: '请至少输入中文或英文标题之一',
                    dateRequired: '请选择新闻日期'
                }
            }
        },
        groups: {
            title: '研究课题组',
            leader: '课题组负责人',
            description: '课题组简介',
            members: '成员列表',
            addGroup: '添加课题组',
            editGroup: '编辑课题组',
            searchPlaceholder: '搜索课题组名称...',
            fetchError: '获取课题组列表失败',
            deleteConfirmText: '确定要删除这个课题组吗？此操作不可撤销。',
            deleteSuccess: '课题组删除成功',
            deleteError: '删除课题组失败',
            form: {
                nameZh: '中文名称',
                nameEn: '英文名称',
                descriptionZh: '中文描述',
                descriptionEn: '英文描述',
                leader: '组长',
                placeholders: {
                    nameZh: '请输入课题组中文名称',
                    nameEn: '请输入课题组英文名称',
                    descriptionZh: '请输入课题组中文描述（支持 Markdown 语法）',
                    descriptionEn: '请输入课题组英文描述（支持 Markdown 语法）',
                    leader: '请选择组长'
                },
                validation: {
                    nameZhRequired: '请输入课题组中文名称'
                }
            }
        },
        // MarkdownEditor 翻译
        markdownEditor: {
            preview: '预览',
            edit: '编辑',
            tip: '支持 Markdown 语法：**粗体**, *斜体*, ### 标题, - 列表, [链接](url)',
            placeholder: '请输入内容...',
            toolbar: {
                bold: '粗体',
                italic: '斜体',
                heading: '标题',
                list: '列表',
                link: '链接'
            },
            imageUpload: {
                selectFile: '选择图片文件',
                invalidFileType: '请选择图片文件',
                fileSizeExceeded: '图片大小不能超过 5MB',
                uploadSuccess: '成功上传 {count} 张图片',
                uploadFailed: '图片上传失败',
                uploading: '正在上传图片...'
            }
        },
        // QuickActionModal 翻译
        quickAction: {
            modalTitle: {
                createMember: '新增成员',
                editMember: '编辑成员',
                createPaper: '新增论文',
                editPaper: '编辑论文',
                createProject: '新增项目',
                editProject: '编辑项目',
                createNews: '新增新闻',
                editNews: '编辑新闻',
                createGroup: '新增课题组',
                editGroup: '编辑课题组',
                createAdmin: '新增管理员',
                editAdmin: '编辑管理员',
                createResource: '新增资源',
                editResource: '编辑资源'
            },
            messages: {
                createSuccess: '创建成功',
                updateSuccess: '更新成功',
                operationFailed: '操作失败',
                checkInput: '操作失败，请检查输入',
                loadGroupsFailed: '载入课题组失败',
                loadMembersFailed: '载入成员失败'
            },
            timeFormat: {
                daysAgo: '天前',
                hoursAgo: '小时前',
                minutesAgo: '分钟前',
                justNow: '刚刚',
                yearsAgo: '年前',
                monthsAgo: '个月前',
                shortMinutesAgo: '分前',
                now: '刚才'
            },
            activities: {
                created: '新增了',
                updated: '编辑了',
                moduleNames: {
                    members: '成员',
                    papers: '论文',
                    projects: '项目',
                    news: '新闻',
                    groups: '课题组',
                    resources: '资源'
                }
            }
        },
        // 实验室管理翻译
        lab: {
            basicInfo: '基本信息',
            contactInfo: '联系信息',
            imageManagement: '图片管理',
            nameZh: '实验室中文名称',
            nameEn: '实验室英文名称',
            descZh: '中文描述',
            descEn: '英文描述',
            addressZh: '中文地址',
            addressEn: '英文地址',
            email: '联系邮箱',
            phone: '联系电话',
            logo: '实验室Logo',
            carouselImages: '轮播图片',
            carouselImage: '轮播图片 {number}',
            placeholders: {
                nameZh: '请输入实验室中文名称',
                nameEn: '请输入实验室英文名称',
                descZh: '请输入实验室中文描述',
                descEn: '请输入实验室英文描述',
                addressZh: '请输入实验室中文地址',
                addressEn: '请输入实验室英文地址',
                email: '请输入联系邮箱',
                phone: '请输入联系电话'
            },
            validation: {
                nameZhRequired: '实验室中文名称必填',
                nameEnRequired: '实验室英文名称必填'
            },
            messages: {
                fetchFailed: '获取实验室信息失败',
                saveSuccess: '保存成功',
                saveFailed: '保存失败'
            },
            logoPreview: 'Logo 预览',
            carouselPreview: '轮播图 {number} 预览'
        },
        // 管理员管理翻译
        admins: {
            addAdmin: '添加管理员',
            editAdmin: '编辑管理员',
            resetPassword: '重置密码',
            searchPlaceholder: '搜索管理员用户名...',
            adminName: '用户名',
            adminType: '类型',
            superAdmin: '超级管理员',
            normalAdmin: '普通管理员',
            createdAt: '创建时间',
            fetchError: '获取管理员列表失败',
            deleteConfirmText: '确定要删除这个管理员吗？此操作不可撤销。',
            deleteSuccess: '管理员删除成功',
            deleteError: '删除管理员失败',
            noEditPermission: '无权限编辑此管理员',
            noDeletePermission: '无权限删除此管理员',
            noResetPasswordPermission: '无权限重置此管理员密码',
            noCreatePermission: '无权限创建管理员',
            cannotEditSelf: '不能编辑自己的账号',
            cannotEditSuperAdmin: '不能编辑超级管理员',
            messages: {
                passwordResetSuccess: '密码重置成功',
                passwordResetFailed: '密码重置失败'
            },
            form: {
                adminName: '用户名',
                adminPass: '密码',
                newPassword: '新密码',
                confirmPassword: '确认密码',
                isSuper: '管理员类型',
                enable: '状态',
                placeholders: {
                    adminName: '请输入用户名',
                    adminPass: '请输入密码',
                    newPassword: '请输入新密码（至少8位字符）',
                    confirmPassword: '请确认新密码',
                    isSuper: '请选择管理员类型',
                    enable: '请选择状态'
                },
                validation: {
                    adminNameRequired: '用户名必填',
                    adminPassRequired: '密码必填',
                    newPasswordRequired: '新密码必填',
                    confirmPasswordRequired: '确认密码必填'
                }
            }
        },
        // 操作日志翻译
        operationLogs: {
            title: '操作日志',
            description: '查看所有管理员操作和系统活动记录',
            searchPlaceholder: '搜索管理员姓名、操作类型或内容...',
            selectAdmin: '选择管理员',
            selectOperation: '选择操作类型',
            selectModule: '选择模块',
            allAdmins: '全部管理员',
            allOperations: '全部操作',
            allModules: '全部模块',
            time: '操作时间',
            admin: '操作管理员',
            operation: '操作类型',
            module: '操作模块',
            content: '操作内容',
            create: '创建',
            update: '更新',
            delete: '删除',
            login: '登录',
            logout: '登出',
            changePassword: '修改密码',
            passwordReset: '重置密码',
            batchCreate: '批量创建',
            batchUpdate: '批量更新',
            batchDelete: '批量删除',
            upload: '文件上传',
            download: '文件下载',
            export: '数据导出',
            adminModule: '管理员/认证',
            labModule: '实验室',
            groupModule: '课题组',
            memberModule: '成员',
            paperModule: '论文',
            newsModule: '新闻',
            projectModule: '项目',
            resourceModule: '资源',
            mediaModule: '媒体文件',
            imageUploadModule: '图片上传',
            loadError: '载入操作日志失败',
            emptyContent: '没有操作内容',
            copyJson: '复制JSON',
            copying: '复制中...',
            copySuccess: 'JSON已复制到剪贴板',
            copyFailed: '复制失败',
            expand: '展开',
            collapse: '收起'
        },
        // 个人资料管理翻译
        profile: {
            editProfile: '编辑个人资料',
            currentPassword: '当前密码',
            newPassword: '新密码',
            confirmPassword: '确认新密码',
            placeholders: {
                currentPassword: '请输入当前密码',
                newPassword: '请输入新密码（至少6位字符）',
                confirmPassword: '请确认新密码'
            },
            validation: {
                currentPasswordRequired: '请输入当前密码',
                newPasswordRequired: '请输入新密码',
                confirmPasswordRequired: '请确认新密码',
                passwordMinLength: '密码至少需要6位字符',
                passwordNotMatch: '两次输入的密码不一致'
            },
            messages: {
                profileUpdateSuccess: '个人资料更新成功',
                passwordChangeSuccess: '密码修改成功',
                passwordChangeFailed: '密码修改失败',
                updateFailed: '更新失败',
                noChanges: '没有需要保存的更改'
            }
        },
        // 系统管理翻译
        system: {
            backup: '数据备份',
            backupDesc: '备份和还原系统数据',
            settings: '系统设置',
            settingsDesc: '配置系统参数和选项'
        },
        // 錯誤頁面翻譯
        error: {
            pageNotFound: '頁面未找到',
            pageNotFoundDescription: '抱歉，您訪問的頁面不存在或已被移動。',
            adminPageNotFoundDescription: '抱歉，您訪問的管理頁面不存在。請檢查URL是否正確。',
            backToHome: '返回首頁',
            backToDashboard: '返回儀表板',
            quickNavigation: '快速導航',
            serverError: '服務器錯誤',
            serverErrorDescription: '服務器發生錯誤，請稍後再試。',
            networkError: '網絡錯誤',
            networkErrorDescription: '網絡連接失敗，請檢查您的網絡設置。'
        },
        // 图片裁切翻译
        imageCropper: {
            selectImage: '选择图片',
            supportedFormats: '支持 JPG、PNG、WebP 格式',
            cropAvatar: '裁切头像',
            cropLogo: '裁切Logo',
            cropCarousel: '裁切轮播图',
            cropImage: '裁切图片',
            avatarHint: '头像将被裁切为正方形',
            logoHint: 'Logo 可保持原始比例',
            carouselHint: '请选择适合的宽高比例',
            aspectRatio: '选择比例',
            reselect: '重新选择',
            cropAndSave: '裁切并保存',
            cropSuccess: '图片裁切成功',
            cropFailed: '图片裁切失败',
            invalidFormat: '请选择有效的图片格式',
            noImageSelected: '未选择图片进行裁切',
            noCropAreaSelected: '未选择裁切区域'
        }
    }
}