import streamlit as st
import json
import os
from datetime import datetime
import time
import random
import requests

# File lưu trữ lịch sử chat
CHAT_HISTORY_DIR = "chat_history"

# Đảm bảo thư mục lưu trữ tồn tại
if not os.path.exists(CHAT_HISTORY_DIR):
    os.makedirs(CHAT_HISTORY_DIR)

def get_chat_file(user_email):
    """Lấy đường dẫn file lưu trữ chat của người dùng"""
    safe_email = user_email.replace("@", "_at_").replace(".", "_dot_")
    return os.path.join(CHAT_HISTORY_DIR, f"{safe_email}_chat.json")

def get_chat_history(user_email):
    """Lấy lịch sử chat của người dùng"""
    chat_file = get_chat_file(user_email)
    if os.path.exists(chat_file):
        try:
            with open(chat_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    else:
        return []

def save_chat_history(user_email, chat_history):
    """Lưu lịch sử chat của người dùng"""
    chat_file = get_chat_file(user_email)
    with open(chat_file, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False)

def add_message(user_email, role, content, file_info=None):
    """Thêm tin nhắn vào lịch sử chat"""
    chat_history = get_chat_history(user_email)
    message_id = str(int(time.time() * 1000))

    # Nếu vừa nhấn "Chat mới" hoặc chưa có conv_id thì tạo mới
    if st.session_state.get("new_conversation", False) or not st.session_state.get("active_conversation_id"):
        conversation_id = f"conv_{int(time.time())}"
        st.session_state.active_conversation_id = conversation_id
        st.session_state.new_conversation = False
    else:
        conversation_id = st.session_state.active_conversation_id

    chat_history.append({
        "id": message_id,
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "timestamp_unix": str(int(time.time()))
    })

    save_chat_history(user_email, chat_history)
    return message_id

def clear_chat_history(user_email):
    """Xóa lịch sử chat của người dùng"""
    chat_file = get_chat_file(user_email)
    if os.path.exists(chat_file):
        os.remove(chat_file)

def group_messages_by_conversation(messages):
    """Nhóm tin nhắn theo cuộc trò chuyện"""
    conversations = {}
    for message in messages:
        conversation_id = message.get("conversation_id", "default")
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        conversations[conversation_id].append(message)
    
    # Sắp xếp theo thời gian
    sorted_conversations = sorted(
        conversations.values(), 
        key=lambda x: x[0].get("timestamp_unix", "0")
    )
    return sorted_conversations

def display_chat_message(message, chat_color):
    """Hiển thị tin nhắn chat"""
    role = message.get("role", "unknown")
    content = message.get("content", "")
    timestamp = message.get("timestamp", "")

    # Sử dụng thư viện html để mã hóa nội dung
    import html
    # Thay thế \n bằng <br> để hiển thị xuống dòng đúng
    safe_content = html.escape(content).replace('\n', '<br>')
    
    try:
        dt = datetime.fromisoformat(timestamp)
        time_str = dt.strftime("%H:%M")
    except:
        time_str = "??:??"
    
    if role == "user":
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin: 15px 0;">
            <div style="
                background: linear-gradient(135deg, {chat_color}, {chat_color}CC); 
                color: white; 
                padding: 14px 18px; 
                border-radius: 20px 20px 0 20px; 
                max-width: 75%;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                font-size: 15px;
                line-height: 1.5;">
                {safe_content}
                <div style="font-size: 0.7rem; text-align: right; margin-top: 8px; opacity: 0.8;">
                    {time_str}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin: 15px 0;">
            <div style="
                background: linear-gradient(135deg, #f8f9fa, #e9ecef); 
                color: #212529; 
                padding: 14px 18px; 
                border-radius: 20px 20px 20px 0; 
                max-width: 75%;
                border-left: 4px solid {chat_color};
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                font-size: 15px;
                line-height: 1.5;">
                {safe_content}
                <div style="font-size: 0.7rem; text-align: right; margin-top: 8px; opacity: 0.8;">
                    {time_str}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_chat_interface(user_email, chat_color_name):
    from config import CHAT_COLORS
    chat_color = CHAT_COLORS.get(chat_color_name, "#007bff")
    
    history = get_chat_history(user_email)

    # Nếu chưa có active_conversation_id thì lấy conv mới nhất, trừ khi vừa nhấn Chat mới
    if "active_conversation_id" not in st.session_state or not st.session_state.active_conversation_id:
        if not st.session_state.get("new_conversation", False) and history:
            st.session_state.active_conversation_id = history[-1]["conversation_id"]
        else:
            st.session_state.active_conversation_id = None
            st.session_state.messages = []
            
            # Hiển thị tin nhắn chào mừng khi bắt đầu cuộc trò chuyện mới
            welcome_message = {
                "role": "assistant", 
                "content": "Xin chào! Tôi có thể giúp gì cho bạn?", 
                "timestamp": datetime.now().isoformat()
            }
            display_chat_message(welcome_message, chat_color)
            add_message(user_email, "assistant", welcome_message["content"])

    # Lọc tin nhắn theo hội thoại đang mở (nếu có)
    st.session_state.messages = [
        msg for msg in history if msg.get("conversation_id") == st.session_state.active_conversation_id
    ] if st.session_state.active_conversation_id else []

    # Hiển thị lịch sử
    for message in st.session_state.messages:
        display_chat_message(message, chat_color)
    
    message_container = st.container()
    
    # CSS tùy chỉnh cho input và nút gửi
    st.markdown("""
    <style>
    .chat-input-container {
        display: flex;
        align-items: flex-end;
        gap: 10px;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
        padding: 10px;
        background: #f8f9fa;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .stTextArea textarea {
        color: black;
        border-radius: 30px !important;
        border: 1px solid #e0e0e0 !important;
        padding: 10px 20px !important;
        font-size: 14px !important;
        box-shadow: none !important;
        transition: all 0.3s ease !important;
        background-color: #f0f2f5 !important;
        height: 40px !important;
        min-height: 40px !important;
    }
    .stTextArea textarea:focus {
        border-color: #e0e0e0 !important;
        box-shadow: none !important;
    }
    .send-button {
        background-color: transparent;
        border-radius: 12px !important;
        padding: 0.6rem 1.5rem !important;
        font-size: 700px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
    }
    .send-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    }
    /* Tùy chỉnh nút mở rộng */
    .stButton button[data-key="expand_button"] {
        border-radius: 50%;
        width: 40px;
        height: 40px;
        background-color: #f0f2f5;
        color: #333;
        padding: 0px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        margin: 10px auto;
    }
    
    /* Tùy chỉnh panel mở rộng */
    .stMarkdown h3 {
        font-size: 16px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    
    /* Tùy chỉnh file uploader */
    .stFileUploader > div {
        padding: 5px;
        border-radius: 10px;
    }
    
    .stFileUploader button {
        border-radius: 10px;
        background-color: #f0f2f5;
    }
    </style>
    """, unsafe_allow_html=True)
    
    
        
    
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([20, 2])
        with col1:
            user_input = st.text_area(
                "Nhập tin nhắn:",
                key="user_input",
                height=40,
                placeholder="Nhập tin nhắn của bạn...",
                label_visibility="collapsed"
            )
        with col2:
            submit_button = st.form_submit_button(
                "➤",
                type="primary",
                use_container_width=True,
                help="Gửi tin nhắn hoặc file"
            )
        
        if submit_button and (user_input or st.session_state.uploaded_file):
            file_info = None
            
            # Xử lý khi có file được tải lên
            if st.session_state.uploaded_file:
                file_info = {
                    "filename": st.session_state.uploaded_file.name,
                    "type": st.session_state.uploaded_file.type,
                    "size": st.session_state.uploaded_file.size
                }
                if user_input:
                    message_content = f"{user_input}\n[File đính kèm: {st.session_state.uploaded_file.name}]"
                else:
                    message_content = f"[File đính kèm: {st.session_state.uploaded_file.name}]"
            else:
                message_content = user_input
            
            add_message(user_email, "user", message_content, file_info)
            with message_container:
                display_chat_message(
                    {"role": "user", "content": message_content, "timestamp": datetime.now().isoformat(), "file_info": file_info}, 
                    chat_color
                )
            
            with st.spinner("AI đang xử lý..."):
                try:
                    # Lấy toàn bộ lịch sử chat để gửi kèm cho API
                    history = [
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in get_chat_history(user_email)
                    ]

                    response = requests.post(
                        "http://127.0.0.1:8000/api/chat",
                        json={"message": message_content}
                    )

                    if response.status_code == 200:
                        data = response.json()
                        ai_response = data.get("response", "⚠️ Không có phản hồi từ API.")
                    else:
                        ai_response = f"⚠️ Lỗi server: {response.status_code}"

                except Exception as e:
                    ai_response = f"⚠️ Lỗi kết nối API: {str(e)}"

                # Lưu & hiển thị tin nhắn AI
                add_message(user_email, "assistant", ai_response)
                with message_container:
                    display_chat_message(
                        {"role": "assistant", "content": ai_response, "timestamp": datetime.now().isoformat()},
                        chat_color
                    )

            
            # Reset file uploader sau khi gửi
            st.session_state.uploaded_file = None
            
            st.session_state.messages = get_chat_history(user_email)
    # Thêm state cho panel mở rộng và file đã upload

    # Thêm file uploader trước form
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    
    st.session_state.uploaded_file = st.file_uploader(
        "Chọn file", 
        type=["jpg", "jpeg", "png", "pdf", "doc", "docx", "xls", "xlsx", "txt", "zip", "rar"],
        help="Tải lên file",
        label_visibility="collapsed"
    )


    if "show_expand_panel" not in st.session_state:
        st.session_state.show_expand_panel = False
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    
    

def delete_conversation(user_email, conversation_id):
    """Xóa một cuộc trò chuyện cụ thể"""
    chat_history = get_chat_history(user_email)
    new_history = [msg for msg in chat_history if msg.get("conversation_id") != conversation_id]
    save_chat_history(user_email, new_history)

    if st.session_state.get("active_conversation_id") == conversation_id:
        st.session_state.active_conversation_id = None
        st.session_state.messages = []
    else:
        st.session_state.messages = new_history

def display_profile_page(user_email):
    """Hiển thị trang hồ sơ người dùng"""
    st.title("Hồ sơ người dùng")
    st.write(f"Email: {user_email}")
    if st.button("⬅️ Quay lại chat"):
        st.session_state.page = "chat"
        # load lại lịch sử theo active_conversation_id
        history = get_chat_history(user_email)
        if st.session_state.get("active_conversation_id"):
            st.session_state.messages = [
                msg for msg in history if msg.get("conversation_id") == st.session_state.active_conversation_id
            ]
        st.rerun()

def display_settings_page(chat_color_name):
    """Hiển thị trang cài đặt"""
    from config import CHAT_COLORS
    chat_color = CHAT_COLORS.get(chat_color_name, "#007bff")
    st.title("Cài đặt")
    st.write("Đây là trang cài đặt. Bạn có thể thêm các tùy chọn ở đây.")
    # Thêm một ví dụ tùy chỉnh màu sắc
    st.color_picker("Chọn màu chat", value=chat_color, key="color_picker")

    if st.button("⬅️ Quay lại chat"):
        st.session_state.page = "chat"
        # load lại lịch sử theo active_conversation_id
        history = get_chat_history(st.session_state.user_email)
        if st.session_state.get("active_conversation_id"):
            st.session_state.messages = [
                msg for msg in history if msg.get("conversation_id") == st.session_state.active_conversation_id
            ]
        st.rerun()

def display_chat_history_sidebar(user_email, chat_color_name):
    from config import CHAT_COLORS
    chat_color = CHAT_COLORS.get(chat_color_name, "#007bff")

    if "open_menu_conv_id" not in st.session_state:
        st.session_state.open_menu_conv_id = None

    st.sidebar.markdown("### 🗂 Lịch sử trò chuyện")
    history = get_chat_history(user_email)
    conversations = group_messages_by_conversation(history)

    if not conversations:
        st.sidebar.info("Chưa có cuộc trò chuyện nào.")
        return

    for conv in reversed(conversations[-10:]):
        first_msg = conv[0]["content"][:40] + ("..." if len(conv[0]["content"]) > 40 else "")
        try:
            start_time = datetime.fromisoformat(conv[0]["timestamp"]).strftime("%d/%m %H:%M")
        except:
            start_time = "??/?? ??"

        conversation_id = conv[0]["conversation_id"]

        col1, col2 = st.sidebar.columns([5, 1.5], vertical_alignment="center")

        # Nút mở hội thoại
        with col1:
            if st.button(f"💬 {first_msg} ({start_time})", key=f"open_{conversation_id}"):
                st.session_state.active_conversation_id = conversation_id
                st.session_state.page = "chat"
                st.rerun()

        # Nút xóa (ngang hàng)
        with col2:
            delete_btn_key = f"del_{conversation_id}"
            if st.button("Xóa", key=delete_btn_key):
                # Xóa cuộc trò chuyện khỏi lịch sử
                chat_history = get_chat_history(user_email)
                chat_history = [msg for msg in chat_history if msg.get("conversation_id") != conversation_id]
                save_chat_history(user_email, chat_history)

                # Cập nhật trạng thái
                if st.session_state.active_conversation_id == conversation_id:
                    st.session_state.active_conversation_id = None
                    st.session_state.messages = []
                st.session_state.open_menu_conv_id = None
                st.rerun()

    # Xóa toàn bộ lịch sử
    if st.sidebar.button("🗑 Xóa lịch sử", use_container_width=True):
        clear_chat_history(user_email)
        st.sidebar.success("Đã xóa toàn bộ lịch sử ✅")
        st.session_state.messages = []
        st.session_state.active_conversation_id = None
        st.session_state.page = "chat"
        st.rerun()


# Main app
def main():
    # Khởi tạo trạng thái trang mặc định là chat
    if "page" not in st.session_state:
        st.session_state.page = "chat"
    if "user_email" not in st.session_state:
        st.session_state.user_email = "hoccolab@gmail.com"  # Giả lập email
    if "chat_color_name" not in st.session_state:
        st.session_state.chat_color_name = "blue"  # Mặc định màu xanh

    # Hiển thị sidebar
    display_chat_history_sidebar(st.session_state.user_email, st.session_state.chat_color_name)

    # Hiển thị nội dung dựa trên trang hiện tại
    st.sidebar.title("AI Chat Assistant")
    selected_menu = show_sidebar_menu(st.session_state.user_email)

    # Điều hướng theo menu đã chọn
    if selected_menu == "chat":
        st.session_state.page = "chat"
    elif selected_menu == "profile":
        st.session_state.page = "profile"
    elif selected_menu == "settings":
        st.session_state.page = "settings"

    # Cập nhật màu sắc từ color picker nếu có thay đổi
    if "color_picker" in st.session_state and st.session_state.color_picker:
        st.session_state.chat_color_name = st.session_state.color_picker

    # Hiển thị nội dung chính với sidebar luôn hiển thị
    if st.session_state.page == "chat":
        create_chat_interface(st.session_state.user_email, st.session_state.chat_color_name)
    elif st.session_state.page == "profile":
        display_profile_page(st.session_state.user_email)
    elif st.session_state.page == "settings":
        display_settings_page(st.session_state.chat_color_name)

if __name__ == "__main__":
    main()