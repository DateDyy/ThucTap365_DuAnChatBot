import streamlit as st
import bcrypt
import json
from datetime import datetime
from config import load_user_data, save_user_data

def hash_password(password):
    """Mã hóa mật khẩu"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    """Xác thực mật khẩu"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def register_user(email, password, name):
    """Đăng ký người dùng mới"""
    users_data = load_user_data()
    
    if email in users_data:
        return False, "Email đã tồn tại!"
    
    # Mã hóa mật khẩu
    hashed_password = hash_password(password)
    
    # Tạo thông tin người dùng mới
    new_user = {
        "name": name,
        "password": hashed_password,
        "avatar": "👤",
        "created_at": datetime.now().isoformat(),
        "last_login": datetime.now().isoformat()
    }
    
    users_data[email] = new_user
    save_user_data(users_data)
    
    return True, "Đăng ký thành công!"

def login_user(email, password):
    """Đăng nhập người dùng"""
    users_data = load_user_data()
    
    if email not in users_data:
        return False, "Email không tồn tại!"
    
    user = users_data[email]
    
    if not verify_password(password, user["password"]):
        return False, "Mật khẩu không đúng!"
    
    # Cập nhật thời gian đăng nhập cuối
    user["last_login"] = datetime.now().isoformat()
    save_user_data(users_data)
    
    return True, "Đăng nhập thành công!"

def update_user_profile(email, name=None, avatar=None):
    """Cập nhật thông tin người dùng"""
    users_data = load_user_data()
    
    if email not in users_data:
        return False, "Người dùng không tồn tại!"
    
    if name:
        users_data[email]["name"] = name
    if avatar:
        users_data[email]["avatar"] = avatar
    
    save_user_data(users_data)
    return True, "Cập nhật thành công!"

def get_user_info(email):
    """Lấy thông tin người dùng"""
    users_data = load_user_data()
    return users_data.get(email, None)

def show_login_form():
    """Hiển thị form đăng nhập"""
    left, center, right = st.columns([1, 2, 1])
    with center:
        with st.form("login_form"):
            # CSS: Center the submit button inside this form
            st.markdown(
                """
                <style>
                div[data-testid="stForm"] .stButton > button {
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                <div style=\"text-align:center; font-weight:700; font-size:1.5rem; margin: 6px 0 8px 0;\">ĐĂNG NHẬP</div>
                """,
                unsafe_allow_html=True,
            )
            email = st.text_input("Email", placeholder="Nhập email của bạn")
            password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu")

            # Link Quên mật khẩu: căn phải, nằm ngay dưới input mật khẩu
            st.markdown(
                """
                <div style=\"text-align:right; margin-top: 2px;\">
                    <a href='?view=forgot'>Quên mật khẩu?</a>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Nút đăng nhập giữa khung
            btn_left, btn_mid, btn_right = st.columns([1, 1, 1])
            with btn_mid:
                login_submitted = st.form_submit_button("Đăng nhập", type="primary")

            # Link đăng ký dưới nút đăng nhập, khoảng cách nhỏ hơn
            st.markdown(
                "<div style='text-align:center; margin-top: 4px; margin-bottom: 12px;'>Chưa có tài khoản? "
                "<a href='?view=register'>Đăng ký</a></div>",
                unsafe_allow_html=True,
            )

            if login_submitted:
                if email and password:
                    success, message = login_user(email, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Vui lòng nhập đầy đủ thông tin!")

            # Nếu người dùng mở view=forgot thì hiển thị hướng dẫn
            try:
                query_params = st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
                view_param = query_params.get("view")
                if view_param == ["forgot"] or view_param == "forgot":
                    st.info("Vui lòng liên hệ quản trị để đặt lại mật khẩu hoặc sử dụng email khôi phục nếu có.")
            except Exception:
                pass

def show_register_form():
    """Hiển thị form đăng ký"""
    left, center, right = st.columns([1, 2, 1])

    with center:
        with st.form("register_form"):
            # CSS: center submit button in this form
            st.markdown(
                """
                <style>
                div[data-testid=\"stForm\"] .stButton > button {
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            # Link quay lại: top-left, canh theo lề form
            st.markdown(
                """
                <div style=\"text-align:left; margin: 4px 0 0 0;\">
                    <a href='?'>← Quay lại đăng nhập</a>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div style=\"text-align:center; font-weight:700; font-size:1.5rem; margin: 6px 0 8px 0;\">ĐĂNG KÝ</div>
                """,
                unsafe_allow_html=True,
            )

            name = st.text_input("Họ và tên", placeholder="Nhập họ và tên")
            email = st.text_input("Email", placeholder="Nhập email")
            password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu")
            confirm_password = st.text_input("Xác nhận mật khẩu", type="password", placeholder="Nhập lại mật khẩu")

            register_submitted = st.form_submit_button("Đăng ký", type="primary")
        
        if register_submitted:
            if name and email and password and confirm_password:
                if password != confirm_password:
                    st.error("Mật khẩu xác nhận không khớp!")
                elif len(password) < 6:
                    st.error("Mật khẩu phải có ít nhất 6 ký tự!")
                else:
                    success, message = register_user(email, password, name)
                    if success:
                        st.success(message)
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.error("Vui lòng nhập đầy đủ thông tin!")

def logout():
    """Đăng xuất"""
    if 'logged_in' in st.session_state:
        del st.session_state.logged_in
    if 'user_email' in st.session_state:
        del st.session_state.user_email
    st.rerun()
