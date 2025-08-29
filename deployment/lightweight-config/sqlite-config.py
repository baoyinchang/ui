"""
轻量化数据库配置 - SQLite替代PostgreSQL
适用于蜜罐主机部署，减少资源占用
"""

from pydantic_settings import BaseSettings
from typing import Optional
import secrets
import os

class LightweightSettings(BaseSettings):
    """轻量化配置类"""
    
    # 应用基本配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "H-System蜜罐EDR平台"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    
    # 轻量化数据库配置 - 使用SQLite
    DATABASE_URL: str = "sqlite:///./hsystem.db"
    DATABASE_POOL_SIZE: int = 5  # SQLite连接池大小
    DATABASE_MAX_OVERFLOW: int = 0  # 不允许溢出连接
    
    # Redis配置 - 可选，用于缓存
    REDIS_URL: Optional[str] = None  # 如果不需要可以设为None
    REDIS_ENABLED: bool = False
    
    # 日志配置
    LOG_LEVEL: str = "WARNING"  # 减少日志输出
    LOG_FILE: str = "/var/log/hsystem/app.log"
    LOG_MAX_SIZE: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 3
    
    # 性能配置
    MAX_CONNECTIONS_COUNT: int = 10
    MIN_CONNECTIONS_COUNT: int = 2
    
    # 安全配置
    ALLOWED_HOSTS: list = ["localhost", "127.0.0.1"]
    CORS_ORIGINS: list = ["http://localhost", "http://127.0.0.1"]
    
    # 文件上传配置
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    UPLOAD_DIR: str = "/tmp/hsystem/uploads"
    
    # 缓存配置
    CACHE_TTL: int = 300  # 5分钟缓存
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# 创建轻量化设置实例
lightweight_settings = LightweightSettings()

# SQLite数据库引擎配置
def get_sqlite_engine_config():
    """获取SQLite引擎配置"""
    return {
        "url": lightweight_settings.DATABASE_URL,
        "connect_args": {
            "check_same_thread": False,  # 允许多线程访问
            "timeout": 20,  # 连接超时
            "isolation_level": None,  # 自动提交模式
        },
        "pool_size": lightweight_settings.DATABASE_POOL_SIZE,
        "max_overflow": lightweight_settings.DATABASE_MAX_OVERFLOW,
        "pool_pre_ping": True,  # 连接前ping检查
        "pool_recycle": 3600,  # 1小时回收连接
        "echo": False,  # 不输出SQL语句
    }

# 内存优化的SQLite配置
SQLITE_PRAGMAS = [
    "PRAGMA journal_mode=WAL",  # 使用WAL模式提高并发
    "PRAGMA synchronous=NORMAL",  # 平衡性能和安全
    "PRAGMA cache_size=10000",  # 10MB缓存
    "PRAGMA temp_store=MEMORY",  # 临时表存储在内存
    "PRAGMA mmap_size=268435456",  # 256MB内存映射
    "PRAGMA optimize",  # 自动优化
]

def apply_sqlite_optimizations(connection):
    """应用SQLite优化配置"""
    for pragma in SQLITE_PRAGMAS:
        connection.execute(pragma)

# 轻量化的数据库会话配置
def get_lightweight_session_config():
    """获取轻量化会话配置"""
    return {
        "autocommit": False,
        "autoflush": False,
        "bind": None,  # 将在创建时绑定
        "expire_on_commit": False,  # 提交后不过期对象
    }

# 监控配置
MONITORING_CONFIG = {
    "enabled": True,
    "metrics_interval": 60,  # 1分钟收集一次指标
    "max_memory_usage": 200 * 1024 * 1024,  # 200MB内存限制
    "max_cpu_usage": 80,  # 80% CPU使用率限制
    "alert_thresholds": {
        "memory": 150 * 1024 * 1024,  # 150MB内存告警
        "cpu": 70,  # 70% CPU告警
        "disk": 80,  # 80% 磁盘使用率告警
    }
}

# 清理配置
CLEANUP_CONFIG = {
    "enabled": True,
    "interval": 3600,  # 1小时清理一次
    "max_log_age": 7 * 24 * 3600,  # 7天日志保留
    "max_temp_age": 24 * 3600,  # 1天临时文件保留
    "vacuum_interval": 24 * 3600,  # 1天执行一次VACUUM
}

# 资源限制配置
RESOURCE_LIMITS = {
    "max_request_size": 10 * 1024 * 1024,  # 10MB请求大小限制
    "max_response_size": 50 * 1024 * 1024,  # 50MB响应大小限制
    "max_concurrent_requests": 50,  # 最大并发请求数
    "request_timeout": 30,  # 30秒请求超时
    "max_query_time": 10,  # 10秒查询超时
}

# 导出配置
__all__ = [
    "lightweight_settings",
    "get_sqlite_engine_config", 
    "get_lightweight_session_config",
    "apply_sqlite_optimizations",
    "MONITORING_CONFIG",
    "CLEANUP_CONFIG", 
    "RESOURCE_LIMITS"
]
