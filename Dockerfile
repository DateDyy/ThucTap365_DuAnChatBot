# Chọn Python image
FROM python:3.10-slim

# Đặt thư mục làm việc
WORKDIR /app

# Copy file requirements
COPY requirements.txt .

# Cài đặt dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ project
COPY . .

# Expose cổng (Railway tự dùng $PORT)
EXPOSE 8000

# Lệnh chạy (chạy FastAPI qua Uvicorn)
CMD ["sh", "-c", "uvicorn api.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
