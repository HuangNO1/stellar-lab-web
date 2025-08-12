<!-- Language Switcher -->

<div align="right">

[简体中文](PYCHARM_TESTING_GUIDE.md)

</div>

# PyCharm Test Running Configuration Guide

## 📊 Test Case Statistics

Currently in the `tests/unit/services/` directory, the following test files have been created:

| Test File | Corresponding Service | Number of Test Cases | Coverage |
|-----------|----------------------|---------------------|----------|
| `test_auth_service.py` | AuthService | 8 | Login, password change, profile management |
| `test_admin_service.py` | AdminService | 10 | Admin CRUD, permission validation |
| `test_lab_service.py` | LabService | 10 | Lab info management, file upload |
| `test_member_service.py` | MemberService | 12 | Member management, batch operations |
| `test_research_group_service.py` | ResearchGroupService | 3 | Research group management |
| `test_paper_service.py` | PaperService | 4 | Paper management, PDF upload |
| `test_news_service.py` | NewsService | 3 | News publishing management |
| `test_project_service.py` | ProjectService | 3 | Project management, status updates |
| `test_media_service.py` | MediaService | 6 | File upload, media services |
| `test_audit_service.py` | AuditService | 6 | Operation audit, statistical analysis |
| `test_base_service.py` | BaseService | 12 | Base service, transaction management |
| `test_service_template.py` | LabService | Template example | Test template reference |

**Total**: 12 test files, 80+ test cases

## 🔧 PyCharm Batch Test Running Configuration

### Method 1: Using PyCharm's Built-in Test Runner (Recommended)

#### 1.1 Running Entire Test Directory

1. **Right-click on test directory**:
   - Right-click on `tests/unit/services/` folder in project browser
   - Select `Run 'Python tests in services'`

2. **Using top toolbar**:
   - Click `Run` menu in PyCharm top bar
   - Select `Run...` or press `Ctrl+Shift+F10`
   - Choose `Python tests in services`

#### 1.2 Running Specific Test Files

1. **Single file**:
   - Right-click on test file (e.g., `test_auth_service.py`)
   - Select `Run 'Python tests in test_auth_service.py'`

2. **Multiple files**:
   - Hold `Ctrl` and select multiple test files
   - Right-click and select `Run 'Python tests in ...'`

#### 1.3 Running Specific Test Classes or Methods

1. **Running test class**:
   - Open test file, click green arrow next to class name
   - Or right-click on class name, select `Run 'TestAuthService'`

2. **Running single test method**:
   - Click green arrow next to test method
   - Or place cursor in method and press `Ctrl+Shift+F10`

### Method 2: Creating Custom Run Configurations

#### 2.1 Creating pytest Configuration

1. **Open run configurations**:
   - Click `Run` > `Edit Configurations...`
   - Click `+` > `Python tests` > `pytest`

2. **Configure parameters**:
   ```
   Name: Service Layer Tests
   Target: Custom
   Target Path: tests/unit/services
   Working Directory: /home/rem/Documents/Study/Code/lab_web/backend
   Environment Variables: PYTHONPATH=/home/rem/Documents/Study/Code/lab_web/backend
   Python Interpreter: Select project's virtual environment
   ```

3. **Add pytest options**:
   ```
   Additional Arguments: -v --tb=short --maxfail=5
   ```

#### 2.2 Creating Marker Run Configurations

1. **Run service layer tests only**:
   ```
   Name: Service Tests Only
   Target: Custom
   Additional Arguments: -m service -v
   ```

2. **Run unit tests only**:
   ```
   Name: Unit Tests Only
   Target: Custom  
   Additional Arguments: -m unit -v
   ```

3. **Retry failed tests**:
   ```
   Name: Failed Tests Retry
   Target: Custom
   Additional Arguments: --lf -v
   ```

### Method 3: Using Terminal Commands

If PyCharm's GUI has issues, you can use the built-in terminal:

1. **Open PyCharm terminal** (`Alt+F12`)
2. **Run the following commands**:

```bash
# Run all service layer tests
pytest tests/unit/services/ -v

# Run specific test file
pytest tests/unit/services/test_auth_service.py -v

# Run tests with markers
pytest -m service -v
pytest -m unit -v

# Run tests and generate coverage report
pytest tests/unit/services/ --cov=app/services --cov-report=html -v

# Run tests with detailed output
pytest tests/unit/services/ -v -s

# Run tests in parallel (requires pytest-xdist)
pip install pytest-xdist
pytest tests/unit/services/ -n auto -v
```

## 🎯 Test Running Options Explained

### Common pytest Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `-v` | Verbose output | `pytest -v` |
| `-s` | Show print output | `pytest -s` |
| `-x` | Stop at first failure | `pytest -x` |
| `--maxfail=n` | Stop after n failures | `pytest --maxfail=3` |
| `-k pattern` | Run tests matching pattern | `pytest -k "auth or admin"` |
| `-m marker` | Run tests with specific marker | `pytest -m service` |
| `--lf` | Run only last failed tests | `pytest --lf` |
| `--tb=style` | Traceback style | `pytest --tb=short` |

### Coverage Testing Options

```bash
# Basic coverage
pytest --cov=app/services tests/unit/services/

# HTML coverage report
pytest --cov=app/services --cov-report=html tests/unit/services/

# Show uncovered lines
pytest --cov=app/services --cov-report=term-missing tests/unit/services/

# Coverage threshold check
pytest --cov=app/services --cov-fail-under=80 tests/unit/services/
```

## 🔍 Debugging Test Cases

### Debugging in PyCharm

1. **Set breakpoints**:
   - Click left side of line numbers to set breakpoints
   - Or press `Ctrl+F8`

2. **Debug run**:
   - Right-click on test, select `Debug 'test_name'`
   - Or click green bug icon next to test method

3. **Debug tools**:
   - `F8`: Step over
   - `F7`: Step into
   - `Shift+F8`: Step out
   - `F9`: Continue execution

### Viewing Test Output

1. **Test results window**:
   - PyCharm bottom shows `Run` or `Debug` window
   - Shows test execution status, pass/fail counts

2. **Error details**:
   - Click on failed test to view error details
   - Can directly jump to failing code line

## ⚙️ Test Environment Configuration

### 1. Ensure Dependencies Installed

```bash
pip install pytest pytest-cov pytest-mock pytest-xdist
```

### 2. Environment Variables Setup

Add in PyCharm run configuration:
```
FLASK_ENV=testing
FLASK_CONFIG=testing  
PYTHONPATH=/home/rem/Documents/Study/Code/lab_web/backend
```

### 3. Database Configuration

Tests use in-memory database, configured in `tests/conftest.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
```

## 📈 Continuous Integration Recommendations

### GitHub Actions Configuration

Add to `.github/workflows/tests.yml`:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run service tests
        run: |
          pytest tests/unit/services/ -v --cov=app/services
```

## 🎉 Quick Start

1. **Ensure PyCharm recognizes test directory**:
   - Right-click on `tests` folder
   - Select `Mark Directory as` > `Test Sources Root`

2. **Run first test**:
   - Open `test_auth_service.py`
   - Click green arrow next to `TestAuthService` class
   - View test results

3. **Batch run all service tests**:
   - Right-click on `tests/unit/services` folder
   - Select `Run 'Python tests in services'`
   - Wait for all 80+ test cases to complete

Now you can efficiently run and manage all service layer test cases using PyCharm!