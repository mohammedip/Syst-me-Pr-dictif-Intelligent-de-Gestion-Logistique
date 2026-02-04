# fastapi_stream/fastapi.Dockerfile
FROM python:3.11-slim

# Install minimal deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create app folder
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI + bridge code
COPY app_fastapi_stream.py .
COPY bridge_ws_to_tcp.py .

# Expose ports
EXPOSE 8000
EXPOSE 9009

# Default command = FastAPI service
CMD ["uvicorn", "app_fastapi_stream:app", "--host", "0.0.0.0", "--port", "8000"]

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/ || exit 1
