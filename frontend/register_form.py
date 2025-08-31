import streamlit as st
from auth import register_user

def show_register_form():
    """Hiển thị form đăng ký (giao diện tách riêng)"""
    # Wrapper cố định chiều rộng cho form để đồng nhất giữa các trang
    st.markdown("""
    <div class='auth-form-wrapper' style='max-width: 520px; margin: 0 auto;'>
    """, unsafe_allow_html=True)

    with st.form("register_form"):
        st.markdown(
            """
            <div style=\"text-align:center; font-weight:700; font-size:1.5rem; margin: 6px 0 8px 0;\">ĐĂNG KÝ</div>
            """,
            unsafe_allow_html=True,
        )

        name = st.text_input("Họ tên", placeholder="Nhập họ tên của bạn")
        email = st.text_input("Email", placeholder="Nhập email của bạn")
        password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu")
        confirm_password = st.text_input("Xác nhận mật khẩu", type="password", placeholder="Nhập lại mật khẩu")

        # Nút đăng ký: full width trong wrapper để nhìn cân đối và ở giữa
        register_submitted = st.form_submit_button("Đăng ký", type="primary", use_container_width=True)

        # Link đăng nhập dưới nút đăng ký với margin-top nhỏ


        if register_submitted:
            if name and email and password and confirm_password:
                if password != confirm_password:
                    st.error("Mật khẩu xác nhận không khớp!")
                else:
                    success, message = register_user(email, password, name)
                    if success:
                        # Lưu thông tin đăng ký thành công vào session state
                        st.session_state.registration_success = True
                        st.session_state.registration_email = email
                        st.session_state.registration_name = name
                        
                        # Hiển thị thông báo thành công với nhiều thông tin hơn
                        st.success(f"🎉 {message} Chào mừng {name}!")
                        
                        # Thêm hướng dẫn đăng nhập
                        st.info("Bạn sẽ được chuyển đến trang đăng nhập trong vài giây...")
                        
                        # Đặt hẹn giờ chuyển về form đăng nhập
                        import time
                        time.sleep(2)  # Dừng 2 giây để người dùng đọc thông báo
                        
                        # Chuyển hướng đến trang đăng nhập bằng cách thay đổi query parameter
                        try:
                            if hasattr(st, "query_params"):
                                st.query_params.update({"view": "login"})
                            else:
                                st.experimental_set_query_params(view="login")
                        except Exception:
                            pass
                        
                        # Thêm JavaScript để đảm bảo chuyển hướng
                        js_redirect = """
                        <script>
                            // Chuyển hướng đến trang đăng nhập
                            window.location.href = '?view=login';
                        </script>
                        """
                        st.markdown(js_redirect, unsafe_allow_html=True)
                        
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.error("Vui lòng nhập đầy đủ thông tin!")

    # Đóng wrapper
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)
    
    # Thêm nút đăng nhập bên ngoài form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        login_button = st.button("Đã có tài khoản? Đăng nhập", key="login_from_register", use_container_width=True)
    
    if login_button:
        st.session_state.show_register = False
        st.rerun()