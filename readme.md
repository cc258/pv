# PV - Video Platform

一个基于 FastAPI + SQLModel + React + Github actions 的视频管理平台，支持 RBAC 权限管理。

## 在线地址

| 服务 | 地址 |
|------|------|
| API | http://134.175.70.95:8887/docs# |
| Admin | http://134.175.70.95:8889/list/search-table |
| Web | http://134.175.70.95:8888/ |

**默认管理员账号：** `admin` / `admin`

## 技术栈

### Backend
- **FastAPI** - 高性能 Python Web 框架
- **SQLModel** - SQLAlchemy + Pydantic 融合
- **JWT** - Token 认证

### Frontend (Admin)
- **React 18**
- **Arco Design** - UI 组件库
- **Redux** - 状态管理
- **React Router** - 路由

### Frontend (Web)
- **React 18**
- **Jotai** - 状态管理
- **React Router** - 路由


## 功能模块

### 1. 用户认证
- JWT Token 登录/登出
- Token 自动刷新处理
- 401 错误自动跳转登录

### 2. 视频管理
- 视频列表（分页、搜索、筛选）
- 视频详情
- 多对多分类标签

### 3. 分类管理
- 分类列表
- 创建/删除分类
- 视频归属分类


## 本地开发

### 后端

```bash
cd backend

# 安装依赖
uv sync

# 初始化数据库
uv run python init_db.py

# 启动服务
uv run uvicorn app.main:app --reload --port 8000
```

### 管理后台

```bash
cd admin

# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev
```

### 用户端

```bash
cd web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## CI/CD 流程

### GitHub Actions

| Workflow | 触发 | 行为 |
|----------|------|------|
| `deploy-fastapi.yml` | backend 代码推送 | SSH 到服务器，执行 `docker-compose up -d --build` |
| `deploy-admin.yml` | admin 代码推送 | 构建后通过 SCP 部署到服务器 |
| `deploy-web.yml` | web 代码推送 | 构建后通过 SCP 部署到服务器 |

### 服务器

- **Docker** - 运行 FastAPI 容器
- **Caddy** - 反向代理，处理 HTTPS 和路由

### 部署流程

1. 代码推送到 `main` 分支
2. GitHub Actions 自动触发构建
3. 后端通过 Docker 部署
4. 前端通过 SCP 同步静态文件
5. Caddy 自动路由到对应服务

