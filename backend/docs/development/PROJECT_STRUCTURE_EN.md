<!-- Language Switcher -->

<div align="right">

[简体中文](PROJECT_STRUCTURE.md)

</div>

# Project Structure Description

## 📁 Organized Directory Structure

```
backend/
├── app/                          # Main application directory
│   ├── __init__.py              # Flask application factory
│   ├── models/                  # Data model layer (ORM)
│   │   ├── __init__.py
│   │   ├── admin.py            # Administrator model
│   │   ├── lab.py              # Laboratory model
│   │   ├── member.py           # Member model
│   │   ├── paper.py            # Paper model
│   │   ├── news.py             # News model
│   │   ├── project.py          # Project model
│   │   ├── research_group.py   # Research group model
│   │   └── edit_record.py      # Edit record model
│   ├── routes/                  # API route layer
│   │   ├── admin.py            # Administrator routes
│   │   ├── auth.py             # Authentication routes
│   │   ├── lab.py              # Laboratory routes
│   │   ├── member.py           # Member routes
│   │   ├── paper.py            # Paper routes
│   │   ├── news.py             # News routes
│   │   ├── project.py          # Project routes
│   │   ├── research_group.py   # Research group routes
│   │   ├── media.py            # Media file routes
│   │   ├── edit_record.py      # Edit record routes
│   │   ├── root.py             # Root routes
│   │   └── swagger_simple.py   # Automated Swagger documentation
│   ├── services/                # Business logic layer ⭐
│   │   ├── __init__.py
│   │   ├── base_service.py     # Base service class
│   │   ├── admin_service.py    # Administrator service
│   │   ├── auth_service.py     # Authentication service
│   │   ├── lab_service.py      # Laboratory service
│   │   ├── member_service.py   # Member service
│   │   ├── paper_service.py    # Paper service
│   │   ├── news_service.py     # News service
│   │   ├── project_service.py  # Project service
│   │   ├── research_group_service.py # Research group service
│   │   ├── media_service.py    # Media service
│   │   └── audit_service.py    # Audit service
│   ├── auth/                    # Authentication related
│   │   ├── __init__.py
│   │   └── decorators.py       # Authentication decorators
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py
│   │   ├── helpers.py          # General helper functions
│   │   ├── validators.py       # Data validators
│   │   ├── file_handler.py     # File processing tools
│   │   └── messages.py         # Unified message management
│   └── static/                  # Static files
├── config/                      # Configuration files
│   └── config.py               # Application configuration
├── scripts/                     # Scripts directory
│   ├── deployment/             # Deployment scripts
│   │   ├── deploy.sh          # Deployment script
│   │   ├── start.sh           # Startup script
│   │   └── docker-entrypoint.sh # Docker entry script
│   ├── development/            # Development scripts
│   │   └── init_db.py         # Database initialization
│   └── maintenance/            # Maintenance scripts
│       └── diagnose.sh        # Diagnostic script
├── tests/                      # Testing directory ⭐
│   ├── conftest.py            # pytest configuration
│   ├── unit/                  # Unit tests
│   │   ├── services/          # Service layer tests ⭐
│   │   │   └── test_service_template.py # Service test template
│   │   ├── models/            # Model tests
│   │   └── utils/             # Utility function tests
│   ├── integration/           # Integration tests
│   │   └── test_api.py       # API integration tests
│   └── fixtures/              # Test data
│       ├── data_fixtures.py  # Business data fixtures
│       └── user_fixtures.py  # User authentication fixtures
├── docs/                      # Documentation directory
│   ├── api/                   # API documentation
│   ├── deployment/            # Deployment documentation
│   │   └── DOCKER_DEPLOY.md  # Docker deployment guide
│   ├── development/           # Development documentation
│   └── migration/             # Migration documentation
│       └── SWAGGER_MIGRATION_GUIDE.md # Swagger migration guide
├── migrations/                # Database migrations
├── logs/                      # Log directory
├── media/                     # Media files directory
├── requirements.txt           # Python dependencies
├── run.py                     # Application entry point
├── README.md                  # Project description
├── .env.example              # Environment variables example
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose configuration
└── docker-compose-minimal.yml # Minimal Docker Compose
```

## 🎯 Organization Results

### ✅ Cleaned Files
- **Temporary demo files**: `demo_swagger_automation.py`, `test_basic.py`, `test_swagger_automation.py` etc.
- **Migration analysis files**: `MIGRATION_ANALYSIS.py`, `MIGRATION_SUCCESS_REPORT.py` etc.
- **Backup files**: `app/__init__.py.backup`, `swagger_docs.py.backup`
- **Redundant Swagger files**: Keep `swagger_simple.py`, clean other redundant files
- **Temporary notes**: `think/` directory

### 📁 New Directory Structure
- **`scripts/`**: Scripts categorized by function (deployment, maintenance, development)
- **`tests/unit/services/`**: Dedicated to service layer unit tests ⭐
- **`tests/integration/`**: Integration tests
- **`tests/fixtures/`**: Test data
- **`docs/`**: Documentation organized by category

### 🧪 Test Environment Preparation
- **`tests/conftest.py`**: pytest configuration including app, database fixtures
- **`tests/unit/services/test_service_template.py`**: Service layer test template
- **`tests/fixtures/data_fixtures.py`**: Business data test fixtures
- **`tests/fixtures/user_fixtures.py`**: User authentication test fixtures

## 🚀 Usage Guide

### Running Tests
```bash
# Run all tests
pytest

# Run service layer tests
pytest tests/unit/services/ -v

# Run tests with specific markers
pytest -m service  # Service layer tests
pytest -m unit     # Unit tests
pytest -m integration  # Integration tests

# Generate coverage report
pytest --cov=app
```

### Developing New Features
1. **Add Model**: Add data model in `app/models/`
2. **Implement Service Layer**: Implement business logic in `app/services/`
3. **Add Routes**: Add API endpoints in `app/routes/`
4. **Write Tests**: Add service layer tests in `tests/unit/services/`

### Deploying Project
```bash
# Development environment
./scripts/development/init_db.py

# Production deployment
./scripts/deployment/deploy.sh

# Diagnose issues
./scripts/maintenance/diagnose.sh
```

## ✨ Project Advantages

- 🎯 **Clear layered architecture**: Routes → Services → Models
- 🧪 **Complete test structure**: Dedicated service layer test directory
- 📚 **Standardized documentation organization**: Documentation structure categorized by type
- 🛠️ **Clean script management**: Script directory categorized by function
- ⚡ **Zero-maintenance API documentation**: Automated Swagger system
- 🚀 **Excellent maintainability**: Each component has clear responsibilities