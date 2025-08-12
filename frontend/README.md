# Lab Website Frontend

A Vue 3 + TypeScript-based laboratory management system frontend with multi-language support (Chinese/English), responsive design, and comprehensive admin dashboard functionality.

## 🚀 Tech Stack

- **Framework**: Vue 3 (Composition API)
- **Language**: TypeScript
- **UI Library**: Naive UI 2.42+
- **Router**: Vue Router 4
- **State Management**: Pinia (Primary) ~~+ Vuex~~ *(Vuex removed)*
- **Internationalization**: Vue I18n 9.14+
- **HTTP Client**: Axios 1.11+
- **Build Tool**: Vue CLI 5
- **Code Style**: ESLint + TypeScript ESLint
- **Image Processing**: vue-advanced-cropper 2.8+
- **Markdown Editor**: md-editor-v3 5.8+
- **Utilities**: js-cookie, highlight.js
- **Deployment**: Docker + Nginx

## 📦 Quick Start

### Requirements
- Node.js >= 16 (Tested with Node.js 20)
- Yarn or npm
- Backend service running (for API integration)

### Environment Configuration

The frontend uses environment-specific configurations:

#### Development Environment
```bash
# Uses .env.development by default
NODE_ENV=development
VUE_APP_API_BASE_URL=http://127.0.0.1:8000/api
```

#### Production Environment  
```bash
# Uses .env.production
NODE_ENV=production
VUE_APP_API_BASE_URL=/api  # Relative path for nginx proxy
```

#### Custom Local Configuration
Create `.env.local` for personal development settings:
```bash
# Custom API endpoint (overrides other files)
VUE_APP_API_BASE_URL=https://your-domain.com/api
```

**📋 See [Environment Configuration Guide](./ENVIRONMENT.md) for detailed setup instructions.**

### Install Dependencies
```bash
yarn install
# or
npm install
```

### Development Mode
```bash
yarn serve
# or
npm run serve
```
Access the application at http://localhost:8080

**Note**: Ensure the backend service is running at http://localhost:8000 for API connectivity.

### Build for Production
```bash
yarn build
# or
npm run build
```

### Lint and Fix Code
```bash
yarn lint
# or
npm run lint
```

## 📁 Project Structure

```
src/
├── assets/              # Static resources
│   ├── engineering.jpg  # Default carousel image
│   └── laptop.jpg      # Default carousel image
├── components/          # Shared components
│   ├── HelloWorld.vue  # Demo component
│   ├── ImageCropperModal.vue  # Image cropper modal
│   ├── MarkdownEditor.vue     # Markdown editor
│   ├── I18nMdEditor.vue       # I18n Markdown editor
│   ├── SearchComponent.vue    # Search component
│   ├── ProfileModal.vue       # Profile modal
│   ├── QuickActionModal.vue   # Quick action modal
│   └── JsonDetailModal.vue    # JSON detail modal
├── composables/         # Vue 3 composables
│   ├── useLab.ts       # Lab information related
│   ├── useMembers.ts   # Member management related
│   └── useResearchGroups.ts  # Research group related
├── guards/              # Route guards
├── layouts/             # Layout components
│   ├── AdminLayout.vue  # Admin dashboard layout
│   └── UserLayout.vue   # User frontend layout
├── locales/             # I18n files
│   ├── zh.ts           # Chinese
│   └── en.ts           # English
├── Model/               # Data models
├── router/              # Route configuration
├── services/            # Service layer
│   └── api.ts          # Unified API management
├── stores/              # Pinia state management
├── types/               # TypeScript type definitions
│   └── api.ts          # API-related types
├── utils/               # Utility functions
│   ├── media.ts        # Media file handling
│   └── text.ts         # Text processing
└── views/               # Page components
    ├── admin/           # Admin dashboard pages
    │   ├── DashboardView.vue      # Dashboard
    │   ├── LoginView.vue          # Login page
    │   ├── ProfileView.vue        # Profile
    │   ├── ChangePasswordView.vue # Change password
    │   ├── LabManageView.vue      # Lab management
    │   ├── MemberManageView.vue   # Member management
    │   ├── GroupManageView.vue    # Research group management
    │   ├── PaperManageView.vue    # Paper management
    │   ├── ProjectManageView.vue  # Project management
    │   ├── NewsManageView.vue     # News management
    │   ├── AdminManageView.vue    # Admin management
    │   ├── SystemManageView.vue   # System management
    │   └── OperationLogsView.vue  # Operation logs
    ├── HomeView.vue      # Homepage
    ├── MemberView.vue    # Member list
    ├── MemberDetailView.vue # Member details
    ├── GroupView.vue     # Research group details
    ├── PaperView.vue     # Paper list
    ├── PaperDetailView.vue # Paper details
    ├── ProjectView.vue   # Project list
    ├── ProjectDetailView.vue # Project details
    ├── NewsView.vue      # News list
    └── NewsDetailView.vue # News details
```

