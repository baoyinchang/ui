from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import Generator, AsyncGenerator
import logging
from app.core.config import settings

# 配置日志
logger = logging.getLogger(__name__)

# 获取数据库URL并判断数据库类型
database_url = settings.database_url
is_sqlite = database_url.startswith("sqlite")
is_postgres = database_url.startswith("postgresql")

# 同步引擎配置
if is_sqlite:
    # SQLite配置
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},  # SQLite需要这个参数
        pool_pre_ping=True,
        echo=settings.DEBUG  # 开发环境显示SQL日志
    )
    # SQLite不支持异步，使用同步引擎
    async_engine = None
else:
    # PostgreSQL配置
    engine = create_engine(
        database_url,
        pool_pre_ping=True,  # 连接前检查连接是否有效
        pool_recycle=300,    # 连接回收时间（秒）
        pool_size=10,        # 连接池大小
        max_overflow=20,     # 最大溢出连接数
        echo=settings.DEBUG  # 开发环境显示SQL日志
    )

    # PostgreSQL异步引擎
    async_database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
    async_engine = create_async_engine(
        async_database_url,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,
        max_overflow=20,
        echo=settings.DEBUG
    )

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 异步会话工厂（仅PostgreSQL）
if async_engine:
    AsyncSessionLocal = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False
    )
else:
    AsyncSessionLocal = None

# 基础模型类
Base = declarative_base()

# 依赖项：提供同步数据库会话
def get_db() -> Generator:
    """
    获取数据库会话的依赖项
    用于FastAPI的Depends注入
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"数据库会话错误: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# 异步数据库会话上下文管理器
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取异步数据库会话（仅PostgreSQL支持）
    """
    if not AsyncSessionLocal:
        raise RuntimeError("异步数据库会话不可用，当前使用SQLite")

    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"异步数据库会话错误: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

# 数据库初始化函数
def init_db() -> None:
    """
    初始化数据库表结构
    仅在开发环境使用，生产环境使用Alembic迁移
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表结构初始化完成")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise