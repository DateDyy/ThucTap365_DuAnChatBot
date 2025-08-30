import streamlit as st
from datetime import datetime
from config import load_css, load_config, CHAT_COLORS
from login_form import show_login_form
from register_form import show_register_form
from chat_utils import create_chat_interface, display_chat_history_sidebar
from profile_settings import (
    show_user_profile, 
    show_settings, 
    show_sidebar_menu, 
    show_user_info_sidebar,
    apply_custom_css
)

<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
def main():
    """Hàm chính của ứng dụng"""
    
    # Load CSS và cấu hình
    load_css()
    config = load_config()
    apply_custom_css(config)
    
    # Header chính
    st.markdown("""
    <div class="main-header">
        AI Chat Assistant
    </div>
    """, unsafe_allow_html=True)
    
    # Kiểm tra trạng thái đăng nhập
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'show_register' not in st.session_state:
        st.session_state.show_register = False
    
    if 'show_full_history' not in st.session_state:
        st.session_state.show_full_history = False
    
<<<<<<< Updated upstream
    if 'selected_menu' not in st.session_state:
        st.session_state.selected_menu = "chat"   # Mặc định mở giao diện chat
    
    # Hiển thị form đăng nhập/đăng ký nếu chưa đăng nhập
    if not st.session_state.logged_in:
=======
    # Hiển thị form đăng nhập/đăng ký nếu chưa đăng nhập
    if not st.session_state.logged_in:
        # Hỗ trợ mở form đăng ký qua query params (?view=register=1)
>>>>>>> Stashed changes
        try:
            query_params = st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
            view_param = query_params.get("view")
            if view_param == ["register"] or view_param == "register":
                st.session_state.show_register = True
        except Exception:
            pass

        if st.session_state.show_register:
            show_register_form()
        else:
            show_login_form()
        return
    
    # Nếu đã đăng nhập, hiển thị giao diện chính
    user_email = st.session_state.user_email
    
    # Sidebar
    with st.sidebar:
        # Thông tin người dùng
        show_user_info_sidebar(user_email)
        
        st.markdown("---")
        
        # Menu chính
        selected_menu = show_sidebar_menu(user_email)
<<<<<<< Updated upstream
        st.session_state.selected_menu = selected_menu  # lưu trạng thái menu
        
        # Nút Chat mới luôn hiển thị
        # if st.button("➕ Chat mới", type="primary", use_container_width=True):
        #     st.session_state.selected_menu = "chat"
        #     st.session_state.show_full_history = False
        #     st.rerun()
        
        st.markdown("---")
        
        # Lịch sử trò chuyện
        display_chat_history_sidebar(user_email, config.get("chat_color", "Blue"))
    
    # Main content area
    if st.session_state.selected_menu == "chat":
=======
    
    # Main content area
    if selected_menu == "chat":
        # Kiểm tra nếu người dùng muốn xem lịch sử đầy đủ
>>>>>>> Stashed changes
        if st.session_state.show_full_history:
            st.markdown("### 📚 Lịch sử chat đầy đủ")
            
            from chat_utils import get_chat_history, group_messages_by_conversation
            chat_history = get_chat_history(user_email)
            
            if not chat_history:
                st.info("Chưa có lịch sử chat nào.")
            else:
<<<<<<< Updated upstream
                conversations = group_messages_by_conversation(chat_history)
                for i, conversation in enumerate(reversed(conversations)):
=======
                # Nhóm tin nhắn theo cuộc trò chuyện
                conversations = group_messages_by_conversation(chat_history)
                
                # Hiển thị các cuộc trò chuyện theo thứ tự mới nhất
                for i, conversation in enumerate(reversed(conversations)):
                    # Thông tin cuộc trò chuyện
>>>>>>> Stashed changes
                    conversation_start = conversation[0]["timestamp"]
                    conversation_end = conversation[-1]["timestamp"]
                    message_count = len(conversation)
                    
                    try:
                        start_dt = datetime.fromisoformat(conversation_start)
                        end_dt = datetime.fromisoformat(conversation_end)
                        date_str = start_dt.strftime("%d/%m/%Y")
                        time_range = f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
                    except:
                        date_str = "Unknown"
                        time_range = "Unknown"
                    
