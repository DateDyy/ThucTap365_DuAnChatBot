import streamlit as st
from datetime import datetime
from auth import get_user_info, update_user_profile
from config import load_config, save_config, CHAT_COLORS

def show_user_profile(user_email):
    """Hiển thị thông tin profile người dùng"""
    st.markdown("### 👤 Thông tin tài khoản")
    
    user_info = get_user_info(user_email)
    if not user_info:
        st.error("Không thể tải thông tin người dùng!")
        return
    
    # Hiển thị thông tin hiện tại
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Avatar
        avatar = user_info.get("avatar", "👤")
        st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 4rem; margin-bottom: 10px;">{avatar}</div>
            <small>Avatar hiện tại</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Thông tin cá nhân:**")
        st.write(f"**Tên:** {user_info.get('name', 'N/A')}")
        st.write(f"**Email:** {user_email}")
        
        # Thời gian tạo tài khoản
        created_at = user_info.get("created_at", "")
        if created_at:
            try:
                dt = datetime.fromisoformat(created_at)
                st.write(f"**Ngày tạo:** {dt.strftime('%d/%m/%Y %H:%M')}")
            except:
                st.write(f"**Ngày tạo:** {created_at}")
        
        # Thời gian đăng nhập cuối
        last_login = user_info.get("last_login", "")
        if last_login:
            try:
                dt = datetime.fromisoformat(last_login)
                st.write(f"**Đăng nhập cuối:** {dt.strftime('%d/%m/%Y %H:%M')}")
            except:
                st.write(f"**Đăng nhập cuối:** {last_login}")
    
    st.markdown("---")
    
    # Form cập nhật thông tin
    st.markdown("### ✏️ Cập nhật thông tin")
    
    with st.form("update_profile_form"):
        new_name = st.text_input(
            "Tên mới",
            value=user_info.get("name", ""),
            placeholder="Nhập tên mới"
        )
        
        # Avatar selection
        st.markdown("**Chọn avatar mới:**")
        avatar_options = ["👤", "👨", "👩", "🧑", "👨‍💻", "👩‍💻", "🤖", "😊", "😎", "🎭"]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        selected_avatar = user_info.get("avatar", "👤")
        
        for i, avatar in enumerate(avatar_options):
            col = [col1, col2, col3, col4, col5][i % 5]
            with col:
                if st.radio(f"Avatar {i+1}", [avatar], label_visibility="collapsed"):
                    selected_avatar = avatar
        
        update_submitted = st.form_submit_button("Cập nhật thông tin", type="primary")
        
        if update_submitted:
            if new_name.strip():
                success, message = update_user_profile(user_email, new_name.strip(), selected_avatar)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Vui lòng nhập tên!")

def show_settings():
    """Hiển thị cài đặt ứng dụng"""
    st.markdown("### ⚙️ Cài đặt")
    
    config = load_config()
    
    with st.form("settings_form"):
        st.markdown("**Cài đặt giao diện:**")
        
        # Chọn màu chat
        chat_color = st.selectbox(
            "Màu sắc chat:",
            list(CHAT_COLORS.keys()),
            index=list(CHAT_COLORS.keys()).index(config.get("chat_color", "Blue"))
        )
        
        # Chọn theme
        theme = st.selectbox(
            "Giao diện:",
            ["light", "dark"],
            index=0 if config.get("theme", "light") == "light" else 1
        )
        
        # Chọn kích thước font
        font_size = st.selectbox(
            "Kích thước chữ:",
            ["small", "medium", "large"],
            index=["small", "medium", "large"].index(config.get("font_size", "medium"))
        )
        
        st.markdown("---")
        st.markdown("**Cài đặt chat:**")
        
        # Các tùy chọn chat
        auto_scroll = st.checkbox("Tự động cuộn xuống tin nhắn mới", value=True)
        show_timestamp = st.checkbox("Hiển thị thời gian tin nhắn", value=True)
        sound_notification = st.checkbox("Thông báo âm thanh", value=False)
        
        st.markdown("---")
        st.markdown("**Cài đặt bảo mật:**")
        
        # Cài đặt bảo mật
        session_timeout = st.selectbox(
            "Thời gian timeout phiên làm việc:",
            ["15 phút", "30 phút", "1 giờ", "2 giờ", "Không giới hạn"],
            index=1
        )
        
        save_submitted = st.form_submit_button("Lưu cài đặt", type="primary")
        
        if save_submitted:
            # Cập nhật cấu hình
            new_config = {
                "chat_color": chat_color,
                "theme": theme,
                "font_size": font_size,
                "auto_scroll": auto_scroll,
                "show_timestamp": show_timestamp,
                "sound_notification": sound_notification,
                "session_timeout": session_timeout
            }
            
            save_config(new_config)
            st.success("Đã lưu cài đặt thành công!")
            st.rerun()

