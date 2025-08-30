# Thư mục `api` - Xây dựng và triển khai API cho Chatbot RAG

Thư mục `api` chứa mã nguồn và tài liệu liên quan đến việc xây dựng, triển khai API phục vụ cho chatbot RAG hỗ trợ sinh viên học lập trình web.

---

## Cấu trúc thư mục

```
api/
├── README_API.md           # Tài liệu hướng dẫn cho thư mục api
├── requirements.txt        # Danh sách thư viện chạy các script API
├── app/
│   ├── main.py             # File chính khởi động server API FastAPI
│   ├── routes/
│   │   ├── query.py        # Định nghĩa các route API cho truy vấn dữ liệu
│   │   ├── chat.py         # Định nghĩa các route API cho chức năng chat
│   │   └── update.py       # Định nghĩa các route API cho cập nhật dữ liệu
│   ├── services/
│   │   ├── llm_service.py      # Xử lý nghiệp vụ liên quan đến mô hình ngôn ngữ lớn (LLM)
│   │   └── vector_service.py   # Xử lý nghiệp vụ liên quan đến truy vấn và tìm kiếm vector
│   ├── prompts/
│   │   └── rag_prompt.py       # Định nghĩa các template prompt cho mô hình LLM
├── router/
│   └── chatbot.py          # Định nghĩa các route API cho chatbot (nếu sử dụng riêng)
```

---

## Chức năng các file và thư mục

### **1. README_API.md**
- Tài liệu hướng dẫn sử dụng, cấu trúc và chức năng các file trong thư mục `api`.

### **2. requirements.txt**
- Danh sách các thư viện Python cần thiết để chạy API:
  - `fastapi`: Xây dựng API nhanh và hiện đại.
  - `uvicorn`: Chạy server FastAPI.
  - `pydantic`: Kiểm tra và xác thực dữ liệu đầu vào.
  - `langchain`, `langchain-huggingface`, `faiss-cpu`, `sentence-transformers`, `torch`, v.v.

### **3. app/main.py**
- File khởi động server API, kết nối các route (query, chat, update) và xử lý request từ người dùng.

### **4. app/routes/query.py**
- Định nghĩa endpoint cho truy vấn dữ liệu từ hệ thống RAG (ví dụ: tìm kiếm thông tin, lấy kết quả từ vector store).

### **5. app/routes/chat.py**
- Định nghĩa endpoint cho chức năng chat, nhận câu hỏi từ người dùng và trả về phản hồi từ chatbot.

### **6. app/routes/update.py**
- Định nghĩa endpoint cho việc cập nhật dữ liệu, ví dụ: thêm mới, chỉnh sửa hoặc xóa dữ liệu trong hệ thống.

### **7. app/services/llm_service.py**
- Chứa các hàm xử lý nghiệp vụ liên quan đến mô hình ngôn ngữ lớn (LLM), ví dụ: sinh câu trả lời, tóm tắt, sinh văn bản.

### **8. app/services/vector_service.py**
- Chứa các hàm xử lý nghiệp vụ liên quan đến truy vấn, tìm kiếm và thao tác với vector embedding, phục vụ cho việc tìm kiếm ngữ nghĩa.

### **9. app/prompts/rag_prompt.py**
- Định nghĩa các template prompt cho mô hình LLM, bao gồm:
  - **RAG_TEMPLATE**: Prompt hỗ trợ trả lời dựa trên ngữ cảnh.
  - **CHAT_TEMPLATE**: Prompt hỗ trợ hội thoại tự nhiên.

### **10. router/chatbot.py**
- Định nghĩa các endpoint riêng cho chatbot, có thể dùng cho các chức năng chat nâng cao hoặc tích hợp với các module khác.

---

## Hướng dẫn sử dụng

### **1. Cài đặt các thư viện cần thiết**
- Tạo môi trường ảo:
  ```bash
  python -m venv venv
  ```
- Kích hoạt môi trường ảo:
  - **Windows**:
    ```bash
    venv\Scripts\activate
    ```
  - **Linux/macOS**:
    ```bash
    source venv/bin/activate
    ```
- Cài đặt các thư viện:
  ```bash
  pip install -r api/requirements.txt
  ```

---

### **2. Khởi động server API**
- Chạy lệnh sau để khởi động server:
  ```bash
  uvicorn api.app.main:app --reload
  ```

---

### **3. Truy cập các endpoint API**
- Mở Swagger UI tại [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) để thử các chức năng.
- Các endpoint chính:
  - **`/api/query`**:
    - **Phương thức**: `POST`
    - **Chức năng**: Truy vấn dữ liệu từ vector store.
  - **`/api/chat`**:
    - **Phương thức**: `POST`
    - **Chức năng**: Gửi tin nhắn và nhận phản hồi từ mô hình LLM.
  - **`/api/update`**:
    - **Phương thức**: `POST`
    - **Chức năng**: Thêm tài liệu mới vào vector store.

---

### **4. Lưu ý**
- Đảm bảo các file dữ liệu và mô hình đã được xử lý và lưu trữ đúng vị trí trước khi khởi động API.
- Có thể mở rộng thêm các route hoặc chức năng tùy theo nhu cầu sử dụng.