import subprocess
import threading
import time
import requests
import streamlit as st

def is_fastapi_running():
    """Kiểm tra xem FastAPI server đã chạy hay chưa."""
    try:
        response = requests.get("http://127.0.0.1:8000")
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        return False
    return False

def run_fastapi():
    """Khởi động FastAPI server."""
    subprocess.run(["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000"])

# Kiểm tra và chỉ khởi động FastAPI nếu chưa chạy
if "fastapi_started" not in st.session_state:
    if not is_fastapi_running():
        thread = threading.Thread(target=run_fastapi, daemon=True)
        thread.start()
        # Đợi một chút để FastAPI server khởi động
        time.sleep(3)
    st.session_state.fastapi_started = True

# Phần còn lại của ứng dụng Streamlit
st.title("Chatbot RAG")

# Đợi một chút để đảm bảo FastAPI đã sẵn sàng
time.sleep(1)

# Phần còn lại của mã nguồn ứng dụng Streamlit
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
from auth import validate_login_token, cleanup_expired_tokens

def get_query_params():
    """Lấy query parameters từ URL"""
    try:
        return st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
    except Exception:
        return {}

def set_query_params(params):
    """Đặt query parameters cho URL"""
    try:
        if hasattr(st, "query_params"):
            st.query_params.update(params)
        else:
            st.experimental_set_query_params(**params)
    except Exception:
        pass

def check_persistent_login():
    """Kiểm tra và khôi phục trạng thái đăng nhập từ token"""
    # Dọn dẹp token hết hạn
    cleanup_expired_tokens()
    
    # Kiểm tra token từ query parameters trước
    query_params = get_query_params()
    token_from_url = query_params.get("token", [None])[0] if isinstance(query_params.get("token"), list) else query_params.get("token")
    
    if token_from_url:
        email = validate_login_token(token_from_url)
        if email:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.login_token = token_from_url
            # Không xóa token khỏi URL để duy trì trạng thái đăng nhập khi F5
            # set_query_params({"token": None})
            # Hiển thị thông báo đăng nhập tự động
            #st.success(f"🔄 Đăng nhập tự động thành công! Chào mừng {email}")
            return True
    
    # Kiểm tra nếu đã có token trong session
    if 'login_token' in st.session_state and st.session_state.login_token:
        email = validate_login_token(st.session_state.login_token)
        if email:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            # Đảm bảo token vẫn được giữ trong URL
            save_token_to_url(st.session_state.login_token)
            return True
    
    return False

def save_token_to_url(token):
    """Lưu token vào URL để duy trì trạng thái đăng nhập"""
    if token:
        set_query_params({"token": token})

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
    
    # Kiểm tra persistent login nếu chưa đăng nhập
    if not st.session_state.logged_in:
        check_persistent_login()
    
    # Hiển thị form đăng nhập/đăng ký nếu chưa đăng nhập
    if not st.session_state.logged_in:
        # Hỗ trợ mở form đăng ký qua query params (?view=register=1)
        query_params = get_query_params()
        view_param = query_params.get("view")
        if view_param == ["register"] or view_param == "register":
            st.session_state.show_register = True

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
    
    # Main content area
    if selected_menu == "chat":
        # Kiểm tra nếu người dùng muốn xem lịch sử đầy đủ
        if st.session_state.show_full_history:
            st.markdown("### 📚 Lịch sử chat đầy đủ")
            
            from chat_utils import get_chat_history, group_messages_by_conversation
            chat_history = get_chat_history(user_email)
            
            if not chat_history:
                st.info("Chưa có lịch sử chat nào.")
            else:
                # Nhóm tin nhắn theo cuộc trò chuyện
                conversations = group_messages_by_conversation(chat_history)
                
                # Hiển thị các cuộc trò chuyện theo thứ tự mới nhất
                for i, conversation in enumerate(reversed(conversations)):
                    # Thông tin cuộc trò chuyện
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
                    
                    # Header cuộc trò chuyện
                    st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid {CHAT_COLORS[config.get('chat_color', 'Blue')]};">
                        <strong>📅 Cuộc trò chuyện {len(conversations) - i}</strong><br>
                        <small>🕐 {date_str} | {time_range} | 💬 {message_count} tin nhắn</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Hiển thị tin nhắn trong cuộc trò chuyện
                    for message in conversation:
                        from chat_utils import display_chat_message
                        display_chat_message(message, config.get("chat_color", "Blue"))
                    
                    st.markdown("---")
                
                # Nút quay lại chat
                if st.button("🔙 Quay lại chat", type="primary"):
                    st.session_state.show_full_history = False
                    st.rerun()
        else:
            # Giao diện chat chính
            # col1, col2 = st.columns([2, 1])
            
            # with col1:
            #     # Chat interface
            #     create_chat_interface(user_email, config.get("chat_color", "Blue"))
            
            # with col2:
            #     # Chat history sidebar
            #     display_chat_history_sidebar(user_email, config.get("chat_color", "Blue"))
            # else:
            # Sử dụng container thay vì cột để khung chat rộng hơn
            with st.container():
                create_chat_interface(user_email, config.get("chat_color", "Blue"))
            # Lịch sử chat sidebar
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
        
        from chat_utils import get_chat_history, group_messages_by_conversation
        chat_history = get_chat_history(user_email)
        
        if not chat_history:
            st.info("Chưa có lịch sử chat nào.")
        else:
            # Nhóm tin nhắn theo cuộc trò chuyện
            conversations = group_messages_by_conversation(chat_history)
            
            # Hiển thị các cuộc trò chuyện theo thứ tự mới nhất
            for i, conversation in enumerate(reversed(conversations)):
                # Thông tin cuộc trò chuyện
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
                
                # Header cuộc trò chuyện
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 15px 0; color: black; border: 1px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 4px solid {CHAT_COLORS[config.get('chat_color', 'Blue')]};">
                    <strong>📅 Cuộc trò chuyện {len(conversations) - i}</strong><br>
                    <small>🕐 {date_str} | {time_range} | 💬 {message_count} tin nhắn</small>
                </div>
                """, unsafe_allow_html=True)
                
                # Hiển thị tin nhắn trong cuộc trò chuyện
                for message in conversation:
                    from chat_utils import display_chat_message
                    display_chat_message(message, config.get("chat_color", "Blue"))
                
                st.markdown("---")

if __name__ == "__main__":
    main()