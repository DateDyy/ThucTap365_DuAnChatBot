import streamlit as st
from datetime import datetime
from auth import get_user_info, update_user_info
from config import CHAT_COLORS, save_config, load_config


def format_datetime(date_str):
    """Chuyển ISO datetime thành dd/mm/YYYY HH:MM:SS (bỏ T và microseconds)"""
    if not date_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(str(date_str))
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    except Exception:
        return str(date_str)


def show_user_info_sidebar(user_email):
    """Hiển thị thông tin người dùng ở sidebar"""
    user_info = get_user_info(user_email)

    if user_info:
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="width: 80px; height: 80px; background-color: #1f77b4; color: white; 
                 border-radius: 50%; margin: 0 auto; display: flex; align-items: center; 
                 justify-content: center; font-size: 2rem;">
                {user_info.get('name', 'User')[0].upper()}
            </div>
            <div style="margin-top: 10px; font-weight: bold;">
                {user_info.get('name', 'User')}
            </div>
            <div style="font-size: 0.8rem; opacity: 0.7;">
                {user_email}
            </div>
            <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 5px;">
                Lần đăng nhập gần nhất: {format_datetime(user_info.get('last_login'))}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center;">
            <div style="width: 80px; height: 80px; background-color: #1f77b4; color: white; 
                 border-radius: 50%; margin: 0 auto; display: flex; align-items: center; 
                 justify-content: center; font-size: 2rem;">
                U
            </div>
            <div style="margin-top: 10px; font-weight: bold;">
                Người dùng
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_sidebar_menu(user_email):
    """Hiển thị menu chính ở sidebar"""
    menu_options = {
        "chat": "💬 Chat mới",
        "profile": "👤 Hồ sơ",
        "settings": "⚙️ Cài đặt"
    }

    # Mặc định chọn chat
    if "selected_menu" not in st.session_state:
        st.session_state.selected_menu = "chat"

    # Hiển thị các nút menu
    for menu_id, menu_label in menu_options.items():
        if st.button(
            menu_label,
            key=f"menu_{menu_id}",
            use_container_width=True,
            type="primary" if st.session_state.selected_menu == menu_id else "secondary"
        ):
            st.session_state.selected_menu = menu_id

            # Nếu bấm Chat mới → reset trạng thái hội thoại
            if menu_id == "chat":
                st.session_state.new_conversation = True
                st.session_state.active_conversation_id = None
                st.session_state.messages = []

            # Nếu không phải chat → reset cờ show_full_history
            if menu_id != "chat":
                st.session_state.show_full_history = False

            st.rerun()

    # Nút đăng xuất
    st.markdown("---")
    if st.button("🚪 Đăng xuất", use_container_width=True):
        # Xóa token đăng nhập nếu có
        if 'login_token' in st.session_state and st.session_state.login_token:
            from auth import remove_login_token
            remove_login_token(st.session_state.login_token)
        
        # Xóa token khỏi URL
        try:
            if hasattr(st, "query_params"):
                st.query_params.clear()
            else:
                st.experimental_set_query_params()
        except Exception:
            pass
        
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.login_token = None
        st.rerun()

    return st.session_state.selected_menu


def show_user_profile(user_email):
    """Hiển thị trang hồ sơ người dùng"""
    st.markdown("### 👤 Hồ sơ người dùng")

    user_info = get_user_info(user_email)

    if not user_info:
        st.error("Không thể tải thông tin người dùng!")
        return

    # Lấy màu chủ đạo từ config
    config = load_config()
    primary_color = CHAT_COLORS.get(config.get("chat_color", "Blue"), "#1f77b4")

    # Hiển thị thông tin cơ bản (dùng màu đồng bộ)
    with st.container():
        st.markdown(f"""
        <div class="profile-section" 
             style="background-color: {primary_color}20; 
                    border: 1px solid {primary_color}; 
                    border-radius: 10px; 
                    padding: 15px; 
                    margin-bottom: 15px;
                    color: inherit;">
            <h4 style="color: {primary_color}; margin-bottom: 10px;">Thông tin cơ bản</h4>
            <p><strong>Họ tên:</strong> {user_info.get('name', 'Chưa cập nhật')}</p>
            <p><strong>Email:</strong> {user_email}</p>
            <p><strong>Ngày tham gia:</strong> {format_datetime(user_info.get('created_at'))}</p>
            <p><strong>Đăng nhập gần nhất:</strong> {format_datetime(user_info.get('last_login'))}</p>
        </div>
        """, unsafe_allow_html=True)

    # Form cập nhật thông tin
    st.markdown("### ✏️ Cập nhật thông tin")

    with st.form("update_profile_form"):
        name = st.text_input("Họ tên", value=user_info.get('name', ''))

        update_submitted = st.form_submit_button("Cập nhật", type="primary")

        if update_submitted:
            success, message = update_user_info(user_email, name)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)


