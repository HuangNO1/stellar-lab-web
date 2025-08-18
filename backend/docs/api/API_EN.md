<!-- Language Switcher -->

<div align="right">

[简体中文](API.md)

</div>

# Laboratory Web Framework API Documentation

## Table of Contents
- [Overview](#overview)
- [Authentication](#authentication)
- [General Response Format](#general-response-format)
- [Error Code Description](#error-code-description)
- [API Interfaces](#api-interfaces)
  - [Authentication Management](#authentication-management)
  - [Administrator Management](#administrator-management)
  - [Laboratory Management](#laboratory-management)
  - [Research Group Management](#research-group-management)
  - [Member Management](#member-management)
  - [Paper Management](#paper-management)
  - [News Management](#news-management)
  - [Project Management](#project-management)
  - [Media File Management](#media-file-management)
  - [Edit Record Management](#edit-record-management)
  - [System Interfaces](#system-interfaces)

## Overview

Laboratory Web Framework Backend API, developed based on Flask framework, providing complete functionality for laboratory information management.

- **Base URL**: `http://localhost:8000/api`
- **Content Type**: `application/json` (except file uploads)
- **Character Encoding**: UTF-8

## Authentication

Interfaces requiring authentication use JWT (JSON Web Token) for identity verification.

### Request Header Configuration
```
Authorization: Bearer <token>
Content-Type: application/json
Accept-Language: en  # or zh, specify language for response messages
X-Language: en       # custom language header, higher priority than Accept-Language
```

### Internationalization Support

The API supports bilingual response messages (Chinese and English). Language detection priority:
1. **X-Language** request header (`zh` | `en`)
2. **Accept-Language** request header
3. **Default Chinese** (`zh`)

**Frontend Integration Example**:
```javascript
// Automatically get language from user settings
const currentLanguage = Cookies.get('language') || 'zh';

axios.defaults.headers['Accept-Language'] = currentLanguage;
axios.defaults.headers['X-Language'] = currentLanguage;
```

**Supported Languages**:
- `zh`: Traditional Chinese (default)
- `en`: English

### Permission Levels
- **Regular Administrator**: `@admin_required`
- **Super Administrator**: `@super_admin_required`

## General Response Format

### Success Response
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    // Actual data
  }
}
```

### Error Response
```json
{
  "code": 2000,
  "message": "Parameter error",
  "data": null
}
```

**Internationalized Error Message Examples**:

Chinese request (`X-Language: zh`):
```json
{
  "code": 3000,
  "message": "成員不存在",
  "data": null
}
```

English request (`X-Language: en`):
```json
{
  "code": 3000,
  "message": "Member not found",
  "data": null
}
```

### Pagination Query Description

**Pagination Parameters**
- `page`: Page number, starting from 1
- `per_page`: Items per page, default 10, maximum 100
- `all`: When set to `true`, ignores pagination parameters and returns all data

**Parameter Priority Strategy**

When multiple parameters exist simultaneously, follow this priority order:

1. **`all=true`** - Highest priority, returns all data
2. **`all=false` or unset** - Uses standard pagination logic
3. **`page` and `per_page`** - Effective in pagination mode

**Parameter Combination Behavior Table**

| Parameter Combination | Actual Behavior | Description |
|----------------------|----------------|-------------|
| `?all=true` | Returns all data | Ignores other parameters |
| `?all=true&page=2&per_page=5` | Returns all data | `all=true` takes priority, ignores pagination parameters |
| `?all=false&page=2&per_page=5` | Returns page 2, 5 items per page | Uses specified pagination parameters |
| `?page=2&per_page=5` | Returns page 2, 5 items per page | Default pagination mode |
| `?all=false` | Returns page 1, 10 items per page | Uses default pagination parameters |
| No parameters | Returns page 1, 10 items per page | Uses default pagination parameters |

**Usage Examples**
```bash
# Standard paginated query
GET /api/members?page=1&per_page=20

# Get all data (recommended)
GET /api/members?all=true

# Mixed parameters (all=true takes effect, ignores pagination parameters)
GET /api/members?all=true&page=2&per_page=5
# Result: Returns all data

# Explicitly disable all parameter
GET /api/members?all=false&page=2&per_page=5
# Result: Returns page 2, 5 items per page
```

### Pagination Response Format

**Standard Pagination Response**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "items": [
      // Data list
    ],
    "total": 100,
    "page": 1,
    "per_page": 10,
    "pages": 10,
    "has_prev": false,
    "has_next": true
  }
}
```

**Get All Data Response** (when `all=true`)
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "items": [
      // All data list
    ],
    "total": 100,
    "all": true
  }
}
```

## Error Code Description

| Error Code | Description | HTTP Status Code | I18n Support |
|-----------|-------------|------------------|--------------|
| 0 | Success | 200 | ✅ |
| 1000 | Authentication error (wrong username/password) | 401 | ✅ |
| 1001 | Insufficient permissions | 403 | ✅ |
| 2000 | Parameter validation error | 400 | ✅ |
| 3000 | Resource not found | 404 | ✅ |
| 4000 | Operation conflict | 409 | ✅ |
| 5000 | Internal server error | 500 | ✅ |

**Internationalized Error Message Types**:
- **Success Messages**: Created successfully, Updated successfully, Deleted successfully, etc.
- **Validation Errors**: Invalid parameter format, Missing required fields, etc.
- **Business Logic Errors**: Association constraints, Permission restrictions, etc.
- **System Errors**: Service unavailable, Internal processing exceptions, etc.

All error messages are automatically returned in Chinese or English based on request language.

## API Interfaces

## Authentication Management

### Administrator Login
```
POST /api/admin/login
```

**Request Headers**
```
Content-Type: application/json
```

**Request Parameters**
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| admin_name | string | ✓ | Administrator username | admin |
| admin_pass | string | ✓ | Administrator password | admin123 |

**Request Example**
```json
{
  "admin_name": "admin",
  "admin_pass": "admin123"
}
```

**Response Parameters**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| access_token | string | JWT token, format: Bearer {token} | Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9... |
| expires_in | integer | Token validity period (seconds) | 86400 |
| admin | object | Administrator information object | See example below |

**Response Example**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "access_token": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "expires_in": 86400,
    "admin": {
      "admin_id": 1,
      "admin_name": "admin",
      "is_super": 1,
      "enable": 1,
      "created_at": "2024-01-01T00:00:00"
    }
  }
}
```

### Administrator Logout
```
POST /api/admin/logout
```

**Request Headers**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Parameters**
None

**Response Example**
```json
{
  "code": 0,
  "message": "Logout successful"
}
```

### Change Password
```
POST /api/admin/change-password
```

**Request Headers**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Parameters**
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| old_password | string | ✓ | Current password | admin123 |
| new_password | string | ✓ | New password (at least 6 characters) | new_admin123 |

**Request Example**
```json
{
  "old_password": "admin123",
  "new_password": "new_admin123"
}
```

**Response Example**
```json
{
  "code": 0,
  "message": "Password changed successfully"
}
```

### Get Personal Information
```
GET /api/admin/profile
```

**Request Headers**
```
Authorization: Bearer <token>
```

**Query Parameters**
None

**Response Example**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "admin_id": 1,
    "admin_name": "admin",
    "is_super": 1,
    "enable": 1,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### Update Personal Information
```
PUT /api/admin/profile
```

**Request Headers**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Parameters**
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| admin_name | string | - | Administrator username (uniqueness will be checked) | new_admin |

**Request Example**
```json
{
  "admin_name": "super_admin"
}
```

**Response Example**
```json
{
  "code": 0,
  "message": "Personal information updated successfully",
  "data": {
    "admin_id": 1,
    "admin_name": "super_admin",
    "is_super": 1,
    "enable": 1,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2025-01-01T10:30:00"
  }
}
```

**Notes**
- Administrators can only modify their own personal information
- Username must be unique and cannot duplicate existing administrators
- Updated username takes effect immediately, new JWT token will contain updated username
- All modification operations are automatically recorded in operation logs

## Administrator Management

### Get Administrator List
```
GET /api/admins
```

**Request Headers**
```
Authorization: Bearer <token> (Super administrator permission required)
```

**Query Parameters**
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| q | string | - | Search keyword (username) | admin |
| show_all | boolean | - | Whether to show deleted (default false) | true |
| page | integer | - | Page number (default 1) | 1 |
| per_page | integer | - | Items per page (default 10, max 100) | 10 |
| all | string | - | Get all data (ignores pagination when set to 'true') | true |

**Response Example**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "items": [
      {
        "admin_id": 1,
        "admin_name": "admin",
        "is_super": 1,
        "enable": 1,
        "created_at": "2024-01-01T00:00:00"
      }
    ],
    "total": 1,
    "page": 1,
    "per_page": 10,
    "pages": 1,
    "has_prev": false,
    "has_next": false
  }
}
```

### Create Administrator
```
POST /api/admins
```

**Request Headers**
```
Authorization: Bearer <token> (Super administrator permission required)
Content-Type: application/json
```

**Request Parameters**
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| admin_name | string | ✓ | Administrator username | newadmin |
| admin_pass | string | ✓ | Administrator password | password123 |
| is_super | integer | - | Whether super administrator (0/1, default 0) | 0 |

**Request Example**
```json
{
  "admin_name": "newadmin",
  "admin_pass": "password123",
  "is_super": 0
}
```

### Reset Administrator Password
```
POST /api/admins/{admin_id}/reset-password
```

**Request Headers**
```
Authorization: Bearer <token> (Super administrator permission required)
Content-Type: application/json
```

**Path Parameters**
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| admin_id | integer | ✓ | Administrator ID to reset password | 2 |

**Request Parameters**
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| new_password | string | ✓ | New password (at least 6 characters) | newpass123 |

**Request Example**
```json
{
  "new_password": "newpass123"
}
```

**Response Example**
```json
{
  "code": 0,
  "message": "Administrator password reset successfully",
  "data": {
    "admin_id": 2,
    "message": "Password has been reset"
  }
}
```

## Laboratory Management

### Get Laboratory Information
```
GET /api/lab
```

**Request Headers**
No authentication required

**Query Parameters**
None

**Response Example**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "lab_id": 1,
    "lab_logo_path": "/media/lab_logo/logo.png",
    "carousel_img_1": "/media/lab_logo/carousel_1.jpg",
    "carousel_img_2": "/media/lab_logo/carousel_2.jpg",
    "carousel_img_3": "/media/lab_logo/carousel_3.jpg",
    "carousel_img_4": "/media/lab_logo/carousel_4.jpg",
    "lab_zh": "Intelligent Computing Laboratory",
    "lab_en": "Intelligent Computing Laboratory",
    "lab_desc_zh": "This laboratory focuses on research in artificial intelligence, machine learning, and computer vision",
    "lab_desc_en": "Our laboratory focuses on research in artificial intelligence, machine learning, and computer vision",
    "lab_address_zh": "FIT Building, Tsinghua University, Beijing",
    "lab_address_en": "FIT Building, Tsinghua University, Beijing",
    "lab_email": "contact@lab.tsinghua.edu.cn",
    "lab_phone": "+86-10-62785678",
    "enable": 1
  }
}
```

### Update Laboratory Information
```
PUT /api/lab
POST /api/lab
```

**Request Headers**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Parameters**
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| lab_zh | string | - | Laboratory Chinese name | Intelligent Computing Laboratory |
| lab_en | string | - | Laboratory English name | Intelligent Computing Laboratory |
| lab_desc_zh | string | - | Laboratory Chinese description | Focus on AI research |
| lab_desc_en | string | - | Laboratory English description | Focus on AI research |
| lab_address_zh | string | - | Laboratory Chinese address | Beijing, Haidian |
| lab_address_en | string | - | Laboratory English address | Beijing, Haidian |
| lab_email | string | - | Laboratory contact email | contact@lab.edu.cn |
| lab_phone | string | - | Laboratory contact phone | +86-10-12345678 |
| lab_logo | file | - | Laboratory logo file | logo.png |
| lab_logo_delete | string | - | Delete logo (delete when value is "true") | true |
| carousel_img_1 | file | - | Carousel image 1 | carousel1.jpg |
| carousel_img_2 | file | - | Carousel image 2 | carousel2.jpg |
| carousel_img_3 | file | - | Carousel image 3 | carousel3.jpg |
| carousel_img_4 | file | - | Carousel image 4 | carousel4.jpg |
| clear_carousel_img_1 | string | - | Clear carousel image 1 (clear when value is "true") | true |
| clear_carousel_img_2 | string | - | Clear carousel image 2 (clear when value is "true") | true |
| clear_carousel_img_3 | string | - | Clear carousel image 3 (clear when value is "true") | true |
| clear_carousel_img_4 | string | - | Clear carousel image 4 (clear when value is "true") | true |

## Member Management

### Get Member List
```
GET /api/members
```

**Request Headers**
No authentication required

**Query Parameters**
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| q | string | - | Search keyword (name, email) | Professor Zhang |
| type | integer | - | Member type (0=Teacher, 1=Student, 2=Alumni) | 0 |
| research_group_id | integer | - | Research group ID filter | 1 |
| lab_id | integer | - | Laboratory ID filter | 1 |
| show_all | boolean | - | Whether to show deleted | false |
| sort_by | string | - | Sort field (name/type/created_at) | name |
| order | string | - | Sort order (asc/desc) | asc |
| page | integer | - | Page number | 1 |
| per_page | integer | - | Items per page | 10 |
| all | string | - | Get all data (ignores pagination when set to 'true') | true |

**Response Example**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "items": [
      {
        "mem_id": 1,
        "mem_avatar_path": "/media/member_avatar/avatar_001.jpg",
        "mem_name_zh": "Professor Li",
        "mem_name_en": "Prof. Li",
        "mem_desc_zh": "Focus on machine learning research",
        "mem_desc_en": "Focus on machine learning research",
        "mem_email": "li@lab.edu.cn",
        "mem_type": 0,
        "job_type": 0,
        "student_type": null,
        "student_grade": null,
        "destination_zh": "Tsinghua University",
        "destination_en": "Tsinghua University",
        "research_group_id": 1,
        "lab_id": 1,
        "enable": 1,
        "created_at": "2024-01-01T00:00:00"
      }
    ],
    "total": 1,
    "page": 1,
    "per_page": 10,
    "pages": 1,
    "has_prev": false,
    "has_next": false
  }
}
```

### Create Member
```
POST /api/members
```

**Request Headers**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Parameters**
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| mem_name_zh | string | ✓ | Member Chinese name | Professor Li |
| mem_name_en | string | ✓ | Member English name | Prof. Li |
| mem_email | string | ✓ | Email address | li@lab.edu.cn |
| mem_type | integer | ✓ | Member type (0=Teacher, 1=Student, 2=Alumni) | 0 |
| job_type | integer | - | Job type (Teacher: 0=Professor, 1=Associate Professor, 2=Lecturer, 3=Assistant Researcher, 4=Postdoc) | 0 |
| student_type | integer | - | Student type (Student: 0=PhD, 1=Master, 2=Undergraduate) | 0 |
| student_grade | integer | - | Student grade | 1 |
| research_group_id | integer | - | Research group ID (can be null for "None") | 1 |
| mem_desc_zh | string | - | Member Chinese description | Focus on machine learning research |
| mem_desc_en | string | - | Member English description | Focus on ML research |
| destination_zh | string | - | Destination Chinese | Tsinghua University |
| destination_en | string | - | Destination English | Tsinghua University |
| mem_avatar | file | - | Avatar file | avatar.jpg |
| mem_avatar_delete | string | - | Delete avatar (delete when value is "true") | true |

**Note**: The `research_group_id` field can now accept null values or be omitted entirely to represent "None" (no research group assignment). This applies to all member types - teachers, students, and alumni can all have no research group assignment.

## System Interfaces

### Health Check
```
GET /api/health
```

**Request Headers**
No authentication required

**Query Parameters**
None

**Response Example**
```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "status": "healthy",
    "timestamp": "2024-01-01T00:00:00",
    "version": "1.0.0"
  }
}
```

### API Information
```
GET /api/api-info
```

**Request Headers**
No authentication required

**Query Parameters**
None

Returns API information page (HTML)

### Swagger Documentation
```
GET /api/docs
```

**Request Headers**
No authentication required

**Query Parameters**
None

Returns Swagger UI page

### API Specification
```
GET /api/swagger.json
```

**Request Headers**
No authentication required

**Query Parameters**
None

Returns OpenAPI specification JSON

## Appendix

### Data Type Description

**Member Type (mem_type)**
- 0: Teacher
- 1: Student  
- 2: Alumni

**Job Type (job_type)** - Teachers only
- 0: Professor
- 1: Associate Professor
- 2: Lecturer
- 3: Assistant Researcher
- 4: Postdoc

**Student Type (student_type)** - Students only
- 0: PhD Student
- 1: Master Student
- 2: Undergraduate

**Paper Type (paper_type)**
- 0: Conference
- 1: Journal
- 2: Patent
- 3: Book
- 4: Other

**Paper Acceptance Status (paper_accept)**
- 0: Under Review
- 1: Accepted

**News Type (news_type)**
- 0: Paper Publication
- 1: Award News
- 2: Academic Activity

**Project Status (is_end)**
- 0: Ongoing
- 1: Completed

### Soft Delete Constraints

The system uses soft delete mechanism with the following constraints:

1. **Laboratory Deletion**: Must delete all research groups and members first
2. **Research Group Deletion**: Must delete or migrate all members first
3. **Member Deletion**: Cannot be research group leader and cannot have associated valid papers

### File Upload Description

**Supported File Types**
- Images: PNG, JPG, JPEG, GIF
- Documents: PDF

**File Size Limits**
- Paper files: Maximum 50MB
- Other files: Maximum 5MB

**Storage Paths**
- Laboratory Logo: `/media/lab_logo/`
- Carousel Images: `/media/lab_logo/` (same directory as Logo)
- Member Avatars: `/media/member_avatar/`
- Paper Files: `/media/paper/`
- Other Files: `/media/other/`