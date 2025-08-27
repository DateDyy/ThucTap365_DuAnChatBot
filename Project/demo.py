import streamlit as st

st.title("🤖 AI Chat Assistant - Demo")

st.write("Ứng dụng đã được tạo thành công!")
st.write("Để chạy ứng dụng chính, sử dụng lệnh:")
st.code("streamlit run app.py")

st.write("### Các tính năng đã được implement:")
st.markdown("""
- ✅ Hệ thống đăng nhập/đăng ký
- ✅ Giao diện chat với AI
- ✅ Upload file đính kèm
- ✅ Lịch sử chat
- ✅ Quản lý profile người dùng
- ✅ Cài đặt tùy chỉnh (màu sắc, theme)
- ✅ Nút ghi âm (placeholder)
- ✅ Responsive design
""")

st.write("### Tài khoản mẫu:")
st.code("Email: admin@example.com\nMật khẩu: admin123")

st.write("### Cấu trúc dự án:")
st.code("""
Project/
├── app.py                 # File chính
├── config.py             # Cấu hình
├── auth.py               # Xác thực
├── chat_utils.py         # Chat & file upload
├── profile_settings.py   # Profile & settings
├── requirements.txt      # Dependencies
└── README.md            # Hướng dẫn
""")


