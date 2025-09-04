# ---- Stage 1: Builder ----
FROM python:3.10-slim AS builder

# Set working directory
WORKDIR /app

# Cài dependencies hệ thống cần thiết để build wheel
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements trước để cache
COPY requirements.txt .

# Tạo virtual environment riêng (giảm dung lượng)
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# ---- Stage 2: Final ----
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy virtual environment từ builder
COPY --from=builder /venv /venv

# Add venv vào PATH
ENV PATH="/venv/bin:$PATH"

# Copy toàn bộ source code
COPY . .

# Expose port cho Railway/Docker
EXPOSE 8000

# Chạy FastAPI bằng uvicorn
CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]