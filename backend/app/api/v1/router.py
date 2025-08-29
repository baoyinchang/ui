from fastapi import APIRouter
from app.api.v1 import (
    auth,
    users,
    dashboard,
    assets,
    alerts,
    hunting,
    intelligence,
    investigation,
    reports,
    system
)

api_router = APIRouter()

# 认证相关路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])

# 用户管理路由
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])

# 安全态势路由
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["安全态势"])

# 核心业务路由
api_router.include_router(assets.router, prefix="/assets", tags=["资产管理"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["告警中心"])
api_router.include_router(hunting.router, prefix="/hunting", tags=["威胁狩猎"])
api_router.include_router(intelligence.router, prefix="/intelligence", tags=["威胁情报"])
api_router.include_router(investigation.router, prefix="/investigation", tags=["调查与响应"])
api_router.include_router(reports.router, prefix="/reports", tags=["报告中心"])

# 系统管理路由
api_router.include_router(system.router, prefix="/system", tags=["系统管理"])