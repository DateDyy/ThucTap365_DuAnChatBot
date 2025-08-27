# Thư mục api - Xây dựng và triển khai API cho Chatbot RAG

Thư mục `api` dùng để lưu trữ mã nguồn và tài liệu liên quan đến việc xây dựng, triển khai API phục vụ cho chatbot RAG về Lập trình Web.

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
├── router/
│   └── chatbot.py          # Định nghĩa các route API cho chatbot (nếu sử dụng riêng)
```

## Chức năng các file và thư mục

- **README_API.md**  
  Tài liệu hướng dẫn sử dụng, cấu trúc và chức năng các file trong thư mục `api`.

- **requirements.txt**  
  Liệt kê các thư viện Python cần thiết để chạy API, ví dụ:  
  - `fastapi`: Xây dựng API nhanh và hiện đại.
  - `uvicorn`: Chạy server FastAPI.
  - `pydantic`: Kiểm tra và xác thực dữ liệu đầu vào.
  - `langchain`, `langchain-huggingface`, `faiss-cpu`, `sentence-transformers`, `torch`, v.v.

- **app/main.py**  
  File khởi động server API, kết nối các route (query, chat, update) và xử lý request từ người dùng.

- **app/routes/query.py**  
  Định nghĩa endpoint cho truy vấn dữ liệu từ hệ thống RAG (ví dụ: tìm kiếm thông tin, lấy kết quả từ vector store).

- **app/routes/chat.py**  
  Định nghĩa endpoint cho chức năng chat, nhận câu hỏi từ người dùng và trả về phản hồi từ chatbot.

- **app/routes/update.py**  
  Định nghĩa endpoint cho việc cập nhật dữ liệu, ví dụ: thêm mới, chỉnh sửa hoặc xóa dữ liệu trong hệ thống.

- **app/services/llm_service.py**  
  Chứa các hàm xử lý nghiệp vụ liên quan đến mô hình ngôn ngữ lớn (LLM), ví dụ: sinh câu trả lời, tóm tắt, sinh văn bản.

- **app/services/vector_service.py**  
  Chứa các hàm xử lý nghiệp vụ liên quan đến truy vấn, tìm kiếm và thao tác với vector embedding, phục vụ cho việc tìm kiếm ngữ nghĩa.

- **router/chatbot.py**  
  Định nghĩa các endpoint riêng cho chatbot, có thể dùng cho các chức năng chat nâng cao hoặc tích hợp với các module khác.

## Hướng dẫn sử dụng

1. **Cài đặt các thư viện cần thiết:**
   ```
   pip install -r api/requirements.txt
   ```

2. **Khởi động server API:**
   ```
   uvicorn api.app.main:app --reload
   ```

3. **Truy cập các endpoint API:**  
   Truy cập [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) để thử các chức năng truy vấn, chat, cập nhật dữ liệu.

---

**Lưu ý:**  
- Đảm bảo các file dữ liệu và mô hình đã được xử lý và lưu trữ đúng vị trí trước khi khởi động API.
- Có thể mở rộng thêm các route hoặc chức năng tùy theo nhu cầu sử dụng.