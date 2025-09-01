from pydantic_settings import BaseSettings
from typing import Optional
import secrets

class Settings(BaseSettings):
    # 应用基本配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "H-System蜜罐EDR平台"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120  # JWT有效期2小时

    # 开发配置
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # 数据库配置 - 支持SQLite和PostgreSQL
    DATABASE_URL: Optional[str] = None  # 优先使用这个
    POSTGRES_SERVER: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "hsystem"
    POSTGRES_URI: Optional[str] = None

    # Manticore配置
    MANTICORE_HOST: str = "manticore"
    MANTICORE_PORT: int = 9306
    MANTICORE_USER: str = ""
    MANTICORE_PASSWORD: str = ""

    # Redis（Celery用）
    REDIS_URL: str = "redis://redis:6379/0"

    @property
    def database_url(self) -> str:
        """获取数据库连接URL"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        if self.POSTGRES_URI:
            return self.POSTGRES_URI
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    @property
    def postgres_uri(self) -> str:
        """保持向后兼容"""
        return self.database_url

    class Config:
        case_sensitive = True
        env_file = ".env"
        # 允许额外的字段，避免验证错误
        extra = "allow"

settings = Settings()