import streamlit as st
from auth import login_user


def show_login_form():
    """Hiển thị form đăng nhập (giao diện tách riêng)"""
    # Wrapper cố định chiều rộng cho form để đồng nhất giữa các trang
<<<<<<< Updated upstream
 

    with st.form("login_form"):
        st.markdown(
                    """
                    <div style=\"text-align:center; font-weight:700; font-size:1.5rem; margin: 6px 0 8px 0;\">ĐĂNG NHẬP</div>
                    """,
                    unsafe_allow_html=True,
                )

        email = st.text_input("Email", placeholder="Nhập email của bạn", key="email_input")
        password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu", key="password_input")

        st.markdown(
            """
            <div style=\"text-align:right; margin-top: 2px; margin-bottom: 5px;\">
                <a href='?view=forgot' style='color: #555; text-decoration: none;'>Quên mật khẩu?</a>
=======
    st.markdown("""
    <div class='auth-form-wrapper' style='max-width: 520px; margin: 0 auto;'>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        st.markdown(
            """
            <div style=\"text-align:center; font-weight:700; font-size:1.5rem; margin: 6px 0 8px 0;\">ĐĂNG NHẬP</div>
            """,
            unsafe_allow_html=True,
        )

        email = st.text_input("Email", placeholder="Nhập email của bạn")
        password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu")

        # Link Quên mật khẩu: căn phải, ngay dưới password
        st.markdown(
            """
            <div style=\"text-align:right; margin-top: 2px; margin-bottom: 5px;\">
                <a href='?view=forgot'>Quên mật khẩu?</a>
>>>>>>> Stashed changes
            </div>
            """,
            unsafe_allow_html=True,
        )

<<<<<<< Updated upstream
        login_submitted = st.form_submit_button("Đăng nhập", type="primary", use_container_width=True)

        st.markdown(
            "<div style='text-align:center; margin-top: 1rem; margin-bottom: 1rem; color: #555;'>Chưa có tài khoản? "
            "<a href='?view=register' style='color: #0068c9; text-decoration: none;'>Đăng ký</a></div>",
=======
        # Nút đăng nhập: full width trong wrapper để nhìn cân đối và ở giữa
        login_submitted = st.form_submit_button("Đăng nhập", type="primary", use_container_width=True)

        # Link đăng ký dưới nút đăng nhập với margin-top nhỏ
        st.markdown(
            "<div style='text-align:center; margin-top: 4px; margin-bottom: 25px;'>Chưa có tài khoản? "
            "<a href='?view=register'>Đăng ký</a></div>",
>>>>>>> Stashed changes
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

    # Đóng wrapper
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

    # Gợi ý nếu mở view=forgot
    try:
        query_params = st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
        view_param = query_params.get("view")
        if view_param == ["forgot"] or view_param == "forgot":
            st.info("Vui lòng liên hệ quản trị để đặt lại mật khẩu hoặc sử dụng email khôi phục nếu có.")
    except Exception:
        pass