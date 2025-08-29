from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需限制来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix=settings.API_V1_STR)

# 根路径
@app.get("/")
def read_root():
    return {"message": f"欢迎使用{settings.PROJECT_NAME} API", "version": "v1"}