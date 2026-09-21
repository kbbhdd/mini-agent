FROM python:3.11-slim

WORKDIR /app

# 先复制依赖文件，利用 Docker 缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn//simple


# 再复制代码
COPY app/ ./app/
COPY web/ ./web/
COPY pytest.ini .

# 创建 docs 目录（运行时用挂载覆盖）
RUN mkdir -p docs

EXPOSE 8000

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]