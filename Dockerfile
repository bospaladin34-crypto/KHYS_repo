FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || true

ENV BRIDGE_TOKEN=""
ENV SANTOS_INTERFACE="TCP://0.0.0.0:8080"
ENV BRIDGE_INTERFACE="0.0.0.0"
ENV BRIDGE_PORT="9090"

EXPOSE 8080 9090

CMD ["python", "run_kernel.py"]
