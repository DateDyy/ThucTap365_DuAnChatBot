# Chatbot RAG Cho Lập Trình Web

Dự án này nhằm nâng cao trải nghiệm học tập cho người dùng quan tâm đến lập trình web bằng cách cung cấp một chatbot tương tác, thông minh và dễ sử dụng. Chatbot hỗ trợ tìm kiếm thông tin, trả lời câu hỏi, và quản lý dữ liệu học tập.

---

## Hướng Dẫn Sử Dụng

### **Trường hợp muốn trải nghiệm toàn bộ hệ thống**
Đọc các file **README** tương ứng của từng thư mục theo thứ tự:
1. `rag_data_prep`
2. `vector`
3. `api`
4. `frontend`

---

### **Trường hợp chỉ muốn chạy thử giao diện FastAPI + Streamlit**

#### **Bước 1: Khởi động API (FastAPI)**
1. Tạo một cửa sổ PowerShell/Terminal cho API.
2. Tạo môi trường ảo:
   ```bash
   python -m venv venv
    ```
3. Kích hoạt môi trường ảo:
- **Windows**:
    ```bash
    venv\Scripts\activate
    ```
- **Linux/macOS**:
    ```bash
    source venv/bin/activate
    ```
4. Cài đặt các thư viện:
  ```bash
  pip install -r api/requirements.txt
  ```
5. Chạy lệnh sau để khởi động server api:
  ```bash
  uvicorn api.app.main:app --reload
  ```
6. Truy cập các endpoint API:
- Mở Swagger UI tại [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) để thử các chức năng.

#### **Bước 2: Khởi động giao diện (Streamlit)**
1. Tạo một cửa sổ PowerShell/Terminal khác.
2. Cài đặt thư viện:
  ```bash
  pip install streamlit
  ```
3. Chạy lệnh sau để khởi động Giao diện:
  ```bash
  streamlit run frontend/streamlit_app.py
  ```

### Nếu phần API bị lỗi

1. Kiểm tra trong thư mục THUCTAP365_DUANCHATBOT có tồn tại file ".env".
2. Nếu không hãy tạo file .env ở thư mục chính với nội dung
  ```bash
  HF_TOKEN=<mã của bạn>
  ```


#### Hướng Dẫn Cho Người Dùng

1. Đăng nhập bằng tài khoản đã đăng ký.
2. Chọn "Ghi nhớ đăng nhập" nếu muốn duy trì phiên đăng nhập lâu dài.
3. Làm mới trình duyệt (F5) hoặc đóng/mở lại tab.
4. Hệ thống sẽ tự động khôi phục đăng nhập nếu đã chọn ghi nhớ.