<<<<<<< Updated upstream
=======
                    # Header cuộc trò chuyện
>>>>>>> Stashed changes
                    st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid {CHAT_COLORS[config.get('chat_color', 'Blue')]};">
                        <strong>📅 Cuộc trò chuyện {len(conversations) - i}</strong><br>
                        <small>🕐 {date_str} | {time_range} | 💬 {message_count} tin nhắn</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
<<<<<<< Updated upstream
=======
                    # Hiển thị tin nhắn trong cuộc trò chuyện
>>>>>>> Stashed changes
                    for message in conversation:
                        from chat_utils import display_chat_message
                        display_chat_message(message, config.get("chat_color", "Blue"))
                    
                    st.markdown("---")
                
<<<<<<< Updated upstream
=======
                # Nút quay lại chat
>>>>>>> Stashed changes
                if st.button("🔙 Quay lại chat", type="primary"):
                    st.session_state.show_full_history = False
                    st.rerun()
        else:
<<<<<<< Updated upstream
            create_chat_interface(user_email, config.get("chat_color", "Blue"))
    
    elif st.session_state.selected_menu == "profile":
        show_user_profile(user_email)
    
    elif st.session_state.selected_menu == "settings":
        show_settings()
    
    elif st.session_state.selected_menu == "history":
        st.markdown("### 📚 Lịch sử chat chi tiết")
=======
            # Giao diện chat chính
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Chat interface
                create_chat_interface(user_email, config.get("chat_color", "Blue"))
            
            with col2:
                # Chat history sidebar
                display_chat_history_sidebar(user_email, config.get("chat_color", "Blue"))
    
    elif selected_menu == "profile":
        # Giao diện profile
        show_user_profile(user_email)
    
    elif selected_menu == "settings":
        # Giao diện settings
        show_settings()
    
    elif selected_menu == "history":
        # Giao diện lịch sử chat chi tiết
        st.markdown("### 📚 Lịch sử chat chi tiết")
        
>>>>>>> Stashed changes
        from chat_utils import get_chat_history, group_messages_by_conversation
        chat_history = get_chat_history(user_email)
        
        if not chat_history:
            st.info("Chưa có lịch sử chat nào.")
        else:
<<<<<<< Updated upstream
            conversations = group_messages_by_conversation(chat_history)
            for i, conversation in enumerate(reversed(conversations)):
=======
            # Nhóm tin nhắn theo cuộc trò chuyện
            conversations = group_messages_by_conversation(chat_history)
            
            # Hiển thị các cuộc trò chuyện theo thứ tự mới nhất
            for i, conversation in enumerate(reversed(conversations)):
                # Thông tin cuộc trò chuyện
>>>>>>> Stashed changes
                conversation_start = conversation[0]["timestamp"]
                conversation_end = conversation[-1]["timestamp"]
                message_count = len(conversation)
                
                try:
                    start_dt = datetime.fromisoformat(conversation_start)
                    end_dt = datetime.fromisoformat(conversation_end)
                    date_str = start_dt.strftime("%d/%m/%Y")
                    time_range = f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
                except:
                    date_str = "Unknown"
                    time_range = "Unknown"
                
<<<<<<< Updated upstream
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 15px 0; color: black; border: 1px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 4px solid {CHAT_COLORS[config.get('chat_color', 'Blue')]};">
=======
                # Header cuộc trò chuyện
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid {CHAT_COLORS[config.get('chat_color', 'Blue')]};">
>>>>>>> Stashed changes
                    <strong>📅 Cuộc trò chuyện {len(conversations) - i}</strong><br>
                    <small>🕐 {date_str} | {time_range} | 💬 {message_count} tin nhắn</small>
                </div>
                """, unsafe_allow_html=True)
                
<<<<<<< Updated upstream
=======
                # Hiển thị tin nhắn trong cuộc trò chuyện
>>>>>>> Stashed changes
                for message in conversation:
                    from chat_utils import display_chat_message
                    display_chat_message(message, config.get("chat_color", "Blue"))
                
                st.markdown("---")

<<<<<<< Updated upstream

if __name__ == "__main__":
    main()
=======
if __name__ == "__main__":
    main()
>>>>>>> Stashed changes