def show_settings():
    """Hiển thị trang cài đặt"""
    st.markdown("### ⚙️ Cài đặt")

    # Tải cấu hình hiện tại
    config = load_config()

    with st.form("settings_form"):
        # Cài đặt chế độ sáng/tối
        st.markdown("#### 🌓 Chế độ giao diện")
        theme_mode = st.radio(
            "Chế độ giao diện",
            options=["Sáng", "Tối"],
            index=0 if config.get("theme_mode", "Sáng") == "Sáng" else 1,
            horizontal=True
        )
        
        # Cài đặt màu sắc
        st.markdown("#### 🎨 Màu sắc")
        chat_color = st.selectbox(
            "Màu chủ đạo",
            options=list(CHAT_COLORS.keys()),
            index=list(CHAT_COLORS.keys()).index(config.get("chat_color", "Blue"))
        )
        
        # Màu nền thẻ tin nhắn
        # message_bg_color = st.selectbox(
        #     "Màu nền thẻ tin nhắn",
        #     options=["Mặc định", "Xanh nhạt", "Xám nhạt", "Hồng nhạt", "Tím nhạt", "Vàng nhạt"],
        #     index=["Mặc định", "Xanh nhạt", "Xám nhạt", "Hồng nhạt", "Tím nhạt", "Vàng nhạt"].index(config.get("message_bg_color", "Mặc định"))
        # )
        
        # Màu nút
        button_color = st.selectbox(
            "Màu nút",
            options=["Default", "Blue", "Red", "Purple", "Orange", "Green"],
            index=["Default", "Blue", "Red", "Purple", "Orange", "Green"].index(config.get("button_color", "Default"))
        )


        # # Cài đặt font chữ
        # st.markdown("#### 📝 Font chữ")
        # font_size = st.radio(
        #     "Kích thước font chữ",
        #     options=["Nhỏ", "Vừa", "Lớn"],
        #     index=["Nhỏ", "Vừa", "Lớn"].index(config.get("font_size", "Vừa"))
        # )
        
        # # Cài đặt tự động cuộn
        # st.markdown("#### 📜 Tùy chọn cuộn")
        # auto_scroll = st.checkbox(
        #     "Tự động cuộn xuống tin nhắn mới",
        #     value=config.get("auto_scroll", True)
        # )

        # Nút lưu cài đặt
        save_submitted = st.form_submit_button("Lưu cài đặt", type="primary")

        if save_submitted:
            # Cập nhật cấu hình
            config["theme_mode"] = theme_mode
            config["chat_color"] = chat_color
            # config["message_bg_color"] = message_bg_color
            config["button_color"] = button_color
            # config["font_size"] = font_size
            # config["auto_scroll"] = auto_scroll

            # Lưu cấu hình
            save_config(config)

            st.success("Đã lưu cài đặt!")
            st.rerun()


def apply_custom_css(config):
    """Áp dụng CSS tùy chỉnh dựa trên cấu hình"""
    # Lấy các cài đặt từ config
    theme_mode = config.get("theme_mode", "Sáng")
    font_size = config.get("font_size", "Vừa")
    message_bg_color = config.get("message_bg_color", "Mặc định")
    button_color = config.get("button_color", "Mặc định")
    chat_color = config.get("chat_color", "Blue")
    primary_color = CHAT_COLORS.get(chat_color, "#1f77b4")

    # Áp dụng kích thước font chữ
    font_size_map = {
        "Nhỏ": "0.9rem",
        "Vừa": "1rem",
        "Lớn": "1.1rem"
    }

    base_font_size = font_size_map.get(font_size, "1rem")
    
    # Màu nền thẻ tin nhắn
    message_bg_color_map = {
        "Mặc định": "#f0f2f5",
        "Xanh nhạt": "#e3f2fd",
        "Xám nhạt": "#f5f5f5",
        "Hồng nhạt": "#fce4ec",
        "Tím nhạt": "#f3e5f5",
        "Vàng nhạt": "#fffde7"
    }
    
    # Màu nút
    button_color_map = {
        "Default": primary_color,
        "Blue": "#2196F3",
        "Red": "#F44336",
        "Purple": "#9C27B0",
        "Orange": "#FF9800",
        "Green": "#4CAF50"
    }

    
    # Chọn màu dựa trên chế độ sáng/tối
    if theme_mode == "Tối":
        bg_color = "#121212"
        text_color = "#ffffff"
        card_bg_color = "#1e1e1e"
        border_color = "#333333"
        sidebar_bg = "#0e0e0e"
        input_bg = "#2d2d2d"
    else:
        bg_color = "#ffffff"
        text_color = "#000000"
        card_bg_color = "#ffffff"
        border_color = "#e6e6e6"
        sidebar_bg = "#f8f9fa"
        input_bg = "#f0f2f5"
    
    # Màu nền thẻ tin nhắn tùy chỉnh
    msg_bg_color = message_bg_color_map.get(message_bg_color, "#f0f2f5")
    if theme_mode == "Tối" and message_bg_color == "Default":
        msg_bg_color = "#2d2d2d"
    
    # Màu nút tùy chỉnh
    btn_color = button_color_map.get(button_color, primary_color)

    # Áp dụng CSS
    st.markdown(f"""
    <style>
    /* Font size */
    .stTextInput input, .stTextArea textarea, .stSelectbox, .stMultiselect, p, div {{
        font-size: {base_font_size} !important;
    }}
    
    /* Theme mode */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    
    .stSidebar {{
        background-color: {sidebar_bg};
    }}
    
    /* Card styling */
    div.stCard {{
        background-color: {card_bg_color};
        border-color: {border_color};
        
    }}
    
    /* Input fields */
    .stTextInput input, .stTextArea textarea {{
        background-color: {input_bg};
        border-color: {border_color};
        color: {text_color};
    }}
    
    /* Message styling */
    .message-container {{
        background-color: {msg_bg_color};

    }}
    
    /* Button styling */
    .stButton button[data-baseweb="button"],
    .stButton button,
    button.st-emotion-cache-19rxjzo,
    button.st-emotion-cache-1erivf3,
    button.st-emotion-cache-7ym5gk,
    button.st-emotion-cache-1aumxhf {{
        background-color: {btn_color} !important;
        
    }}
    </style>
    """, unsafe_allow_html=True)
