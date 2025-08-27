# 🤖 AI Chat Assistant

Ứng dụng chat AI hoàn chỉnh được xây dựng bằng Streamlit với các tính năng đăng nhập, chat, upload file, và cài đặt tùy chỉnh.

## ✨ Tính năng chính

### 🔐 Hệ thống xác thực
- Đăng ký tài khoản mới
- Đăng nhập với email và mật khẩu
- Mã hóa mật khẩu an toàn với bcrypt
- Quản lý phiên làm việc

### 💬 Chat AI
- Giao diện chat thân thiện
- Lịch sử chat được lưu trữ
- Upload file đính kèm (txt, pdf, doc, docx, jpg, png, gif)
- Nút ghi âm (placeholder cho tính năng voice)
- Phản hồi AI mô phỏng (sẵn sàng tích hợp OpenAI API)

### 👤 Quản lý Profile
- Xem thông tin tài khoản
- Cập nhật tên người dùng
- Thay đổi avatar từ bộ sưu tập emoji
- Theo dõi thời gian tạo tài khoản và đăng nhập cuối

### ⚙️ Cài đặt tùy chỉnh
- Thay đổi màu sắc chat (6 màu có sẵn)
- Chọn giao diện sáng/tối
- Điều chỉnh kích thước chữ
- Cài đặt tự động cuộn, hiển thị timestamp
- Thông báo âm thanh
- Timeout phiên làm việc

### 📚 Lịch sử chat
- Xem lịch sử chat theo thời gian
- Nhóm tin nhắn theo ngày
- Hiển thị file đính kèm

## 🚀 Cài đặt

### Yêu cầu hệ thống
- Python 3.8+
- Windows/Linux/macOS

### Bước 1: Clone repository
```bash
git clone <repository-url>
cd ai-chat-assistant
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy ứng dụng
```bash
streamlit run app.py
```

Ứng dụng sẽ chạy tại: `http://localhost:8501`

## 📝 Sử dụng

### Đăng ký tài khoản
1. Mở ứng dụng trong trình duyệt
2. Nhấn nút "Đăng ký"
3. Điền thông tin: Họ tên, Email, Mật khẩu
4. Nhấn "Đăng ký" để tạo tài khoản

### Đăng nhập
1. Nhập email và mật khẩu
2. Nhấn "Đăng nhập"
3. Hoặc sử dụng tài khoản mẫu: `admin@example.com` / `admin123`

### Chat với AI
1. Sau khi đăng nhập, chọn "💬 Chat" từ menu
2. Gõ tin nhắn trong ô nhập liệu
3. Có thể upload file đính kèm
4. Nhấn "Gửi tin nhắn" hoặc Enter
5. AI sẽ phản hồi (hiện tại là mô phỏng)

### Cài đặt Profile
1. Chọn "👤 Profile" từ menu
2. Xem thông tin tài khoản hiện tại
3. Cập nhật tên và chọn avatar mới
4. Nhấn "Cập nhật thông tin"

### Cài đặt ứng dụng
1. Chọn "⚙️ Settings" từ menu
2. Tùy chỉnh màu sắc, giao diện, font size
3. Cài đặt các tùy chọn chat và bảo mật
4. Nhấn "Lưu cài đặt"

## 🗂️ Cấu trúc dự án

```
ai-chat-assistant/
├── app.py                 # File chính của ứng dụng
├── config.py             # Cấu hình và CSS
├── auth.py               # Xử lý xác thực người dùng
├── chat_utils.py         # Xử lý chat và file upload
├── profile_settings.py   # Quản lý profile và settings
├── requirements.txt      # Dependencies
├── README.md            # Hướng dẫn sử dụng
├── users.json           # Dữ liệu người dùng (tự động tạo)
├── config.json          # Cấu hình ứng dụng (tự động tạo)
└── chat_history_*.json  # Lịch sử chat theo người dùng
```

## 🔧 Tích hợp OpenAI API

Để tích hợp OpenAI API thực tế, cần:

1. Cài đặt thêm dependency:
```bash
pip install openai
```

2. Thêm API key vào file `.env`:
```
OPENAI_API_KEY=your_api_key_here
```

3. Cập nhật hàm `simulate_ai_response()` trong `chat_utils.py`:
```python
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ai_response(user_message, file_info=None):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là một trợ lý AI hữu ích."},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Xin lỗi, có lỗi xảy ra: {str(e)}"
```

## 🎨 Tùy chỉnh giao diện

### Thêm màu sắc mới
Chỉnh sửa `CHAT_COLORS` trong `config.py`:
```python
CHAT_COLORS = {
    "Blue": "#007bff",
    "Green": "#28a745",
    "Purple": "#6f42c1",
    "Orange": "#fd7e14",
    "Red": "#dc3545",
    "Teal": "#20c997",
    "Pink": "#e83e8c",  # Thêm màu mới
}
```

### Tùy chỉnh CSS
Chỉnh sửa hàm `load_css()` trong `config.py` để thay đổi giao diện.

## 🔒 Bảo mật

- Mật khẩu được mã hóa với bcrypt
- Dữ liệu người dùng lưu trữ local
- Session management an toàn
- Validation input đầu vào

## 🐛 Xử lý lỗi

### Lỗi thường gặp:

1. **Port 8501 đã được sử dụng**
   ```bash
   streamlit run app.py --server.port 8502
   ```

2. **Lỗi import module**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Lỗi file permissions**
   - Đảm bảo thư mục có quyền ghi
   - Chạy với quyền admin nếu cần

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra console log
2. Đảm bảo đã cài đặt đúng dependencies
3. Kiểm tra quyền truy cập file

## 🚀 Roadmap

- [ ] Tích hợp OpenAI API thực tế
- [ ] Tính năng ghi âm và nhận diện giọng nói
- [ ] Hỗ trợ đa ngôn ngữ
- [ ] Export lịch sử chat
- [ ] Chia sẻ chat
- [ ] Database thay vì file JSON
- [ ] API endpoints
- [ ] Docker deployment

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.


