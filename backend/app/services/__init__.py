"""
實驗室管理系統 - 服務層模塊

三層架構：
1. 路由層 (Routes) - HTTP請求/響應處理，參數校驗，權限檢查
2. 服務層 (Services) - 業務邏輯，數據校驗，事務管理，審計記錄
3. 模型層 (Models) - 數據持久化，數據庫操作
"""

from .base_service import BaseService
from .audit_service import AuditService
from .auth_service import AuthService
from .lab_service import LabService
from .member_service import MemberService
from .news_service import NewsService
from .project_service import ProjectService
from .research_group_service import ResearchGroupService
from .paper_service import PaperService
from .admin_service import AdminService
from .media_service import MediaService
from .image_upload_service import ImageUploadService

__all__ = [
    'BaseService',
    'AuditService',
    'AuthService',
    'LabService',
    'MemberService',
    'NewsService',
    'ProjectService',
    'ResearchGroupService',
    'PaperService',
    'AdminService',
    'MediaService',
    'ImageUploadService'
]