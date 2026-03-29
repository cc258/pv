import uvicorn
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

# 环境
from apis.app.core.config import settings

# 路由
from apis.app.core.router import router

# 数据库
from apis.app.core.deps import create_db_and_tables, drop_db

# 创建数据库表
drop_db()
create_db_and_tables()


# 创建APP
app = FastAPI(
    title="PV",
    description="Popular video project",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 设置允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由
app.include_router(router, prefix=settings.API_V1)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

