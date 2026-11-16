# syntax=docker/dockerfile:1
FROM python:3.12-slim

# 容器内必须监听 0.0.0.0；DB 放在 /data，用 volume 持久化。
# 注意：如果通过 --env-file 传入 .env，里面的 HOST/DB_PATH 会覆盖这里的值，
# 记得改成 HOST=0.0.0.0、DB_PATH=/data/gateway.db。
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=3006 \
    DB_PATH=/data/gateway.db \
    MOCK_UPSTREAM=0

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./

RUN useradd --create-home --uid 10001 app \
    && mkdir -p /data \
    && chown app:app /data

USER app
VOLUME ["/data"]
EXPOSE 3006

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:3006/healthz', timeout=2)"

CMD ["python", "server.py"]
