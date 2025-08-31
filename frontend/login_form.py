import streamlit as st
from auth import login_user


def show_login_form():
    """Hiển thị form đăng nhập (giao diện tách riêng)"""
    # Wrapper với chiều rộng cố định phù hợp
    st.markdown("""
    <div style="width: 450px; margin: 0 auto; padding: 20px;">
    """, unsafe_allow_html=True)
    
    # Hiển thị form đăng nhập
    with st.form("login_form"):
        st.markdown(
                    """
                    <div style=\"text-align:center; font-weight:700; font-size:1.5rem; margin: 6px 0 8px 0;\">ĐĂNG NHẬP</div>
                    """,
                    unsafe_allow_html=True,
                )

        email = st.text_input("Email", placeholder="Nhập email của bạn", key="email_input")
        password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu", key="password_input")
        
        # Thêm tùy chọn "Remember me"
        remember_me = st.checkbox("Ghi nhớ đăng nhập", value=False, help="Đăng nhập sẽ được duy trì trong 30 ngày")

        st.markdown(
            """
            <div style=\"text-align:right; margin-top: 2px; margin-bottom: 5px;\">
                <a href='?view=forgot' style='color: #555; text-decoration: none;'>Quên mật khẩu?</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

        login_submitted = st.form_submit_button("Đăng nhập", type="primary", use_container_width=True)
        
        if login_submitted:
            if email and password:
                success, message, token = login_user(email, password, remember_me)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.login_token = token
                    
                    # Lưu token vào URL để duy trì trạng thái đăng nhập
                    try:
                        if hasattr(st, "query_params"):
                            st.query_params.update({"token": token})
                        else:
                            st.experimental_set_query_params(token=token)
                    except Exception:
                        pass
                    
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Vui lòng nhập đầy đủ thông tin!")

    # Thêm nút đăng ký ở cuối form đăng nhập
    st.markdown("<div style='text-align: center; margin-top: 10px;'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        register_button = st.button("Chưa có tài khoản? Đăng ký ngay", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if register_button:
        st.session_state.show_register = True
        st.rerun()

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