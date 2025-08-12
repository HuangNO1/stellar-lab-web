<!-- Language Switcher -->

<div align="right">

[简体中文](README_zh-CN.md)

</div>

<!-- Header -->

<div align="center">

<img src="frontend/src/assets/logo.png" width="128"/>

# Lab Website Framework

A modern, universal laboratory website framework with content management system.

<!-- Shields/Badges -->

<p>
<a href="https://vuejs.org/"><img alt="Vue.js" src="https://img.shields.io/badge/Frontend-Vue%203-4FC08D?style=for-the-badge&logo=vue.js"></a>
<a href="https://flask.palletsprojects.com/"><img alt="Flask" src="https://img.shields.io/badge/Backend-Flask-000000?style=for-the-badge&logo=flask"></a>
<a href="https://www.mysql.com/"><img alt="MySQL" src="https://img.shields.io/badge/Database-MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white"></a>
<a href="https://www.docker.com/"><img alt="Docker" src="https://img.shields.io/badge/Deploy-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"></a>
<br/>
<img alt="License" src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">
<img alt="Status" src="https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge">
</p>

</div>

## ✨ Introduction

This laboratory website framework was born out of frustration with existing solutions. Many labs rely on static GitHub Pages that are cumbersome to update and lack proper content management capabilities. Our framework addresses these pain points by providing a modern, feature-rich solution that any laboratory can easily adopt and customize.

Built with Vue 3 and Flask, this framework offers a complete laboratory website solution with both public-facing pages and a comprehensive admin dashboard. It's designed to be universal - allowing easy customization of school logos, laboratory information, and branding to suit different institutions.

## 🎯 Key Features

### 🌐 Public Website
- **Dynamic Homepage**: Customizable laboratory introduction with carousel images and latest news
- **Member Showcase**: Organized display of faculty, students, and alumni with detailed profiles
- **Research Groups**: Showcase different research teams with their focuses and members
- **Publications**: Complete paper management with search, filtering, and author linking
- **Projects**: Display ongoing and completed research projects
- **News & Updates**: Latest laboratory achievements, awards, and announcements
- **🌍 Internationalization**: Complete Chinese/English interface switching with localized content
- **🎨 Theme Support**: Light/Dark mode toggle throughout all pages for enhanced user experience
- **📱 Responsive Design**: Perfect display across desktop, tablet, and mobile devices

### 🛠️ Content Management System
- **📊 Dashboard**: Comprehensive overview with statistics and quick actions (supports theme switching)
- **Laboratory Management**: Basic info, contact details, logo, and carousel image management
- **Member Management**: Complete CRUD operations with avatar cropping and research group assignment
- **Research Group Management**: Team organization with leader assignment and descriptions
- **Publication Management**: Paper records with Markdown content editing and file uploads
- **Project Management**: Research project tracking with status management
- **News Management**: News publishing with categorization and content editing
- **👥 Admin Management**: Multi-level administrator accounts with permission control
- **📝 Operation Logs**: Complete audit trail of all system changes with detailed tracking
- **📁 Media Management**: Centralized file upload and storage system
- **🌐 Multi-language Admin**: Full internationalization support in admin interface

### 🔧 Technical Excellence
- **Modern Architecture**: Vue 3 + TypeScript frontend, Python Flask backend
- **Security First**: JWT authentication, bcrypt encryption, XSS protection, CSRF prevention
- **Performance Optimized**: Database indexing, pagination, caching, and query optimization
- **Docker Ready**: Complete containerization with one-click deployment
- **Developer Friendly**: Comprehensive API documentation, testing framework, and clear code structure

## 🎨 Interface Preview

### 🌟 Key Highlights
- **🌐 International Support**: Complete Chinese/English interface switching
- **🎨 Theme Switching**: Light/Dark mode toggle for better user experience  
- **📱 Responsive Design**: Seamless experience across all devices
- **⚡ Modern UI**: Clean, professional design with intuitive navigation

### 🏠 Public Website Interface

#### Homepage & Core Features
<div align="center">
<img src="preview/en/home.png" width="100%" alt="Homepage - Laboratory Introduction"/>
<p><em>Laboratory homepage with customizable introduction and latest updates</em></p>
</div>

#### Member & Research Showcase
<div align="center">
<table>
<tr>
<td width="50%"><img src="preview/en/member.png" width="100%" alt="Member Directory"/></td>
<td width="50%"><img src="preview/en/memberDetail.png" width="100%" alt="Member Profile"/></td>
</tr>
<tr>
<td align="center"><em>Member directory with organized display</em></td>
<td align="center"><em>Detailed member profiles with research info</em></td>
</tr>
</table>
</div>

#### Publications & Projects
<div align="center">
<table>
<tr>
<td width="50%"><img src="preview/en/paper.png" width="100%" alt="Publications List"/></td>
<td width="50%"><img src="preview/en/project.png" width="100%" alt="Projects Overview"/></td>
</tr>
<tr>
<td align="center"><em>Publication management with search & filtering</em></td>
<td align="center"><em>Research projects with status tracking</em></td>
</tr>
</table>
</div>

#### News & Updates
<div align="center">
<table>
<tr>
<td width="50%"><img src="preview/en/news.png" width="100%" alt="News List"/></td>
<td width="50%"><img src="preview/en/newsDetail.png" width="100%" alt="News Detail"/></td>
</tr>
<tr>
<td align="center"><em>Laboratory news and announcements</em></td>
<td align="center"><em>Detailed news content with rich text</em></td>
</tr>
</table>
</div>

### 🛠️ Admin Dashboard Interface

