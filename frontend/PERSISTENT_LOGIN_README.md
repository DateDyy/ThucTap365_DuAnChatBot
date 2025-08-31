# Tính năng Persistent Login (Đăng nhập liên tục)

## Tổng quan
Tính năng này cho phép người dùng duy trì trạng thái đăng nhập sau khi refresh trang (F5) hoặc đóng/mở lại trình duyệt.

## Cách hoạt động

### 1. Hệ thống Token
- Khi đăng nhập thành công, hệ thống tạo một token ngẫu nhiên
- Token được lưu trữ trong file `login_tokens.json`
- Token có thời hạn: 1 ngày (mặc định) hoặc 30 ngày (nếu chọn "Ghi nhớ đăng nhập")

### 2. Lưu trữ Token
- **URL Parameters**: Token được lưu tạm thời trong URL
- **localStorage**: Token được lưu vào localStorage của trình duyệt (nếu hỗ trợ)
- **Session State**: Token được lưu trong Streamlit session state

### 3. Khôi phục Đăng nhập
Khi load trang, hệ thống sẽ kiểm tra theo thứ tự:
1. Token trong URL parameters
2. Token trong localStorage
3. Token trong session state

## Các tính năng

### ✅ Đăng nhập với "Ghi nhớ đăng nhập"
- Chọn checkbox "Ghi nhớ đăng nhập" khi đăng nhập
- Token sẽ có hiệu lực trong 30 ngày
- Tự động đăng nhập khi mở lại trang

### ✅ Đăng nhập thông thường
- Không chọn "Ghi nhớ đăng nhập"
- Token có hiệu lực trong 1 ngày
- Vẫn duy trì trạng thái đăng nhập sau F5

### ✅ Đăng xuất an toàn
- Xóa token khỏi tất cả nơi lưu trữ
- Xóa token khỏi URL để bảo mật
- Xóa token khỏi localStorage

### ✅ Tự động dọn dẹp
- Xóa token hết hạn tự động
- Kiểm tra và làm sạch token cũ khi load trang

## Bảo mật

### 🔒 Token Security
- Token được tạo ngẫu nhiên với độ dài 32 ký tự
- Token được mã hóa và lưu trữ an toàn
- Token tự động hết hạn sau thời gian quy định

### 🔒 URL Security
- Token trong URL được xóa ngay sau khi xác thực thành công
- Sử dụng `window.history.replaceState()` để xóa token khỏi URL

### 🔒 Cross-tab Sync
- Token được đồng bộ giữa các tab của trình duyệt
- Khi đăng xuất ở một tab, các tab khác cũng sẽ đăng xuất

## Cấu trúc File

### Files đã thêm/sửa đổi:
- `auth.py`: Thêm hệ thống quản lý token
- `login_form.py`: Thêm tùy chọn "Ghi nhớ đăng nhập"
- `streamlit_app.py`: Thêm logic kiểm tra persistent login
- `profile_settings.py`: Cập nhật chức năng đăng xuất
- `config.py`: Thêm JavaScript cho localStorage

### Files mới:
- `login_tokens.json`: Lưu trữ token đăng nhập (tự động tạo)

## Cách sử dụng

### **. Cài đặt các thư viện cần thiết**
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
  pip install streamlit
  ```
- Chạy lệnh sau để khởi động Giao diện:
  ```bash
  streamlit run frontend/streamlit_app.py
  ```
### Cho người dùng:
1. Đăng nhập bình thường
2. Chọn "Ghi nhớ đăng nhập" nếu muốn duy trì đăng nhập lâu dài
3. Nhấn F5 hoặc đóng/mở lại trình duyệt
4. Hệ thống sẽ tự động đăng nhập lại

### Cho developer:
```python
# Kiểm tra token
from auth import validate_login_token
email = validate_login_token(token)

# Tạo token mới
from auth import create_login_token
token = create_login_token(email, remember_me=True)

# Xóa token
from auth import remove_login_token
remove_login_token(token)
```

## Troubleshooting

### Token không hoạt động:
1. Kiểm tra file `login_tokens.json` có tồn tại không
2. Kiểm tra token có hết hạn không
3. Kiểm tra localStorage có được hỗ trợ không

### Đăng nhập tự động không hoạt động:
1. Kiểm tra JavaScript có được load không
2. Kiểm tra console có lỗi JavaScript không
3. Kiểm tra token có được lưu vào localStorage không

## Lưu ý
- Tính năng này hoạt động tốt nhất với HTTPS
- Một số trình duyệt cũ có thể không hỗ trợ localStorage
- Token sẽ bị xóa khi người dùng xóa cache trình duyệt
