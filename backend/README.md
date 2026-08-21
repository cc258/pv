# pv
preview video project~! deploy 5


# Quick Start
```bash
cd backend
uv sync
source .venv/bin/activate

uvicorn app.main:app --reload --port 8000
```


# e2e 测试

Playwright
https://playwright.dev/docs/intro


如果修改了数据库表

```python
$ alembic revision -m "create account table"
$ alembic upgrade head
```

什么是 
python-multipart
email-validator