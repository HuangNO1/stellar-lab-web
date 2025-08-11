export default {
  nav: {
    home: 'Home',
    members: 'Members',
    research: 'Research',
    projects: 'Projects',
    papers: 'Papers',
    news: 'News',
    about: 'About'
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
    goBack: 'Go Back'
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
    professor: 'Professor',
    postdoc: 'Postdoc',
    phd: 'PhD Student',
    master: 'Master Student',
    undergraduate: 'Undergraduate',
    alumni: 'Alumni',
    others: 'Others',
    description: 'Biography',
    relatedPapers: 'Related Papers'
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
    other: 'Other'
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
    venue: 'Journal/Conference'
  },
  groups: {
    title: 'Research Groups',
    leader: 'Group Leader',
    description: 'Group Description',
    members: 'Members'
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
    name: 'Project Name'
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
    fetchMemberDetail: 'Failed to fetch member details'
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
      normal: 'Normal',
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
      // Form Options
      memberTypes: {
        teacher: 'Teacher',
        student: 'Student',
        alumni: 'Alumni'
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
      }
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
      fetchError: 'Failed to fetch members',
      deleteConfirmText: 'Are you sure you want to delete this member? This action cannot be undone.',
      deleteSuccess: 'Member deleted successfully',
      deleteError: 'Failed to delete member',
      // QuickActionModal related
      form: {
        nameZh: 'Chinese Name',
        nameEn: 'English Name',
        email: 'Email',
        type: 'Member Type',
        group: 'Research Group',
        description: 'Description',
        avatar: 'Avatar Upload',
        placeholders: {
          nameZh: 'Enter Chinese name',
          nameEn: 'Enter English name',
          email: 'Enter email address',
          type: 'Select member type',
          group: 'Select research group',
          description: 'Enter member description (supports Markdown syntax)'
        },
        validation: {
          nameZhRequired: 'Chinese name is required',
          nameEnRequired: 'English name is required',
          emailRequired: 'Email is required',
          typeRequired: 'Member type is required',
          groupRequired: 'Research group is required'
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
      form: {
        titleZh: 'Chinese Title',
        titleEn: 'English Title',
        description: 'Paper Description',
        venue: 'Journal/Conference',
        type: 'Paper Type',
        date: 'Publication Date',
        status: 'Acceptance Status',
        file: 'Paper File',
        placeholders: {
          titleZh: 'Enter paper Chinese title',
          titleEn: 'Enter paper English title',
          description: 'Enter paper Chinese description (supports Markdown syntax)',
          venue: 'Enter publication journal or conference',
          type: 'Select paper type',
          date: 'Select publication date',
          status: 'Select acceptance status'
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
      form: {
        nameZh: 'Chinese Name',
        nameEn: 'English Name',
        description: 'Project Description',
        url: 'Project URL',
        startDate: 'Start Date',
        status: 'Project Status',
        placeholders: {
          nameZh: 'Enter project Chinese name',
          nameEn: 'Enter project English name',
          description: 'Enter project description (supports Markdown syntax)',
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
      form: {
        type: 'News Type',
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
        editGroup: 'Edit Group'
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
        justNow: 'just now'
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
    }
  }
}