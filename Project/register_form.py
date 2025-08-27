import streamlit as st
from auth import register_user


def show_register_form():
    """Hiển thị form đăng ký (giao diện tách riêng)"""
    # Wrapper cố định chiều rộng cho form để đồng nhất giữa các trang
    st.markdown(
        """
        <div class='auth-form-wrapper' style='max-width: 520px; margin: 0 auto;'>
        """,
        unsafe_allow_html=True,
    )

    with st.form("register_form"):
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
                <div style=\"text-align:center; font-weight:700; font-size:1.5rem; margin: 12px 0 30px 0;\">ĐĂNG KÝ</div>
                """,
                unsafe_allow_html=True,
            )

            name = st.text_input("Họ và tên", placeholder="Nhập họ và tên")
            email = st.text_input("Email", placeholder="Nhập email")
            password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu")
            confirm_password = st.text_input("Xác nhận mật khẩu", type="password", placeholder="Nhập lại mật khẩu")

            register_submitted = st.form_submit_button("Đăng ký", type="primary", use_container_width=True)
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

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

    # Đóng wrapper
    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True,
    )