def show_sidebar_menu(user_email):
    """Hiển thị menu sidebar"""
    st.sidebar.markdown("### 🎯 Menu chính")
    
    # Menu options (không dùng dropdown, dùng từng nút riêng)
    menu_options = [
<<<<<<< Updated upstream
=======
        ("💬 Chat", "chat"),
>>>>>>> Stashed changes
        ("👤 Profile", "profile"),
        ("⚙️ Settings", "settings"),
        ("📚 Lịch sử", "history"),
    ]

    # Trạng thái mục đã chọn
    if "selected_menu" not in st.session_state:
        st.session_state.selected_menu = "chat"

    # Hiển thị các nút chức năng
    for label, value in menu_options:
        is_active = st.session_state.selected_menu == value
        button_type = "primary" if is_active else "secondary"
        if st.sidebar.button(label, use_container_width=True, type=button_type, key=f"menu_btn_{value}"):
            st.session_state.selected_menu = value

    # Logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Đăng xuất", use_container_width=True):
        from auth import logout
        logout()
    
    return st.session_state.selected_menu

def show_user_info_sidebar(user_email):
    """Hiển thị thông tin người dùng trong sidebar"""
    user_info = get_user_info(user_email)
    if not user_info:
        return
    
    st.sidebar.markdown("### 👤 Thông tin người dùng")
    
    # Avatar và tên
    avatar = user_info.get("avatar", "👤")
    name = user_info.get("name", "Unknown")
    
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 10px;">
        <div style="font-size: 2rem; margin-bottom: 5px;">{avatar}</div>
        <strong>{name}</strong><br>
        <small>{user_email}</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Trạng thái online
    st.sidebar.markdown("🟢 **Trạng thái:** Online")
    
    # Thời gian đăng nhập cuối
    last_login = user_info.get("last_login", "")
    if last_login:
        try:
            dt = datetime.fromisoformat(last_login)
            st.sidebar.markdown(f"🕐 **Đăng nhập:** {dt.strftime('%H:%M')}")
        except:
            pass

def apply_custom_css(config):
    """Áp dụng CSS tùy chỉnh dựa trên cấu hình"""
    chat_color = config.get("chat_color", "Blue")
    theme = config.get("theme", "light")
    font_size = config.get("font_size", "medium")
    
    # Map font size
    font_sizes = {
        "small": "14px",
        "medium": "16px", 
        "large": "18px"
    }
    
    # Map theme colors
    theme_colors = {
        "light": {
            "bg": "#ffffff",
            "text": "#333333",
            "sidebar": "#f8f9fa"
        },
        "dark": {
            "bg": "#1e1e1e",
            "text": "#ffffff", 
            "sidebar": "#2d2d2d"
        }
    }
    
    theme_color = theme_colors.get(theme, theme_colors["light"])
    
    custom_css = f"""
    <style>
    .stApp {{
        background-color: {theme_color['bg']};
        color: {theme_color['text']};
        font-size: {font_sizes.get(font_size, '16px')};
    }}
    
    .css-1d391kg {{
        background-color: {theme_color['sidebar']};
    }}
    
    .user-message {{
        background-color: {CHAT_COLORS[chat_color]} !important;
    }}
    
    .stButton > button {{
        background-color: {CHAT_COLORS[chat_color]};
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
    }}
    
    .stButton > button:hover {{
        background-color: {CHAT_COLORS[chat_color]};
        opacity: 0.8;
    }}
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)
