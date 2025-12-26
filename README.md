# 数码网购平台 - 后端 API

FastAPI + Tortoise ORM + SQLite

## Railway 部署步骤

### 1. 准备工作
- 注册 [Railway](https://railway.app) 账号
- 安装 Railway CLI（可选）：`npm install -g @railway/cli`

### 2. 部署方式

#### 方式一：通过 GitHub 部署（推荐）

1. 将 `backend` 文件夹推送到 GitHub 仓库
2. 登录 Railway，点击 "New Project"
3. 选择 "Deploy from GitHub repo"
4. 选择你的仓库，Railway 会自动检测并部署

#### 方式二：通过 CLI 部署

```bash
cd backend
railway login
railway init
railway up
```

### 3. 配置环境变量

在 Railway 项目设置中添加以下环境变量：

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `SECRET_KEY` | JWT 密钥（必须修改） | `your-random-secret-key-here` |
| `CORS_ORIGINS` | 允许的前端域名 | `https://your-frontend.com` |
| `DEBUG` | 调试模式 | `false` |

### 4. 初始化数据

部署成功后，通过 Railway CLI 运行初始化脚本：

```bash
railway run python init_data.py
```

或者在 Railway 控制台的 Shell 中运行。

### 5. 获取 API 地址

部署完成后，Railway 会提供一个域名，如：
`https://your-project.up.railway.app`

将此地址配置到前端的 API 基础路径中。

## 本地开发

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据
python init_data.py

# 启动服务
python run.py
```

## API 文档

启动后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
