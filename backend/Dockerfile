FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

# 使用腾讯云 pip 镜像源安装依赖
RUN pip install --no-cache-dir -r requirements.txt \
    -i https://mirrors.cloud.tencent.com/pypi/simple \
    --trusted-host mirrors.cloud.tencent.com \
    --timeout 120

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8887"]