#### Dashboard Overview & Theme Switching
<div align="center">
<table>
<tr>
<td width="50%"><img src="preview/en/admin_dashboard.png" width="100%" alt="Admin Dashboard Light"/></td>
<td width="50%"><img src="preview/en/admin_dashboard_dark_theme.png" width="100%" alt="Admin Dashboard Dark"/></td>
</tr>
<tr>
<td align="center"><em>Admin dashboard - Light theme</em></td>
<td align="center"><em>Admin dashboard - Dark theme</em></td>
</tr>
</table>
</div>

#### Management Interfaces
<div align="center">
<table>
<tr>
<td width="33%"><img src="preview/en/admin_memberManage.png" width="100%" alt="Member Management"/></td>
<td width="33%"><img src="preview/en/admin_labManage.png" width="100%" alt="Lab Management"/></td>
<td width="33%"><img src="preview/en/admin_adminManage.png" width="100%" alt="Admin Management"/></td>
</tr>
<tr>
<td align="center"><em>Member management with CRUD operations</em></td>
<td align="center"><em>Laboratory information management</em></td>
<td align="center"><em>Administrator account management</em></td>
</tr>
</table>
</div>

#### System Monitoring
<div align="center">
<img src="preview/en/admin_operationLogs.png" width="70%" alt="Operation Logs"/>
<p><em>Comprehensive operation logs for system auditing</em></p>
</div>

## 🚀 Quick Start

### Option 1: Docker Deployment (Recommended)

```bash
# Clone the repository
git clone [your-repo-url]
cd lab_web

# Start all services with Docker Compose
docker-compose up -d --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Admin Panel: http://localhost:3000/admin
```

### Option 2: Manual Setup

```bash
# Backend setup
cd backend
pip install -r requirements.txt
python run.py

# Frontend setup (new terminal)
cd frontend
npm install
npm run serve
```

## 📊 System Overview

### Architecture
- **Frontend**: Vue 3 + TypeScript + Naive UI + Vue Router + Pinia
- **Backend**: Python + Flask + SQLAlchemy + JWT + MySQL
- **Database**: MySQL with complete relational design
- **Deployment**: Docker + Docker Compose + Nginx
- **Storage**: Local filesystem with organized media management

### Default Credentials
- **Admin Username**: `admin`
- **Admin Password**: `admin123`
- **Database**: Automatically initialized with sample data

⚠️ **Important**: Change the default password immediately in production!

## 💡 Use Cases

### Perfect for:
- **Academic Laboratories**: Research groups in universities and institutes
- **Corporate R&D Teams**: Company research and development divisions
- **Medical Labs**: Hospital and clinical research laboratories
- **Government Research**: Public sector research institutions
- **Startup Labs**: Emerging technology companies and incubators

### Migration from GitHub Pages
This framework is specifically designed for laboratories currently using GitHub Pages who want:
- **Easy Content Updates**: No more manual HTML/Markdown editing
- **Dynamic Content**: Real-time updates without rebuilding
- **Rich Media Support**: Image uploads, PDF papers, member photos
- **Search Functionality**: Find papers, members, and projects easily
- **Admin Controls**: Multiple administrators with different permission levels

## 📁 Project Structure

```
lab_web/
├── frontend/          # Vue 3 Frontend Application
│   ├── src/          # Source code
│   ├── public/       # Static assets
│   └── dist/         # Built files
├── backend/           # Flask Backend Application  
│   ├── app/          # Application code
│   ├── docs/         # API documentation
│   ├── scripts/      # Deployment & maintenance scripts
│   └── tests/        # Test suites
├── docs/             # Project documentation
├── docker-compose.yml # Full-stack deployment
└── deploy/           # Deployment scripts
```

For detailed technical information, refer to:
- Frontend: [frontend/README.md](frontend/README.md)
- Backend: [backend/README.md](backend/README.md)
- Deployment: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## 🔐 Security Features

- **Enterprise-grade Authentication**: JWT tokens with secure expiration
- **Multi-level Authorization**: Super admin and regular admin roles
- **Complete Audit Trail**: All operations logged with timestamp and user
- **XSS/CSRF Protection**: Modern web security implementations
- **Secure File Uploads**: Type validation and size restrictions
- **Soft Delete System**: Data safety with recovery capabilities

## 🌐 Multilingual Support

Complete interface available in:
- **Chinese (Simplified)**: 简体中文界面
- **English**: Full English interface
- **Extensible**: Easy to add more languages

Content management supports bilingual editing for all text fields.

## 📱 Device Compatibility

- **Desktop**: Full-featured interface (1024px+)
- **Tablet**: Touch-optimized experience (768-1024px)
- **Mobile**: Mobile-first responsive design (<768px)
- **Cross-browser**: Compatible with modern browsers

## 🛠️ Customization

### Branding
- Upload your institution's logo
- Customize color schemes and themes
- Set laboratory name and contact information
- Add carousel images for homepage

### Content Structure
- Define research groups and their focuses
- Organize members by categories (faculty/students/alumni)
- Categorize publications by type and venue
- Manage project portfolios with timelines

## 📚 Documentation

- **[Deployment Guide](docs/DEPLOYMENT.md)**: Complete setup instructions
- **[API Documentation](backend/docs/api/)**: Full REST API reference
- **[User Manual](docs/USER_MANUAL.md)**: Admin panel usage guide
- **[Development Guide](docs/DEVELOPMENT.md)**: Contributing and customization

## 🤝 Contributing

We welcome contributions from the research community:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Support

For questions, issues, or feature requests:
- Open an [issue](../../issues) on GitHub
- Check our [documentation](docs/)
- Contact the development team

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Transform your laboratory's online presence today!**

*From static pages to dynamic, manageable content in minutes.*

</div>