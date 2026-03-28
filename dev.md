# 开发步骤

### Step1 初始化

```shell

uv init .

uv add "fastapi[all]" langchain langchain-openai python-dotenv sqlmodel alembic uvicorn psycopg2-binary pydantic-settings aioredis httpx

还要设置 pycharm的解释器 > 设置 > 已经存在的本地 > uv > 在项目对应.venv， 比如

/Users/charlie/Documents/github/pv/.venv/bin/python3.13

完成后，系统会重新构建，等待完成，
需要更新pycharm，调试启动应用的配置，设定为当前项目的配置，重启OK。

如果要升级当前的依赖
uv sync --upgrade

```

### Step2 建立目录
```shell
- api
- core
- modals
```

### Step3 按照顺序写代码
```shell
- .env
- main.py
- config.py
- route.py
```

### Step4 加入数据库
```shell
- core
------deps.py
- api
------users.py
- models
------models.py
```

### 浏览效果
使用navcat打开数据库文件，插入数据，并访问users表第一条记录
```shell
http://127.0.0.1:8000/api/users/1
```


# alembic

### installation
dependence SqlAchemy

```python
# 添加 `alembic`
uv add alembic

# 初始化，并建立 `alembic` 目录
alembic init alembic

```

# pyjwt

```python
uv add pyjwt
```







---

# 2. web后台搭建：

`manage`目录

使用Arco pro的React，vite框架

# 脚手架的方式不容易出错

```
npm create arco-pro@latest
```

按照步骤，安装完整版本

注意2个要点，使用官方推荐的pnpm,安装dayjs

具体执行下面的操作

```
cd 你的目录
npm -g install pnpm
pnpm i dayjs
pnpm dev || pnpm start
```

# 3.Web前台展示

`web`目录

使用Vite构建React项目，

加入Tailwindcss

比较简单好用。










