export default {
    nav: {
        home: '首頁',
        members: '成員',
        research: '研究',
        projects: '項目',
        papers: '論文',
        news: '新聞',
        about: '關於',
        menu: '導航菜單'
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
        goBack: '返回',
        back: '返回',
        page: '頁',
        noData: '暫無數據',
        itemsPerPage: '每頁條數'
    },
    auth: {
        loginFailed: '登錄失敗',
        loginNetworkError: '登錄失敗，請檢查網路連接',
        logoutFailed: '登出請求失敗',
        updateProfileFailed: '更新個人資訊失敗',
        updateFailed: '更新失敗，請重試',
        changePasswordFailed: '修改密碼失敗',
        changePasswordSuccess: '密碼修改成功',
        changeFailed: '修改失敗，請重試'
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
        teachers: '教師',
        professor: '教授',
        postdoc: '博士後',
        phd: '博士生',
        master: '碩士生',
        undergraduate: '大學生',
        alumni: '校友',
        others: '其他成員',
        description: '個人簡介',
        relatedPapers: '相關論文',
        positions: {
            professor: '教授',
            associateProfessor: '副教授',
            lecturer: '講師',
            assistantProfessor: '助理教授',
            postdoc: '博士後',
            phdStudent: '博士生',
            masterStudent: '碩士生',
            undergraduate: '大學生',
            alumni: '校友',
            other: '其他',
            year: '年級'
        }
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
        other: '其他',
        viewMore: '查看更多',
        notFound: '未找到該新聞',
        invalidId: '無效的新聞ID',
        fetchError: '獲取新聞詳情失敗',
        types: {
            publication: '論文發表',
            award: '獲獎消息',
            activity: '學術活動'
        }
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
        viewOnline: '線上查看',
        download: '下載',
        empty: '暫無論文數據',
        conference: '會議論文',
        journal: '期刊論文',
        patent: '專利',
        book: '書籍',
        other: '其他',
        date: '發表日期',
        venue: '發表期刊/會議',
        andOthers: '等',
        authors: '作者',
        abstract: '摘要',
        correspondingAuthor: '通訊作者',
        notFound: '未找到該論文',
        invalidId: '無效的論文ID',
        fetchError: '獲取論文詳情失敗',
        types: {
            conference: '會議論文',
            journal: '期刊論文',
            patent: '專利',
            book: '書籍',
            other: '其他'
        }
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
        name: '項目名稱',
        notFound: '未找到該項目',
        invalidId: '無效的項目ID',
        fetchError: '獲取項目詳情失敗'
    },
    groups: {
        title: '研究課題組',
        leader: '課題組負責人',
        description: '課題組簡介',
        members: '成員列表'
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
        fetchMemberDetail: '獲取成員詳情失敗',
        invalidMemberId: '無效的成員ID',
        invalidGroupId: '無效的課題組ID',
        networkError: '網路連接錯誤'
    },
    language: {
        chinese: '中文',
        english: 'English'
    },
    admin: {
        layout: {
            title: '管理後台',
            dashboard: '儀錶板',
            languageChanged: '語言已切換'
        },
        menu: {
            dashboard: '儀錶板',
            content: '內容管理',
            members: '成員管理',
            groups: '課題組管理',
            papers: '論文管理',
            projects: '項目管理',
            news: '新聞管理',
            lab: '實驗室管理',
            admins: '管理員管理',
            system: '系統管理'
        },
        login: {
            title: '管理員登錄',
            subtitle: '歡迎回到實驗室管理系統',
            usernamePlaceholder: '請輸入管理員使用者名稱',
            passwordPlaceholder: '請輸入管理員密碼',
            loginButton: '登錄',
            footer: '實驗室管理系統 v1.0',
            usernameRequired: '請輸入使用者名稱',
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
            databaseStatus: '資料庫',
            mediaStatus: '媒體服務',
            online: '在線',
            offline: '離線',
            normal: '正常',
            error: '異常',
            unknown: '未知',
            checking: '檢查中...',
            recentActivities: '最近活動',
            noActivities: '暫無活動記錄',
            todoList: '待辦事項',
            reviewPapers: '審核新提交的論文',
            updateLabInfo: '更新實驗室基本資訊',
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
            comingSoonDesc: '此功能正在開發中，敬請期待！',
            create: '創建',
            update: '更新',
            cancel: '取消',
            submit: '提交',
            loading: '載入中...',
            success: '成功',
            failed: '失敗',
            batchEdit: '批次編輯',
            batchDelete: '批次刪除',
            noPermission: '無權限',
            status: '狀態',
            // 表單選項
            memberTypes: {
                teacher: '教師',
                student: '學生',
                alumni: '校友'
            },
            jobTypes: {
                professor: '教授',
                associateProfessor: '副教授',
                lecturer: '講師',
                assistantResearcher: '助理研究員',
                postdoc: '博士後'
            },
            studentTypes: {
                phd: '博士生',
                master: '碩士生',
                undergraduate: '大學生'
            },
            paperTypes: {
                conference: '會議',
                journal: '期刊',
                patent: '專利',
                book: '書籍',
                other: '其他'
            },
            paperStatus: {
                submitting: '投稿中',
                accepted: '已接收'
            },
            projectStatus: {
                ongoing: '進行中',
                completed: '已完成'
            },
            newsTypes: {
                publication: '論文發表',
                award: '獲獎消息',
                activity: '學術活動'
            },
            validationMessages: {
                required: '此欄位為必填項',
                invalidEmail: '請輸入有效的電子信箱',
                invalidUrl: '請輸入有效的URL'
            },
            fileUpload: {
                selectImage: '選擇圖片',
                selectPdf: '選擇 PDF 文件',
                selectFile: '選擇文件',
                uploadSuccess: '文件上傳成功',
                uploadError: '文件上傳失敗'
            },
            viewDetails: '查看詳情',
            avatarPreview: '頭像預覽'
        },
        members: {
            addMember: '添加成員',
            editMember: '編輯成員',
            searchPlaceholder: '搜索成員姓名或信箱...',
            filterByType: '按類型篩選',
            filterByGroup: '按課題組篩選',
            avatar: '頭像',
            name: '姓名',
            email: '信箱',
            type: '類型',
            group: '課題組',
            status: '狀態',
            details: '詳情',
            studentGrade: '年級',
            jobType: '職位',
            studentType: '學位類型',
            grade: '年級',
            fetchError: '獲取成員列表失敗',
            deleteConfirmText: '確定要刪除這個成員嗎？此操作不可撤銷。',
            deleteSuccess: '成員刪除成功',
            deleteError: '刪除成員失敗',
            batchEdit: '批次編輯',
            batchEditTip: '將對選中的 {count} 位成員進行批次修改',
            batchDeleteConfirmText: '確定要刪除選中的 {count} 位成員嗎？此操作不可撤銷。',
            batchDeleteWarning: '批次刪除操作將無法恢復，請謹慎操作！',
            batchDeleteSuccess: '成功刪除 {count} 位成員',
            batchUpdateSuccess: '成功更新 {count} 位成員',
            updateError: '更新成員失敗',
            noUpdatesSelected: '請至少選擇一個要更新的欄位',
            jobTypes: {
                professor: '教授',
                assocProfessor: '副教授',
                lecturer: '講師',
                assistantProfessor: '助理教授',
                postdoc: '博士後'
            },
            studentTypes: {
                phd: '博士',
                master: '碩士',
                undergraduate: '本科'
            },
            placeholders: {
                studentGrade: '請輸入年級 (1-6)',
                jobType: '請選擇職位類型',
                studentType: '請選擇學位類型',
                status: '請選擇狀態'
            },
            // QuickActionModal 相關
            form: {
                nameZh: '中文姓名',
                nameEn: '英文姓名',
                email: '電子信箱',
                type: '成員類型',
                jobType: '職務類型',
                studentType: '學生類型',
                studentGrade: '年級',
                destinationZh: '去向（中文）',
                destinationEn: '去向（英文）',
                group: {
                    label: '課題組',
                    none: '無'
                },
                description: '成員描述（中文）',
                descriptionEn: '成員描述（英文）',
                avatar: '頭像上傳',
                placeholders: {
                    nameZh: '請輸入中文姓名',
                    nameEn: '請輸入英文姓名',
                    email: '請輸入電子信箱',
                    type: '請選擇成員類型',
                    jobType: '請選擇職務類型',
                    studentType: '請選擇學生類型',
                    studentGrade: '請輸入年級（1-10）',
                    destinationZh: '請輸進去向（中文）',
                    destinationEn: '請輸進去向（英文）',
                    group: '請選擇課題組',
                    description: '請輸入成員中文描述（支持 Markdown 語法）',
                    descriptionEn: '請輸入成員英文描述（支持 Markdown 語法）'
                },
                validation: {
                    nameZhRequired: '請輸入中文姓名',
                    nameEnRequired: '請輸入英文姓名',
                    emailRequired: '請輸入電子信箱',
                    typeRequired: '請選擇成員類型',
                    groupRequired: '請選擇課題組',
                    jobTypeRequired: '請選擇職務類型',
                    studentTypeRequired: '請選擇學生類型',
                    studentGradeRequired: '請輸入有效年級（1-10）'
                }
            }
        },
        papers: {
            addPaper: '添加論文',
            editPaper: '編輯論文',
            searchPlaceholder: '搜尋論文標題...',
            filterByType: '按類型篩選',
            filterByStatus: '按狀態篩選',
            fetchError: '獲取論文列表失敗',
            deleteConfirmText: '確定要刪除這篇論文嗎？此操作不可撤銷。',
            deleteSuccess: '論文刪除成功',
            deleteError: '刪除論文失敗',
            form: {
                titleZh: '中文標題',
                titleEn: '英文標題',
                description: '論文描述（中文）',
                descriptionEn: '論文描述（英文）',
                venue: '期刊/會議',
                type: '論文類型',
                date: '發表日期',
                status: '接收狀態',
                url: '論文連結',
                file: '論文文件',
                authors: '作者',
                labAuthors: '實驗室作者',
                allAuthors: '全部作者',
                allAuthorsZh: '全部作者（中文）',
                allAuthorsEn: '全部作者（英文）',
                placeholders: {
                    titleZh: '請輸入論文中文標題',
                    titleEn: '請輸入論文英文標題',
                    description: '請輸入論文中文描述（支持 Markdown 語法）',
                    descriptionEn: '請輸入論文英文描述（支持 Markdown 語法）',
                    venue: '請輸入發表期刊或會議',
                    type: '請選擇論文類型',
                    date: '請選擇發表日期',
                    status: '請選擇接收狀態',
                    url: '請輸入論文連結URL',
                    authors: '請選擇論文作者',
                    allAuthorsZh: '請輸入全部作者中文名稱（例如：張三, 李四, 王五）',
                    allAuthorsEn: '請輸入全部作者英文名稱（例如：John Smith, Jane Doe）'
                },
                validation: {
                    titleZhRequired: '請輸入中文標題',
                    typeRequired: '請選擇論文類型',
                    statusRequired: '請選擇接收狀態',
                    dateRequired: '請選擇發表日期'
                }
            }
        },
        projects: {
            addProject: '添加項目',
            editProject: '編輯項目',
            searchPlaceholder: '搜索項目名稱...',
            filterByStatus: '按狀態篩選',
            fetchError: '獲取項目列表失敗',
            deleteConfirmText: '確定要刪除這個項目嗎？此操作不可撤銷。',
            deleteSuccess: '項目刪除成功',
            deleteError: '刪除項目失敗',
            form: {
                nameZh: '中文名稱',
                nameEn: '英文名稱',
                description: '項目描述（中文）',
                descriptionEn: '項目描述（英文）',
                url: '項目URL',
                startDate: '開始日期',
                status: '項目狀態',
                placeholders: {
                    nameZh: '請輸入項目中文名稱',
                    nameEn: '請輸入項目英文名稱',
                    description: '請輸入項目描述（支持 Markdown 語法）',
                    descriptionEn: '請輸入項目英文描述（支持 Markdown 語法）',
                    url: '請輸入項目URL',
                    startDate: '請選擇開始日期',
                    status: '請選擇項目狀態'
                },
                validation: {
                    nameZhRequired: '請輸入項目中文名稱'
                }
            }
        },
        news: {
            addNews: '添加新聞',
            editNews: '編輯新聞',
            searchPlaceholder: '搜索新聞內容...',
            filterByType: '按類型篩選',
            fetchError: '獲取新聞列表失敗',
            deleteConfirmText: '確定要刪除這條新聞嗎？此操作不可撤銷。',
            deleteSuccess: '新聞刪除成功',
            deleteError: '刪除新聞失敗',
            form: {
                type: '新聞類型',
                titleZh: '中文標題',
                titleEn: '英文標題',
                contentZh: '中文內容',
                contentEn: '英文內容',
                date: '新聞日期',
                placeholders: {
                    type: '請選擇新聞類型',
                    titleZh: '請輸入新聞中文標題',
                    titleEn: '請輸入新聞英文標題',
                    contentZh: '請輸入新聞中文內容（支持 Markdown 語法）',
                    contentEn: '請輸入新聞英文內容（支持 Markdown 語法）',
                    date: '請選擇新聞日期'
                },
                validation: {
                    typeRequired: '請選擇新聞類型',
                    contentZhRequired: '請輸入新聞中文內容',
                    dateRequired: '請選擇新聞日期'
                }
            }
        },
        groups: {
            title: '研究課題組',
            leader: '課題組負責人',
            description: '課題組簡介',
            members: '成員列表',
            addGroup: '添加課題組',
            editGroup: '編輯課題組',
            searchPlaceholder: '搜索課題組名稱...',
            fetchError: '獲取課題組列表失敗',
            deleteConfirmText: '確定要刪除這個課題組嗎？此操作不可撤銷。',
            deleteSuccess: '課題組刪除成功',
            deleteError: '刪除課題組失敗',
            form: {
                nameZh: '中文名稱',
                nameEn: '英文名稱',
                descriptionZh: '中文描述',
                descriptionEn: '英文描述',
                leader: '組長',
                placeholders: {
                    nameZh: '請輸入課題組中文名稱',
                    nameEn: '請輸入課題組英文名稱',
                    descriptionZh: '請輸入課題組中文描述（支持 Markdown 語法）',
                    descriptionEn: '請輸入課題組英文描述（支持 Markdown 語法）',
                    leader: '請選擇組長'
                },
                validation: {
                    nameZhRequired: '請輸入課題組中文名稱'
                }
            }
        },
        // MarkdownEditor 翻譯
        markdownEditor: {
            preview: '預覽',
            edit: '編輯',
            tip: '支持 Markdown 語法：**粗體**, *斜體*, ### 標題, - 列表, [連結](url)',
            placeholder: '請輸入內容...',
            toolbar: {
                bold: '粗體',
                italic: '斜體',
                heading: '標題',
                list: '列表',
                link: '連結'
            },
            imageUpload: {
                selectFile: '選擇圖片文件',
                invalidFileType: '請選擇圖片文件',
                fileSizeExceeded: '圖片大小不能超過 5MB',
                uploadSuccess: '成功上傳 {count} 張圖片',
                uploadFailed: '圖片上傳失敗',
                uploading: '正在上傳圖片...'
            }
        },
        // QuickActionModal 翻譯
        quickAction: {
            modalTitle: {
                createMember: '新增成員',
                editMember: '編輯成員',
                createPaper: '新增論文',
                editPaper: '編輯論文',
                createProject: '新增項目',
                editProject: '編輯項目',
                createNews: '新增新聞',
                editNews: '編輯新聞',
                createGroup: '新增課題組',
                editGroup: '編輯課題組',
                createAdmin: '新增管理員',
                editAdmin: '編輯管理員'
            },
            messages: {
                createSuccess: '創建成功',
                updateSuccess: '更新成功',
                operationFailed: '操作失敗',
                checkInput: '操作失敗，請檢查輸入',
                loadGroupsFailed: '載入課題組失敗',
                loadMembersFailed: '載入成員失敗'
            },
            timeFormat: {
                daysAgo: '天前',
                hoursAgo: '小時前',
                minutesAgo: '分鐘前',
                justNow: '剛剛',
                yearsAgo: '年前',
                monthsAgo: '個月前',
                shortMinutesAgo: '分前',
                now: '剛才'
            },
            activities: {
                created: '新增了',
                updated: '編輯了',
                moduleNames: {
                    members: '成員',
                    papers: '論文',
                    projects: '項目',
                    news: '新聞',
                    groups: '課題組'
                }
            }
        },
        // 實驗室管理翻譯
        lab: {
            basicInfo: '基本資訊',
            contactInfo: '聯繫資訊',
            imageManagement: '圖片管理',
            nameZh: '實驗室中文名稱',
            nameEn: '實驗室英文名稱',
            descZh: '中文描述',
            descEn: '英文描述',
            addressZh: '中文地址',
            addressEn: '英文地址',
            email: '聯繫信箱',
            phone: '聯絡電話',
            logo: '實驗室Logo',
            carouselImages: '輪播圖片',
            carouselImage: '輪播圖片 {number}',
            placeholders: {
                nameZh: '請輸入實驗室中文名稱',
                nameEn: '請輸入實驗室英文名稱',
                descZh: '請輸入實驗室中文描述',
                descEn: '請輸入實驗室英文描述',
                addressZh: '請輸入實驗室中文地址',
                addressEn: '請輸入實驗室英文地址',
                email: '請輸入聯繫信箱',
                phone: '請輸入聯絡電話'
            },
            validation: {
                nameZhRequired: '實驗室中文名稱必填',
                nameEnRequired: '實驗室英文名稱必填'
            },
            messages: {
                fetchFailed: '獲取實驗室資訊失敗',
                saveSuccess: '保存成功',
                saveFailed: '保存失敗'
            },
            logoPreview: 'Logo 預覽',
            carouselPreview: '輪播圖 {number} 預覽'
        },
        // 管理員管理翻譯
        admins: {
            addAdmin: '添加管理員',
            editAdmin: '編輯管理員',
            resetPassword: '重置密碼',
            searchPlaceholder: '搜索管理員使用者名稱...',
            adminName: '使用者名稱',
            adminType: '類型',
            superAdmin: '超級管理員',
            normalAdmin: '普通管理員',
            createdAt: '創建時間',
            fetchError: '獲取管理員列表失敗',
            deleteConfirmText: '確定要刪除這個管理員嗎？此操作不可撤銷。',
            deleteSuccess: '管理員刪除成功',
            deleteError: '刪除管理員失敗',
            noEditPermission: '無權限編輯此管理員',
            noDeletePermission: '無權限刪除此管理員',
            noResetPasswordPermission: '無權限重置此管理員密碼',
            noCreatePermission: '無權限創建管理員',
            cannotEditSelf: '不能編輯自己的帳號',
            cannotEditSuperAdmin: '不能編輯超級管理員',
            messages: {
                passwordResetSuccess: '密碼重置成功',
                passwordResetFailed: '密碼重置失敗'
            },
            form: {
                adminName: '使用者名稱',
                adminPass: '密碼',
                newPassword: '新密碼',
                confirmPassword: '確認密碼',
                isSuper: '管理員類型',
                enable: '狀態',
                placeholders: {
                    adminName: '請輸入使用者名稱',
                    adminPass: '請輸入密碼',
                    newPassword: '請輸入新密碼（至少8位字元）',
                    confirmPassword: '請確認新密碼',
                    isSuper: '請選擇管理員類型',
                    enable: '請選擇狀態'
                },
                validation: {
                    adminNameRequired: '使用者名稱必填',
                    adminPassRequired: '密碼必填',
                    newPasswordRequired: '新密碼必填',
                    confirmPasswordRequired: '確認密碼必填'
                }
            }
        },
        // 操作日誌翻譯
        operationLogs: {
            title: '操作日誌',
            description: '查看所有管理員操作和系統活動記錄',
            searchPlaceholder: '搜索管理員姓名、操作類型或內容...',
            selectAdmin: '選擇管理員',
            selectOperation: '選擇操作類型',
            selectModule: '選擇模組',
            allAdmins: '全部管理員',
            allOperations: '全部操作',
            allModules: '全部模組',
            time: '操作時間',
            admin: '操作管理員',
            operation: '操作類型',
            module: '操作模組',
            content: '操作內容',
            create: '創建',
            update: '更新',
            delete: '刪除',
            login: '登錄',
            logout: '登出',
            changePassword: '修改密碼',
            passwordReset: '重置密碼',
            batchCreate: '批次創建',
            batchUpdate: '批次更新',
            batchDelete: '批次刪除',
            upload: '文件上傳',
            download: '文件下載',
            export: '數據匯出',
            adminModule: '管理員/認證',
            labModule: '實驗室',
            groupModule: '課題組',
            memberModule: '成員',
            paperModule: '論文',
            newsModule: '新聞',
            projectModule: '項目',
            resourceModule: '資源',
            mediaModule: '媒體檔案',
            imageUploadModule: '圖片上傳',
            loadError: '載入操作日誌失敗',
            emptyContent: '沒有操作內容',
            copyJson: '複製JSON',
            copying: '複製中...',
            copySuccess: 'JSON已複製到剪貼簿',
            copyFailed: '複製失敗',
            expand: '展開',
            collapse: '收起'
        },
        // 個人資料管理翻譯
        profile: {
            editProfile: '編輯個人資料',
            currentPassword: '當前密碼',
            newPassword: '新密碼',
            confirmPassword: '確認新密碼',
            placeholders: {
                currentPassword: '請輸入當前密碼',
                newPassword: '請輸入新密碼（至少6位字元）',
                confirmPassword: '請確認新密碼'
            },
            validation: {
                currentPasswordRequired: '請輸入當前密碼',
                newPasswordRequired: '請輸入新密碼',
                confirmPasswordRequired: '請確認新密碼',
                passwordMinLength: '密碼至少需要6位字元',
                passwordNotMatch: '兩次輸入的密碼不一致'
            },
            messages: {
                profileUpdateSuccess: '個人資料更新成功',
                passwordChangeSuccess: '密碼修改成功',
                passwordChangeFailed: '密碼修改失敗',
                updateFailed: '更新失敗',
                noChanges: '沒有需要保存的更改'
            }
        },
        // 系統管理翻譯
        system: {
            backup: '數據備份',
            backupDesc: '備份和還原系統數據',
            settings: '系統設置',
            settingsDesc: '配置系統參數和選項'
        },
        // 圖片裁切翻譯
        imageCropper: {
            selectImage: '選擇圖片',
            supportedFormats: '支持 JPG、PNG、WebP 格式',
            cropAvatar: '裁切頭像',
            cropLogo: '裁切Logo',
            cropCarousel: '裁切輪播圖',
            avatarHint: '頭像將被裁切為正方形',
            logoHint: 'Logo 可保持原始比例',
            carouselHint: '請選擇適合的寬高比例',
            aspectRatio: '選擇比例',
            reselect: '重新選擇',
            cropAndSave: '裁切並保存',
            cropSuccess: '圖片裁切成功',
            cropFailed: '圖片裁切失敗',
            invalidFormat: '請選擇有效的圖片格式',
            noImageSelected: '未選擇圖片進行裁切',
            noCropAreaSelected: '未選擇裁切區域'
        }
    }
}