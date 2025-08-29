from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Numeric, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

# 用户角色关联表
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

# 角色权限关联表
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 多对多关系：用户-角色
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    # 一对多关系：用户创建的调查会话
    investigations = relationship("InvestigationSession", back_populates="creator")
    # 一对多关系：用户创建的狩猎任务
    hunting_tasks = relationship("HuntingTask", back_populates="creator")

class Role(Base):
    """角色表"""
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 多对多关系
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

class Permission(Base):
    """权限表"""
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    # 多对多关系
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

class Asset(Base):
    """资产信息表"""
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    asset_type = Column(String(50), nullable=False)  # 服务器、工作站、网络设备等
    ip_address = Column(String(50), nullable=False, index=True)
    mac_address = Column(String(50))
    os_version = Column(String(100))
    status = Column(String(20), default='normal')  # normal, warning, danger
    is_honeypot = Column(Boolean, default=True)  # 是否为蜜罐设备
    is_virtual = Column(Boolean, default=True)  # 是否为虚拟机
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    vulnerabilities = relationship("AssetVulnerability", back_populates="asset")
    alerts = relationship("Alert", back_populates="asset")
    events = relationship("Event", back_populates="asset")
    compliance_results = relationship("AssetComplianceResult", back_populates="asset")

class Vulnerability(Base):
    """漏洞表"""
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String(50), unique=True)
    description = Column(Text)
    cvss_score = Column(Numeric(3, 1))
    severity = Column(String(20))  # low, medium, high, critical
    discovered_at = Column(DateTime)
    patched = Column(Boolean, default=False)

    # 关联关系
    asset_vulnerabilities = relationship("AssetVulnerability", back_populates="vulnerability")

class AssetVulnerability(Base):
    """资产漏洞关联表"""
    __tablename__ = "asset_vulnerabilities"

    asset_id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    vulnerability_id = Column(Integer, ForeignKey("vulnerabilities.id"), primary_key=True)
    first_found = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='open')  # open, fixed

    # 关联关系
    asset = relationship("Asset", back_populates="vulnerabilities")
    vulnerability = relationship("Vulnerability", back_populates="asset_vulnerabilities")

class Event(Base):
    """事件表"""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), nullable=False, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    source_ip = Column(String(50))
    destination_ip = Column(String(50))
    source_port = Column(Integer)
    destination_port = Column(Integer)
    protocol = Column(String(20))
    description = Column(Text)
    event_time = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    raw_data = Column(JSON)  # 存储原始事件数据

    # 关联关系
    asset = relationship("Asset", back_populates="events")
    alerts = relationship("Alert", back_populates="event")

class Alert(Base):
    """告警表"""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    asset_id = Column(Integer, ForeignKey("assets.id"))
    alert_name = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False, index=True)  # low, medium, high, critical
    status = Column(String(20), default='unhandled', index=True)  # unhandled, handling, resolved
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    handled_by = Column(Integer, ForeignKey("users.id"))
    handle_notes = Column(Text)
    handled_at = Column(DateTime)

    # 关联关系
    event = relationship("Event", back_populates="alerts")
    asset = relationship("Asset", back_populates="alerts")
    handler = relationship("User")

class AlertRule(Base):
    """告警规则表"""
    __tablename__ = "alert_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    condition = Column(JSON, nullable=False)  # 存储告警触发条件
    severity = Column(String(20), nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class IOC(Base):
    """威胁情报指标表"""
    __tablename__ = "iocs"

    id = Column(Integer, primary_key=True, index=True)
    ioc_type = Column(String(50), nullable=False, index=True)  # ip, domain, hash, url等
    value = Column(String(255), nullable=False, unique=True, index=True)
    threat_type = Column(String(100))
    severity = Column(String(20), default='medium')
    source = Column(String(100))
    confidence = Column(Integer)  # 0-100
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

class ThreatFamily(Base):
    """威胁家族表"""
    __tablename__ = "threat_families"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    associated_iocs = Column(JSON)  # 关联的IOC ID数组

class IntelligenceSource(Base):
    """情报源表"""
    __tablename__ = "intelligence_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    source_type = Column(String(50))  # internal, commercial, open_source
    url = Column(String(255))
    api_key = Column(String(255))
    enabled = Column(Boolean, default=True)
    last_sync = Column(DateTime)
    sync_interval = Column(Integer)  # 同步间隔(分钟)

class InvestigationSession(Base):
    """调查会话表"""
    __tablename__ = "investigation_sessions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String(20), default='active')  # active, completed, archived

    # 关联关系
    creator = relationship("User", back_populates="investigations")

class HuntingTask(Base):
    """狩猎任务表"""
    __tablename__ = "hunting_tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    query_string = Column(Text, nullable=False)
    query_type = Column(String(20), default='advanced')  # advanced, visual
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='pending')  # pending, running, completed, failed
    result_count = Column(Integer, default=0)
    completed_at = Column(DateTime)

    # 关联关系
    creator = relationship("User", back_populates="hunting_tasks")

class ComplianceCheck(Base):
    """合规检查项表"""
    __tablename__ = "compliance_checks"

    id = Column(Integer, primary_key=True, index=True)
    policy_name = Column(String(100), nullable=False)
    check_item = Column(String(200), nullable=False)
    severity = Column(String(20), default='medium')
    description = Column(Text)

    # 关联关系
    results = relationship("AssetComplianceResult", back_populates="check")

class AssetComplianceResult(Base):
    """资产合规检查结果表"""
    __tablename__ = "asset_compliance_results"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    check_id = Column(Integer, ForeignKey("compliance_checks.id"))
    result = Column(Boolean)  # TRUE:合规, FALSE:不合规
    checked_at = Column(DateTime, default=datetime.utcnow)

    # 关联关系
    asset = relationship("Asset", back_populates="compliance_results")
    check = relationship("ComplianceCheck", back_populates="results")