## 🔧 Core Features

### Frontend User Features
- 🏠 **Homepage**: Lab introduction, carousel display, latest updates
- 👥 **Member Management**: Member list, member details, research group categorization
- 📚 **Research Groups**: Group introduction, member list, research directions
- 📝 **Publications**: Paper list, detailed information, category filtering
- 🚀 **Projects**: Project showcase, tech stack, achievements
- 📢 **News & Updates**: Latest news, event announcements, awards
- 🌍 **Multi-language**: Chinese/English switching
- 📱 **Responsive Design**: Desktop, tablet, mobile support

### Admin Dashboard Features
- 🎛️ **Dashboard**: System overview, statistics, quick actions
- 🏢 **Lab Management**: Basic info, contact details, logo and carousel management
- 👨‍💼 **Member Management**: Member CRUD, avatar upload/crop, group assignment
- 🔬 **Research Group Management**: Group info, leader assignment, description editing
- 📄 **Paper Management**: Publication records, Markdown content editing
- 💼 **Project Management**: Project maintenance, tech stack, achievements
- 📰 **News Management**: News publishing, category management, content editing
- 🔐 **Permission Management**: Admin accounts, password changes, operation logs
- ⚙️ **System Management**: System configuration, data backup, log viewing

## 🎨 Key Features

### Image Processing System
- **Smart Cropping**: Image cropping based on vue-advanced-cropper
- **Multiple Format Support**: Avatar, logo, carousel with different size requirements
- **Live Preview**: Real-time cropping preview
- **Error Handling**: Automatic fallback for image loading failures

### Dynamic Website Configuration
- **Dynamic Title**: Auto-update page title based on lab settings
- **Dynamic Favicon**: Use lab logo as website icon
- **Smart Fallback**: Use defaults when no settings available, ensuring stability

### Markdown Editing System
- **Bilingual Editing**: Support simultaneous Chinese/English Markdown editing
- **Live Preview**: WYSIWYG editing experience
- **Syntax Highlighting**: Code block syntax highlighting
- **Rich Toolbar**: Comprehensive formatting tools

### Search & Filtering
- **Full-text Search**: Support searching members, papers, projects, etc.
- **Smart Filtering**: Multi-condition combined filtering
- **Real-time Results**: Instant search results display

## 🔧 Development Guide

### Route Structure
```
Frontend Routes:
├── / - Homepage
├── /members - Member list
├── /member/:id - Member details
├── /group/:id - Research group details
├── /papers - Paper list
├── /paper/:id - Paper details
├── /projects - Project list
├── /project/:id - Project details
├── /news - News list
└── /news/:id - News details

Admin Routes (require authentication):
├── /admin - Admin home (redirect to dashboard)
├── /admin/login - Login page
├── /admin/dashboard - Dashboard
├── /admin/profile - Profile
├── /admin/change-password - Change password
├── /admin/lab - Lab management
├── /admin/members - Member management
├── /admin/groups - Research group management
├── /admin/papers - Paper management
├── /admin/projects - Project management
├── /admin/news - News management
├── /admin/admins - Admin management
├── /admin/system - System management
└── /admin/logs - Operation logs
```

### State Management
The project uses Pinia for state management, main stores include:
- `auth.ts` - Authentication state
- Global state shared through provide/inject for lab info and theme settings

### Internationalization
Supports Chinese/English switching:
- Language files located in `src/locales/`
- Use `useI18n()` composable to get translation methods
- Use `{{ $t('key') }}` in templates for translation
- Supports dynamic language switching without page reload

