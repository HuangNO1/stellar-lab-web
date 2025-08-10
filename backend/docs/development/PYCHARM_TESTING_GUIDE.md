# PyCharm 測試運行配置指南

## 📊 測試用例統計

目前在 `tests/unit/services/` 目錄下已創建以下測試文件：

| 測試文件 | 對應服務 | 測試用例數量 | 覆蓋功能 |
|----------|----------|-------------|----------|
| `test_auth_service.py` | AuthService | 8個 | 登錄、密碼修改、個人信息管理 |
| `test_admin_service.py` | AdminService | 10個 | 管理員CRUD、權限驗證 |
| `test_lab_service.py` | LabService | 10個 | 實驗室信息管理、文件上傳 |
| `test_member_service.py` | MemberService | 12個 | 成員管理、批量操作 |
| `test_research_group_service.py` | ResearchGroupService | 3個 | 課題組管理 |
| `test_paper_service.py` | PaperService | 4個 | 論文管理、PDF上傳 |
| `test_news_service.py` | NewsService | 3個 | 新聞發布管理 |
| `test_project_service.py` | ProjectService | 3個 | 項目管理、狀態更新 |
| `test_media_service.py` | MediaService | 6個 | 文件上傳、媒體服務 |
| `test_audit_service.py` | AuditService | 6個 | 操作審計、統計分析 |
| `test_base_service.py` | BaseService | 12個 | 基礎服務、事務管理 |
| `test_service_template.py` | LabService | 示例模板 | 測試模板參考 |

**總計**: 12個測試文件，80+個測試用例

## 🔧 PyCharm 批量運行測試配置

### 方法1: 使用PyCharm的內建測試運行器 (推薦)

#### 1.1 運行整個測試目錄

1. **右鍵點擊測試目錄**:
   - 在項目瀏覽器中右鍵點擊 `tests/unit/services/` 文件夾
   - 選擇 `Run 'Python tests in services'`

2. **使用頂部工具欄**:
   - 點擊 PyCharm 頂部的 `Run` 菜單
   - 選擇 `Run...` 或按 `Ctrl+Shift+F10`
   - 選擇 `Python tests in services`

#### 1.2 運行特定測試文件

1. **單個文件**:
   - 右鍵點擊測試文件 (如 `test_auth_service.py`)
   - 選擇 `Run 'Python tests in test_auth_service.py'`

2. **多個文件**:
   - 按住 `Ctrl` 選中多個測試文件
   - 右鍵選擇 `Run 'Python tests in ...'`

#### 1.3 運行特定測試類或方法

1. **運行測試類**:
   - 打開測試文件，點擊類名旁的綠色箭頭
   - 或右鍵點擊類名，選擇 `Run 'TestAuthService'`

2. **運行單個測試方法**:
   - 點擊測試方法旁的綠色箭頭
   - 或將光標放在方法內，按 `Ctrl+Shift+F10`

### 方法2: 創建自定義運行配置

#### 2.1 創建pytest配置

1. **打開運行配置**:
   - 點擊 `Run` > `Edit Configurations...`
   - 點擊 `+` > `Python tests` > `pytest`

2. **配置參數**:
   ```
   Name: Service Layer Tests
   Target: Custom
   Target Path: tests/unit/services
   Working Directory: /home/rem/Documents/Study/Code/lab_web/backend
   Environment Variables: PYTHONPATH=/home/rem/Documents/Study/Code/lab_web/backend
   Python Interpreter: 選擇項目的虛擬環境
   ```

3. **添加pytest選項**:
   ```
   Additional Arguments: -v --tb=short --maxfail=5
   ```

#### 2.2 創建標記運行配置

1. **按服務層測試運行**:
   ```
   Name: Service Tests Only
   Target: Custom
   Additional Arguments: -m service -v
   ```

2. **按單元測試運行**:
   ```
   Name: Unit Tests Only
   Target: Custom  
   Additional Arguments: -m unit -v
   ```

3. **運行失敗重試**:
   ```
   Name: Failed Tests Retry
   Target: Custom
   Additional Arguments: --lf -v
   ```

