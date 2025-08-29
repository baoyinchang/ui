# 导入所有数据库模型
from .postgres import (
    User,
    Role,
    Permission,
    Asset,
    Vulnerability,
    AssetVulnerability,
    Event,
    Alert,
    AlertRule,
    IOC,
    ThreatFamily,
    IntelligenceSource,
    InvestigationSession,
    HuntingTask,
    ComplianceCheck,
    AssetComplianceResult,
    user_roles,
    role_permissions
)

# 导出所有模型，方便其他模块导入
__all__ = [
    "User",
    "Role",
    "Permission",
    "Asset",
    "Vulnerability",
    "AssetVulnerability",
    "Event",
    "Alert",
    "AlertRule",
    "IOC",
    "ThreatFamily",
    "IntelligenceSource",
    "InvestigationSession",
    "HuntingTask",
    "ComplianceCheck",
    "AssetComplianceResult",
    "user_roles",
    "role_permissions"
]