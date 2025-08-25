# Thư mục api - Xây dựng và triển khai API cho Chatbot RAG

Thư mục `api` dùng để lưu trữ các mã nguồn và tài liệu liên quan đến việc xây dựng, triển khai API phục vụ cho chatbot RAG về Lập trình Web.

## Cấu trúc thư mục

```
api/
├── README_API.md           # Tài liệu hướng dẫn cho thư mục api
├── requirements.txt        # Danh sách thư viện chạy các script API
├── app/
│   ├── main.py             # File chính khởi động server API FastAPI
│   └── routes/
│       ├── query.py        # Định nghĩa các route API cho truy vấn dữ liệu
│       ├── chat.py         # Định nghĩa các route API cho chức năng chat
│       └── update.py       # Định nghĩa các route API cho cập nhật dữ liệu
├── router/
│   └── chatbot.py          # Định nghĩa các route API cho chatbot (nếu sử dụng riêng)
├── utils/
│   └── helper.py           # Các hàm tiện ích hỗ trợ xử lý dữ liệu cho API
```

## Chức năng các file và thư mục

- **README_API.md**  
  Tài liệu hướng dẫn sử dụng, cấu trúc và chức năng các file trong thư mục `api`.

- **requirements.txt**  
  Liệt kê các thư viện Python cần thiết để chạy API, ví dụ:  
  - `fastapi`: Xây dựng API nhanh và hiện đại.
  - `uvicorn`: Chạy server FastAPI.
  - `pydantic`: Kiểm tra và xác thực dữ liệu đầu vào.
  - Các thư viện khác phục vụ cho xử lý dữ liệu và tích hợp với chatbot.

- **app/main.py**  
  File khởi động server API, kết nối các route (query, chat, update) và xử lý request từ người dùng.

- **app/routes/query.py**  
  Định nghĩa các endpoint cho truy vấn dữ liệu từ hệ thống RAG (ví dụ: tìm kiếm thông tin, lấy kết quả từ vector store).

- **app/routes/chat.py**  
  Định nghĩa các endpoint cho chức năng chat, nhận câu hỏi từ người dùng và trả về phản hồi từ chatbot.

- **app/routes/update.py**  
  Định nghĩa các endpoint cho việc cập nhật dữ liệu, ví dụ: thêm mới, chỉnh sửa hoặc xóa dữ liệu trong hệ thống.

- **router/chatbot.py**  
  Định nghĩa các endpoint riêng cho chatbot, có thể dùng cho các chức năng chat nâng cao hoặc tích hợp với các module khác.

- **utils/helper.py**  
  Chứa các hàm tiện ích hỗ trợ xử lý dữ liệu, tiền xử lý câu hỏi, kiểm tra đầu vào, hoặc tích hợp với các module khác.

## Hướng dẫn sử dụng

1. Cài đặt các thư viện cần thiết:
   ```
   pip install -r api/requirements.txt
   ```

2. Khởi động server API:
   ```
   uvicorn api.app.main:app --reload
   ```

3. Truy cập các endpoint API để gửi câu hỏi và nhận phản hồi từ chatbot.

---

**Lưu ý:**  
- Đảm bảo các file dữ liệu và mô hình đã được xử lý và lưu trữ đúng vị trí trước khi khởi động API.
- Có thể mở rộng thêm các route hoặc chức năng tùy theo nhu cầu sử dụng.