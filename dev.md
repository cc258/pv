# 开发步骤

### Step1 初始化

```shell

uv init .

uv add "fastapi[all]" langchain langchain-openai python-dotenv sqlalchemy uvicorn psycopg2-binary pydantic-settings aioredis httpx

```

### Step2 建立目录
```shell
- api
- core
- modals
- schemas
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
- api
------users.py
- db
------database.py
- models
------models.py
- schemas
------schemas.py
```

### 浏览效果
使用navcat打开数据库文件，插入数据，并访问users表第一条记录
```shell
http://127.0.0.1:8000/api/users/1
```