### Composables
- `useLab.ts` - Lab information related, provides auto-fetch functionality
- `useMembers.ts` - Member management related, supports search and filtering
- `useResearchGroups.ts` - Research group related, includes auto-fetch and management

### API Services
- API services are unified in `src/services/api.ts`
- Uses Axios for HTTP requests
- Supports request/response interceptors for authentication and error handling
- Unified error handling and message notifications

## 🎨 UI Component Library

Using Naive UI as the main UI library:
- Global `n-message-provider` configured in `App.vue`
- Can directly use `useMessage()` hook for notifications
- Supports dark theme switching
- Responsive design, adapts to various devices

### Common Components
- `n-form` / `n-form-item` - Form components
- `n-data-table` - Data table with pagination, sorting, filtering
- `n-button` - Button component
- `n-input` / `n-select` / `n-upload` - Input components
- `n-modal` / `n-drawer` - Modal components
- `n-message` / `n-notification` - Message notifications
- `n-card` - Card container
- `n-spin` - Loading indicator

## 🔒 Authentication

- Uses JWT Token for authentication
- Token stored in Cookies (using js-cookie)
- Route guards protect admin dashboard pages
- Auto-handles token expiration and refresh
- Unified login state management

## 📱 Responsive Design

The project adopts responsive design supporting multiple devices:
- **Desktop**: 1024px+, full feature display
- **Tablet**: 768px - 1024px, touch-optimized
- **Mobile**: <768px, mobile-optimized experience
- Uses CSS Grid and Flexbox for layouts
- Images and media content auto-scale

## 🛠️ Utility Functions

### Media Processing (`utils/media.ts`)
- `getMediaUrl()` - Get complete URL for media files
- `hasCarouselImages()` - Check if carousel images exist

### Text Processing (`utils/text.ts`)
- `stripMarkdown()` - Remove Markdown markup, get plain text

## 🐛 Common Issues & Solutions

### Naive UI useMessage Error
**Issue**: "No outer <n-message-provider /> founded" error  
**Solution**: Ensure `<n-message-provider>` is wrapped in `App.vue`, don't add duplicates in components

### Image Upload and Cropping Issues
**Issue**: Images can't display properly after cropping  
**Solution**: Check `ImageCropperModal` component usage, ensure correct crop type parameters

### Internationalization Content Not Displaying
**Issue**: Some content not updated after language switching  
**Solution**: Check if using `computed` properties or `watch` to listen for language changes, ensure reactive updates

### Route Guard Issues
**Issue**: Logged-in users cannot access admin dashboard  
**Solution**: Check if Token is correctly stored, verify route guard logic

### Development Server Proxy Configuration
For API proxy configuration, add to `vue.config.js`:
```javascript
module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api'
        }
      }
    }
  }
}
```

## 📊 Performance Optimization

### Implemented Optimizations
- **Lazy Loading**: Route components loaded on demand
- **Image Optimization**: Carousel and avatar image compression
- **Caching Strategy**: Common data like lab info cached
- **Code Splitting**: Admin dashboard and user frontend separation

### Recommended Optimizations
- Implement Service Worker for offline caching
- Use CDN for static resource acceleration
- Implement virtual scrolling for large data lists
- Add skeleton screens to improve loading experience

## 📄 License

This project is for internal use only.

## 🤝 Contributing

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Development Standards
- Follow TypeScript strict mode
- Use ESLint for code checking
- Use PascalCase for component naming
- Use kebab-case for file naming
- Commit messages in English, format: `type: description`

## 📞 Technical Support

For technical issues or suggestions, please contact the development team:
- Create Issue with detailed problem description
- Provide detailed error information and reproduction steps
- Specify browser and version information used

## 📈 Changelog

### v0.1.0 (Current Version)
- ✅ Completed basic framework setup
- ✅ Implemented complete frontend functionality
- ✅ Completed all admin dashboard modules
- ✅ Implemented image cropping and dynamic configuration
- ✅ Added multi-language support and responsive design
- ✅ Improved error handling and user experience

---

**[中文文档](./README_zh-CN.md) | English**