import streamlit as st
from auth import get_user_info, update_user_info
from config import CHAT_COLORS, save_config, load_config

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
            # Reset trạng thái xem lịch sử đầy đủ khi chuyển menu
            if menu_id != "chat":
                st.session_state.show_full_history = False
            st.rerun()
    
    # Nút đăng xuất
    st.markdown("---")
    if st.button("🚪 Đăng xuất", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.rerun()
    
    return st.session_state.selected_menu

def show_user_profile(user_email):
    """Hiển thị trang hồ sơ người dùng"""
    st.markdown("### 👤 Hồ sơ người dùng")
    
    user_info = get_user_info(user_email)
    
    if not user_info:
        st.error("Không thể tải thông tin người dùng!")
        return
    
    # Hiển thị thông tin cơ bản
    with st.container():
        st.markdown(f"""
        <div class="profile-section">
            <h4>Thông tin cơ bản</h4>
            <p><strong>Họ tên:</strong> {user_info.get('name', 'Chưa cập nhật')}</p>
            <p><strong>Email:</strong> {user_email}</p>
            <p><strong>Ngày tham gia:</strong> {user_info.get('created_at', 'Không xác định')}</p>
            <p><strong>Đăng nhập gần nhất:</strong> {user_info.get('last_login', 'Không xác định')}</p>
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
        # Cài đặt màu sắc
        st.markdown("#### 🎨 Màu sắc")
        chat_color = st.selectbox(
            "Màu chủ đạo",
            options=list(CHAT_COLORS.keys()),
            index=list(CHAT_COLORS.keys()).index(config.get("chat_color", "Blue"))
        )
        
        # Cài đặt font chữ
        st.markdown("#### 📝 Font chữ")
        font_size = st.radio(
            "Kích thước font chữ",
            options=["Small", "Medium", "Large"],
            index=["Small", "Medium", "Large"].index(config.get("font_size", "Medium"))
        )
        
        # Nút lưu cài đặt
        save_submitted = st.form_submit_button("Lưu cài đặt", type="primary")
        
        if save_submitted:
            # Cập nhật cấu hình
            config["chat_color"] = chat_color
            config["font_size"] = font_size
            
            # Lưu cấu hình
            save_config(config)
            
            st.success("Đã lưu cài đặt!")
            st.rerun()

def apply_custom_css(config):
    """Áp dụng CSS tùy chỉnh dựa trên cấu hình"""
    font_size = config.get("font_size", "Medium")
    
    # Áp dụng kích thước font chữ
    font_size_map = {
        "Small": "0.9rem",
        "Medium": "1rem",
        "Large": "1.1rem"
    }
    
    base_font_size = font_size_map.get(font_size, "1rem")
    
    st.markdown(f"""
    <style>
    .stTextInput input, .stTextArea textarea, .stSelectbox, .stMultiselect, p, div {{
        font-size: {base_font_size} !important;
    }}
    </style>
    """, unsafe_allow_html=True)