### 方法3: 使用終端命令

如果PyCharm的圖形界面有問題，可以使用內建終端：

1. **打開PyCharm終端** (`Alt+F12`)
2. **運行以下命令**:

```bash
# 運行所有服務層測試
pytest tests/unit/services/ -v

# 運行特定測試文件
pytest tests/unit/services/test_auth_service.py -v

# 運行帶標記的測試
pytest -m service -v
pytest -m unit -v

# 運行測試並生成覆蓋率報告
pytest tests/unit/services/ --cov=app/services --cov-report=html -v

# 運行測試並顯示詳細輸出
pytest tests/unit/services/ -v -s

# 並行運行測試 (需要安裝 pytest-xdist)
pip install pytest-xdist
pytest tests/unit/services/ -n auto -v
```

## 🎯 測試運行選項說明

### 常用pytest參數

| 參數 | 作用 | 示例 |
|------|------|------|
| `-v` | 詳細輸出 | `pytest -v` |
| `-s` | 顯示print輸出 | `pytest -s` |
| `-x` | 遇到第一個失敗就停止 | `pytest -x` |
| `--maxfail=n` | 失敗n次後停止 | `pytest --maxfail=3` |
| `-k pattern` | 運行匹配模式的測試 | `pytest -k "auth or admin"` |
| `-m marker` | 運行帶特定標記的測試 | `pytest -m service` |
| `--lf` | 只運行上次失敗的測試 | `pytest --lf` |
| `--tb=style` | 錯誤回溯樣式 | `pytest --tb=short` |

### 覆蓋率測試選項

```bash
# 基本覆蓋率
pytest --cov=app/services tests/unit/services/

# HTML覆蓋率報告
pytest --cov=app/services --cov-report=html tests/unit/services/

# 顯示缺少覆蓋的行
pytest --cov=app/services --cov-report=term-missing tests/unit/services/

# 覆蓋率閾值檢查
pytest --cov=app/services --cov-fail-under=80 tests/unit/services/
```

## 🔍 調試測試用例

### 在PyCharm中調試

1. **設置斷點**:
   - 點擊代碼行號左側設置斷點
   - 或按 `Ctrl+F8`

2. **調試運行**:
   - 右鍵點擊測試，選擇 `Debug 'test_name'`
   - 或點擊測試方法旁的綠色蟲子圖標

3. **調試工具**:
   - `F8`: 單步執行
   - `F7`: 進入函數
   - `Shift+F8`: 跳出函數
   - `F9`: 繼續執行

### 查看測試輸出

1. **測試結果窗口**:
   - PyCharm底部會顯示 `Run` 或 `Debug` 窗口
   - 顯示測試執行狀態、通過/失敗數量

2. **錯誤詳情**:
   - 點擊失敗的測試查看錯誤詳情
   - 可以直接跳轉到失敗的代碼行

## ⚙️ 測試環境配置

### 1. 確保依賴安裝

```bash
pip install pytest pytest-cov pytest-mock pytest-xdist
```

### 2. 環境變量設置

在PyCharm的運行配置中添加：
```
FLASK_ENV=testing
FLASK_CONFIG=testing  
PYTHONPATH=/home/rem/Documents/Study/Code/lab_web/backend
```

### 3. 數據庫配置

測試使用內存數據庫，已在 `tests/conftest.py` 中配置：
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
```

## 📈 持續集成建議

### GitHub Actions 配置

在 `.github/workflows/tests.yml` 中添加：

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

## 🎉 快速開始

1. **確保PyCharm已識別測試目錄**:
   - 右鍵點擊 `tests` 文件夾
   - 選擇 `Mark Directory as` > `Test Sources Root`

2. **運行第一個測試**:
   - 打開 `test_auth_service.py`
   - 點擊 `TestAuthService` 類旁的綠色箭頭
   - 查看測試結果

3. **批量運行所有服務測試**:
   - 右鍵點擊 `tests/unit/services` 文件夾
   - 選擇 `Run 'Python tests in services'`
   - 等待所有80+個測試用例完成

現在您可以使用PyCharm高效地運行和管理所有service層的測試用例了！