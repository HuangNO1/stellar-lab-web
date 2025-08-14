export default {
  nav: {
    home: 'Home',
    members: 'Members',
    research: 'Research',
    projects: 'Projects',
    papers: 'Papers',
    news: 'News',
    about: 'About',
    menu: 'Navigation Menu'
  },
  common: {
    language: 'Language',
    theme: 'Theme',
    light: 'Light Mode',
    dark: 'Dark Mode',
    loading: 'Loading...',
    error: 'Error',
    success: 'Success',
    confirm: 'Confirm',
    cancel: 'Cancel',
    contact: 'Contact Us',
    retry: 'Retry',
    viewDetails: 'View Details',
    fetchError: 'Failed to fetch data',
    goBack: 'Go Back',
    back: 'Back',
    page: 'Page',
    noData: 'No Data',
    itemsPerPage: 'Items per page'
  },
  auth: {
    loginFailed: 'Login failed',
    loginNetworkError: 'Login failed, please check network connection',
    logoutFailed: 'Logout request failed',
    updateProfileFailed: 'Failed to update profile',
    updateFailed: 'Update failed, please retry',
    changePasswordFailed: 'Failed to change password',
    changePasswordSuccess: 'Password changed successfully',
    changeFailed: 'Change failed, please retry'
  },
  defaults: {
    labName: 'Laboratory',
    labDescription: 'Our laboratory focuses on cutting-edge technology research',
    labFallbackName: 'Smart Laboratory',
    carousel: {
      alt1: 'Laboratory Carousel Image 1',
      alt2: 'Laboratory Carousel Image 2',
      alt3: 'Laboratory Carousel Image 3', 
      alt4: 'Laboratory Carousel Image 4',
      defaultAlt1: 'Default Carousel Image 1',
      defaultAlt2: 'Default Carousel Image 2'
    }
  },
  home: {
    title: 'Welcome to Our Lab',
    subtitle: 'Exploring Science, Creating the Future',
    description: 'We are a laboratory focused on cutting-edge scientific research'
  },
  members: {
    title: 'Team Members',
    teachers: 'Teachers',
    professor: 'Professor',
    postdoc: 'Postdoc',
    phd: 'PhD Student',
    master: 'Master Student',
    undergraduate: 'Undergraduate',
    alumni: 'Alumni',
    others: 'Others',
    description: 'Biography',
    relatedPapers: 'Related Papers',
    positions: {
      professor: 'Professor',
      associateProfessor: 'Associate Professor',
      lecturer: 'Lecturer',
      assistantProfessor: 'Assistant Professor',
      postdoc: 'Postdoc',
      phdStudent: 'PhD Student',
      masterStudent: 'Master Student',
      undergraduate: 'Undergraduate',
      alumni: 'Alumni',
      other: 'Other',
      year: 'Year'
    }
  },
  research: {
    title: 'Research Areas',
    projects_title: 'Research Projects',
    papers_title: 'Academic Papers',
    ongoing: 'Ongoing',
    completed: 'Completed'
  },
  news: {
    title: 'Lab News',
    latest: 'Latest News',
    date: 'Date',
    description: 'View the latest updates from our lab',
    type: 'Type',
    empty: 'No news available',
    paperPublished: 'Paper Published',
    award: 'Award News',
    academic: 'Academic Activity',
    other: 'Other',
    viewMore: 'View More',
    notFound: 'News not found',
    invalidId: 'Invalid news ID',
    fetchError: 'Failed to fetch news details',
    types: {
      publication: 'Paper Published',
      award: 'Award News',
      activity: 'Academic Activity'
    }
  },
  about: {
    title: 'About Us',
    mission: 'Mission',
    vision: 'Vision',
    contact: 'Contact Us'
  },
  researchGroups: {
    title: 'Research Groups',
    viewDetails: 'View Details',
    leader: 'Group Leader',
    members: 'Members Count',
    projects: 'Projects Count'
  },
  papers: {
    title: 'Publications',
    accepted: 'Accepted',
    submitted: 'Submitted',
    description: 'View academic papers published by our lab',
    type: 'Paper Type',
    status: 'Status',
    viewOnline: 'View Online',
    download: 'Download',
    empty: 'No papers available',
    conference: 'Conference Paper',
    journal: 'Journal Paper',
    patent: 'Patent',
    book: 'Book',
    other: 'Other',
    date: 'Publication Date',
    venue: 'Journal/Conference',
    andOthers: 'et al.',
    authors: 'Authors',
    abstract: 'Abstract',
    correspondingAuthor: 'Corresponding Author',
    notFound: 'Paper not found',
    invalidId: 'Invalid paper ID',
    fetchError: 'Failed to fetch paper details',
    types: {
      conference: 'Conference Paper',
      journal: 'Journal Paper',
      patent: 'Patent',
      book: 'Book',
      other: 'Other'
    }
  },
  groups: {
    title: 'Research Groups',
    leader: 'Group Leader',
    description: 'Group Description',
    members: 'Members',
    addGroup: 'Add Group',
    editGroup: 'Edit Group',
    searchPlaceholder: 'Search group name...',
    fetchError: 'Failed to fetch research groups',
    deleteConfirmText: 'Are you sure you want to delete this research group? This action cannot be undone.',
    deleteSuccess: 'Research group deleted successfully',
    deleteError: 'Failed to delete research group'
  },
  projects: {
    title: 'Research Projects',
    description: 'View research projects from our lab',
    status: 'Status',
    startDate: 'Start Date',
    viewRepository: 'View Repository',
    empty: 'No projects available',
    ongoing: 'Ongoing',
    completed: 'Completed',
    name: 'Project Name',
    notFound: 'Project not found',
    invalidId: 'Invalid project ID',
    fetchError: 'Failed to fetch project details'
  },
  search: {
    placeholder: 'Search...',
    advanced: 'Advanced Search',
    dateRange: 'Date Range',
    startDate: 'Start Date',
    endDate: 'End Date',
    all: 'All',
    sortBy: 'Sort By',
    default: 'Default',
    desc: 'Descending',
    asc: 'Ascending',
    search: 'Search'
  },
  emptyStates: {
    noMembers: 'No member data available',
    noGroupMembers: 'No members in this group',
    groupNotFound: 'Group not found',
    memberNotFound: 'Member not found'
  },
  errorMessages: {
    fetchGroupDetail: 'Failed to fetch group details',
    fetchMemberDetail: 'Failed to fetch member details',
    invalidMemberId: 'Invalid member ID',
    invalidGroupId: 'Invalid group ID',
    networkError: 'Network connection error'
  },
  language: {
    chinese: '中文',
    english: 'English'
  },
  admin: {
    layout: {
      title: 'Admin Panel',
      dashboard: 'Dashboard',
      languageChanged: 'Language switched'
    },
    menu: {
      dashboard: 'Dashboard',
      content: 'Content Management',
      members: 'Member Management',
      groups: 'Group Management',
      papers: 'Paper Management',
      projects: 'Project Management',
      news: 'News Management',
      lab: 'Lab Management',
      admins: 'Admin Management',
      system: 'System Management'
    },
    login: {
      title: 'Admin Login',
      subtitle: 'Welcome to Lab Management System',
      usernamePlaceholder: 'Enter admin username',
      passwordPlaceholder: 'Enter admin password',
      loginButton: 'Login',
      footer: 'Lab Management System v1.0',
      usernameRequired: 'Username is required',
      passwordRequired: 'Password is required',
      loginSuccess: 'Login successful',
      loginFailed: 'Login failed'
    },
    user: {
      profile: 'Profile',
      changePassword: 'Change Password',
      logout: 'Logout',
      logoutSuccess: 'Successfully logged out'
    },
    dashboard: {
      totalMembers: 'Total Members',
      totalPapers: 'Total Papers',
      totalProjects: 'Total Projects',
      totalNews: 'Total News',
      quickActions: 'Quick Actions',
      addMember: 'Add Member',
      addPaper: 'Add Paper',
      addProject: 'Add Project',
      addNews: 'Add News',
      systemStatus: 'System Status',
      apiStatus: 'API Service',
      databaseStatus: 'Database',
      mediaStatus: 'Media Service',
      online: 'Online',
      offline: 'Offline',
      normal: 'Normal',
      error: 'Error',
      unknown: 'Unknown',
      checking: 'Checking...',
      recentActivities: 'Recent Activities',
      noActivities: 'No recent activities',
      todoList: 'Todo List',
      reviewPapers: 'Review submitted papers',
      updateLabInfo: 'Update lab information',
      checkNews: 'Check news content'
    },
    common: {
      enabled: 'Enabled',
      disabled: 'Disabled',
      edit: 'Edit',
      delete: 'Delete',
      confirmDelete: 'Confirm Delete',
      actions: 'Actions',
      comingSoon: 'Coming Soon',
      comingSoonDesc: 'This feature is under development. Stay tuned!',
      create: 'Create',
      update: 'Update',
      cancel: 'Cancel',
      submit: 'Submit',
      loading: 'Loading...',
      success: 'Success',
      failed: 'Failed',
      batchEdit: 'Batch Edit',
      batchDelete: 'Batch Delete',
      noPermission: 'No Permission',
      status: 'Status',
      // Form Options
      memberTypes: {
        teacher: 'Teacher',
        student: 'Student',
        alumni: 'Alumni'
      },
      jobTypes: {
        professor: 'Professor',
        associateProfessor: 'Associate Professor',
        lecturer: 'Lecturer',
        assistantResearcher: 'Assistant Researcher',
        postdoc: 'Postdoc'
      },
      studentTypes: {
        phd: 'PhD Student',
        master: 'Master Student',
        undergraduate: 'Undergraduate'
      },
      paperTypes: {
        conference: 'Conference',
        journal: 'Journal',
        patent: 'Patent',
        book: 'Book',
        other: 'Other'
      },
      paperStatus: {
        submitting: 'Submitting',
        accepted: 'Accepted'
      },
      projectStatus: {
        ongoing: 'Ongoing',
        completed: 'Completed'
      },
      newsTypes: {
        publication: 'Publication',
        award: 'Award',
        activity: 'Activity'
      },
      validationMessages: {
        required: 'This field is required',
        invalidEmail: 'Please enter a valid email',
        invalidUrl: 'Please enter a valid URL'
      },
      fileUpload: {
        selectImage: 'Select Image',
        selectPdf: 'Select PDF File',
        selectFile: 'Select File',
        uploadSuccess: 'File uploaded successfully',
        uploadError: 'File upload failed'
      },
      viewDetails: 'View Details',
      avatarPreview: 'Avatar Preview'
    },
    members: {
      addMember: 'Add Member',
      editMember: 'Edit Member',
      searchPlaceholder: 'Search member name or email...',
      filterByType: 'Filter by type',
      filterByGroup: 'Filter by group',
      avatar: 'Avatar',
      name: 'Name',
      email: 'Email',
      type: 'Type',
      group: 'Group',
      status: 'Status',
      details: 'Details',
      studentGrade: 'Grade',
      jobType: 'Job Type',
      studentType: 'Student Type',
      grade: 'Grade',
      fetchError: 'Failed to fetch members',
      deleteConfirmText: 'Are you sure you want to delete this member? This action cannot be undone.',
      deleteSuccess: 'Member deleted successfully',
      deleteError: 'Failed to delete member',
      batchEdit: 'Batch Edit',
      batchEditTip: 'Will batch update {count} selected members',
      batchDeleteConfirmText: 'Are you sure you want to delete {count} selected members? This action cannot be undone.',
      batchDeleteWarning: 'Batch delete operation cannot be recovered, please proceed with caution!',
      batchDeleteSuccess: 'Successfully deleted {count} members',
      batchUpdateSuccess: 'Successfully updated {count} members',
      updateError: 'Failed to update members',
      noUpdatesSelected: 'Please select at least one field to update',
      jobTypes: {
        professor: 'Professor',
        assocProfessor: 'Associate Professor',
        lecturer: 'Lecturer',
        assistantProfessor: 'Assistant Professor',
        postdoc: 'Postdoc'
      },
      studentTypes: {
        phd: 'PhD',
        master: 'Master',
        undergraduate: 'Undergraduate'
      },
      placeholders: {
        studentGrade: 'Enter grade (1-6)',
        jobType: 'Select job type',
        studentType: 'Select student type',
        status: 'Select status'
      },
      // QuickActionModal related
      form: {
        nameZh: 'Chinese Name',
        nameEn: 'English Name',
        email: 'Email',
        type: 'Member Type',
        jobType: 'Job Type',
        studentType: 'Student Type',
        studentGrade: 'Grade',
        destinationZh: 'Destination (Chinese)',
        destinationEn: 'Destination (English)',
        group: {
          label: 'Research Group',
          none: 'None'
        },
        description: 'Description (Chinese)',
        descriptionEn: 'Description (English)',
        avatar: 'Avatar Upload',
        placeholders: {
          nameZh: 'Enter Chinese name',
          nameEn: 'Enter English name',
          email: 'Enter email address',
          type: 'Select member type',
          jobType: 'Select job type',
          studentType: 'Select student type',
          studentGrade: 'Enter grade (1-10)',
          destinationZh: 'Enter destination (Chinese)',
          destinationEn: 'Enter destination (English)',
          group: 'Select research group',
          description: 'Enter member description (Chinese, supports Markdown syntax)',
          descriptionEn: 'Enter member description (English, supports Markdown syntax)'
        },
        validation: {
          nameZhRequired: 'Chinese name is required',
          nameEnRequired: 'English name is required',
          emailRequired: 'Email is required',
          typeRequired: 'Member type is required',
          groupRequired: 'Research group is required',
          jobTypeRequired: 'Job type is required',
          studentTypeRequired: 'Student type is required',
          studentGradeRequired: 'Valid grade (1-10) is required'
        }
      }
    },
    groups: {
      title: 'Research Groups',
      leader: 'Group Leader',
      description: 'Group Description',
      members: 'Member List',
      addGroup: 'Add Group',
      editGroup: 'Edit Group',
      form: {
        nameZh: 'Chinese Name',
        nameEn: 'English Name',
        descriptionZh: 'Chinese Description',
        descriptionEn: 'English Description',
        leader: 'Leader',
        placeholders: {
          nameZh: 'Enter group Chinese name',
          nameEn: 'Enter group English name',
          descriptionZh: 'Enter group Chinese description (supports Markdown syntax)',
          descriptionEn: 'Enter group English description (supports Markdown syntax)',
          leader: 'Select leader'
        },
        validation: {
          nameZhRequired: 'Group Chinese name is required'
        }
      }
    },
    papers: {
      addPaper: 'Add Paper',
      editPaper: 'Edit Paper',
      searchPlaceholder: 'Search paper title...',
      filterByType: 'Filter by type',
      filterByStatus: 'Filter by status',
      fetchError: 'Failed to fetch papers',
      deleteConfirmText: 'Are you sure you want to delete this paper? This action cannot be undone.',
      deleteSuccess: 'Paper deleted successfully',
      deleteError: 'Failed to delete paper',
      form: {
        titleZh: 'Chinese Title',
        titleEn: 'English Title',
        description: 'Description (Chinese)',
        descriptionEn: 'Description (English)',
        venue: 'Journal/Conference',
        type: 'Paper Type',
        date: 'Publication Date',
        status: 'Acceptance Status',
        url: 'Paper URL',
        file: 'Paper File',
        authors: 'Authors',
        labAuthors: 'Lab Authors',
        allAuthors: 'All Authors',
        allAuthorsZh: 'All Authors (Chinese)',
        allAuthorsEn: 'All Authors (English)',
        placeholders: {
          titleZh: 'Enter paper Chinese title',
          titleEn: 'Enter paper English title',
          description: 'Enter paper Chinese description (supports Markdown syntax)',
          descriptionEn: 'Enter paper English description (supports Markdown syntax)',
          venue: 'Enter publication journal or conference',
          type: 'Select paper type',
          date: 'Select publication date',
          status: 'Select acceptance status',
          url: 'Enter paper URL',
          authors: 'Select paper authors',
          allAuthorsZh: 'Enter all authors in Chinese (e.g., 張三, 李四, 王五)',
          allAuthorsEn: 'Enter all authors in English (e.g., John Smith, Jane Doe)',
        },
        validation: {
          titleZhRequired: 'Chinese title is required',
          typeRequired: 'Paper type is required',
          statusRequired: 'Acceptance status is required',
          dateRequired: 'Publication date is required'
        }
      }
    },
    projects: {
      addProject: 'Add Project',
      editProject: 'Edit Project',
      searchPlaceholder: 'Search project name...',
      filterByStatus: 'Filter by status',
      fetchError: 'Failed to fetch projects',
      deleteConfirmText: 'Are you sure you want to delete this project? This action cannot be undone.',
      deleteSuccess: 'Project deleted successfully',
      deleteError: 'Failed to delete project',
      form: {
        nameZh: 'Chinese Name',
        nameEn: 'English Name',
        description: 'Description (Chinese)',
        descriptionEn: 'Description (English)',
        url: 'Project URL',
        startDate: 'Start Date',
        status: 'Project Status',
        placeholders: {
          nameZh: 'Enter project Chinese name',
          nameEn: 'Enter project English name',
          description: 'Enter project Chinese description (supports Markdown syntax)',
          descriptionEn: 'Enter project English description (supports Markdown syntax)',
          url: 'Enter project URL',
          startDate: 'Select start date',
          status: 'Select project status'
        },
        validation: {
          nameZhRequired: 'Project Chinese name is required'
        }
      }
    },
    news: {
      addNews: 'Add News',
      editNews: 'Edit News',
      searchPlaceholder: 'Search news content...',
      filterByType: 'Filter by type',
      fetchError: 'Failed to fetch news',
      deleteConfirmText: 'Are you sure you want to delete this news? This action cannot be undone.',
      deleteSuccess: 'News deleted successfully',
      deleteError: 'Failed to delete news',
      form: {
        type: 'News Type',
        titleZh: 'Chinese Title',
        titleEn: 'English Title',
        contentZh: 'Chinese Content',
        contentEn: 'English Content',
        date: 'News Date',
        placeholders: {
          type: 'Select news type',
          contentZh: 'Enter Chinese news content (supports Markdown syntax)',
          contentEn: 'Enter English news content (supports Markdown syntax)',
          date: 'Select news date'
        },
        validation: {
          typeRequired: 'News type is required',
          contentZhRequired: 'Chinese news content is required',
          dateRequired: 'News date is required'
        }
      }
    },
    // MarkdownEditor translations
    markdownEditor: {
      preview: 'Preview',
      edit: 'Edit',
      tip: 'Supports Markdown syntax: **bold**, *italic*, ### heading, - list, [link](url)',
      placeholder: 'Enter content...',
      toolbar: {
        bold: 'Bold',
        italic: 'Italic',
        heading: 'Heading',
        list: 'List',
        link: 'Link'
      },
      imageUpload: {
        selectFile: 'Select image file',
        invalidFileType: 'Please select an image file',
        fileSizeExceeded: 'Image size cannot exceed 5MB',
        uploadSuccess: 'Successfully uploaded {count} images',
        uploadFailed: 'Image upload failed',
        uploading: 'Uploading images...'
      }
    },
    // QuickActionModal translations
    quickAction: {
      modalTitle: {
        createMember: 'Add Member',
        editMember: 'Edit Member',
        createPaper: 'Add Paper',
        editPaper: 'Edit Paper',
        createProject: 'Add Project',
        editProject: 'Edit Project',
        createNews: 'Add News',
        editNews: 'Edit News',
        createGroup: 'Add Group',
        editGroup: 'Edit Group',
        createAdmin: 'Add Admin',
        editAdmin: 'Edit Admin'
      },
      messages: {
        createSuccess: 'Created successfully',
        updateSuccess: 'Updated successfully',
        operationFailed: 'Operation failed',
        checkInput: 'Operation failed, please check your input',
        loadGroupsFailed: 'Failed to load research groups',
        loadMembersFailed: 'Failed to load members'
      },
      timeFormat: {
        daysAgo: ' days ago',
        hoursAgo: ' hours ago',
        minutesAgo: ' minutes ago',
        justNow: 'just now',
        yearsAgo: ' years ago',
        monthsAgo: ' months ago',
        shortMinutesAgo: 'm ago',
        now: 'now',
        day: 'day',
        days: 'days',
        hour: 'hour',
        hours: 'hours',
        minute: 'minute',
        minutes: 'minutes',
        year: 'year',
        years: 'years',
        month: 'month',
        months: 'months'
      },
      activities: {
        created: 'created',
        updated: 'updated',
        moduleNames: {
          members: 'member',
          papers: 'paper',
          projects: 'project',
          news: 'news',
          groups: 'group'
        }
      }
    },
    // Lab Management translations
    lab: {
      basicInfo: 'Basic Information',
      contactInfo: 'Contact Information',
      imageManagement: 'Image Management',
      nameZh: 'Lab Chinese Name',
      nameEn: 'Lab English Name',
      descZh: 'Chinese Description',
      descEn: 'English Description',
      addressZh: 'Chinese Address',
      addressEn: 'English Address',
      email: 'Contact Email',
      phone: 'Contact Phone',
      logo: 'Lab Logo',
      carouselImages: 'Carousel Images',
      carouselImage: 'Carousel Image {number}',
      placeholders: {
        nameZh: 'Enter lab Chinese name',
        nameEn: 'Enter lab English name',
        descZh: 'Enter lab Chinese description',
        descEn: 'Enter lab English description',
        addressZh: 'Enter lab Chinese address',
        addressEn: 'Enter lab English address',
        email: 'Enter contact email',
        phone: 'Enter contact phone'
      },
      validation: {
        nameZhRequired: 'Lab Chinese name is required',
        nameEnRequired: 'Lab English name is required'
      },
      messages: {
        fetchFailed: 'Failed to fetch lab information',
        saveSuccess: 'Saved successfully',
        saveFailed: 'Save failed'
      },
      logoPreview: 'Logo Preview',
      carouselPreview: 'Carousel Image {number} Preview'
    },
    // Image Cropper Modal translations
    imageCropper: {
      selectImage: 'Click or drag files to this area to upload',
      supportedFormats: 'Supports JPG, PNG, GIF formats',
      aspectRatio: 'Aspect Ratio',
      cropAvatar: 'Crop Avatar',
      cropLogo: 'Crop Logo',
      cropCarousel: 'Crop Carousel Image',
      avatarHint: 'Recommended 1:1 square ratio',
      logoHint: 'Supports any ratio, recommended horizontal layout',
      carouselHint: 'Multiple ratios available, choose as needed',
      reselect: 'Reselect Image',
      cropAndSave: 'Crop and Save',
      invalidFormat: 'Invalid file format, please select an image file',
      cropSuccess: 'Image cropped successfully',
      cropFailed: 'Image crop failed',
      noImageSelected: 'No image selected for cropping',
      noCropAreaSelected: 'No crop area selected'
    },
    // Admin Management translations
    admins: {
      addAdmin: 'Add Admin',
      editAdmin: 'Edit Admin',
      searchPlaceholder: 'Search admin username...',
      adminName: 'Username',
      adminType: 'Type',
      superAdmin: 'Super Admin',
      normalAdmin: 'Normal Admin',
      createdAt: 'Created At',
      fetchError: 'Failed to fetch admin list',
      deleteConfirmText: 'Are you sure you want to delete this admin? This action cannot be undone.',
      deleteSuccess: 'Admin deleted successfully',
      deleteError: 'Failed to delete admin',
      noEditPermission: 'No permission to edit this admin',
      noDeletePermission: 'No permission to delete this admin',
      noCreatePermission: 'No permission to create admin',
      cannotEditSelf: 'Cannot edit your own account',
      cannotEditSuperAdmin: 'Cannot edit super admin accounts',
      form: {
        adminName: 'Username',
        adminPass: 'Password',
        isSuper: 'Admin Type',
        enable: 'Status',
        placeholders: {
          adminName: 'Enter username',
          adminPass: 'Enter password',
          isSuper: 'Select admin type',
          enable: 'Select status'
        },
        validation: {
          adminNameRequired: 'Username is required',
          adminPassRequired: 'Password is required'
        }
      }
    },
    // Operation Logs translations
    operationLogs: {
      title: 'Operation Logs',
      description: 'View all admin operations and system activities',
      searchPlaceholder: 'Search admin name, operation type, or content...',
      selectAdmin: 'Select Admin',
      selectOperation: 'Select Operation',
      selectModule: 'Select Module',
      allAdmins: 'All Admins',
      allOperations: 'All Operations',
      allModules: 'All Modules',
      time: 'Time',
      admin: 'Admin',
      operation: 'Operation',
      module: 'Module',
      content: 'Content',
      create: 'Create',
      update: 'Update',
      delete: 'Delete',
      login: 'Login',
      logout: 'Logout',
      changePassword: 'Change Password',
      batchDelete: 'Batch Delete',
      batchUpdate: 'Batch Update',
      upload: 'Upload',
      adminModule: 'Admin/Auth',
      labModule: 'Lab',
      groupModule: 'Group',
      memberModule: 'Member',
      paperModule: 'Paper',
      newsModule: 'News',
      projectModule: 'Project',
      mediaModule: 'Media Files',
      imageUploadModule: 'Image Upload',
      loadError: 'Failed to load operation logs',
      emptyContent: 'No operation content',
      copyJson: 'Copy JSON',
      copying: 'Copying...',
      copySuccess: 'JSON copied to clipboard',
      copyFailed: 'Copy failed',
      expand: 'Expand',
      collapse: 'Collapse'
    },
    // Profile Management translations
    profile: {
      editProfile: 'Edit Profile',
      currentPassword: 'Current Password',
      newPassword: 'New Password',
      confirmPassword: 'Confirm Password',
      placeholders: {
        currentPassword: 'Enter current password',
        newPassword: 'Enter new password (at least 6 characters)',
        confirmPassword: 'Confirm new password'
      },
      validation: {
        currentPasswordRequired: 'Current password is required',
        newPasswordRequired: 'New password is required',
        confirmPasswordRequired: 'Please confirm new password',
        passwordMinLength: 'Password must be at least 6 characters',
        passwordNotMatch: 'Passwords do not match'
      },
      messages: {
        profileUpdateSuccess: 'Profile updated successfully',
        passwordChangeSuccess: 'Password changed successfully',
        passwordChangeFailed: 'Failed to change password',
        updateFailed: 'Update failed',
        noChanges: 'No changes to save'
      }
    },
    // System Management translations
    system: {
      backup: 'Data Backup',
      backupDesc: 'Backup and restore system data',
      settings: 'System Settings',
      settingsDesc: 'Configure system parameters and options'
    }
  }
}