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
        st.markdown(
            "<div style='text-align:center; margin-top: 4px; margin-bottom: 25px;'>Đã có tài khoản? "
            "<a href='/'>Đăng nhập</a></div>",
            unsafe_allow_html=True,
        )

        if register_submitted:
            if name and email and password and confirm_password:
                if password != confirm_password:
                    st.error("Mật khẩu xác nhận không khớp!")
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

    # Đóng wrapper
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)