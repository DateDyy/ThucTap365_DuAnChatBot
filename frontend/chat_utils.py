import streamlit as st
import json
import os
from datetime import datetime
import time
import random

# File lưu trữ lịch sử chat
CHAT_HISTORY_DIR = "chat_history"

# Đảm bảo thư mục lưu trữ tồn tại
if not os.path.exists(CHAT_HISTORY_DIR):
    os.makedirs(CHAT_HISTORY_DIR)

def get_chat_file(user_email):
    """Lấy đường dẫn file lưu trữ chat của người dùng"""
    # Chuyển email thành tên file an toàn
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

def add_message(user_email, role, content):
    """Thêm tin nhắn vào lịch sử chat"""
    chat_history = get_chat_history(user_email)
    
    # Tạo ID cho tin nhắn mới
    message_id = str(int(time.time() * 1000))
    
    # Tạo ID cuộc trò chuyện (conversation_id)
    # Nếu không có tin nhắn nào hoặc tin nhắn cuối cùng đã cách đây hơn 30 phút, tạo ID mới
    if not chat_history or (int(time.time()) - int(chat_history[-1]["timestamp_unix"]) > 1800):
        conversation_id = f"conv_{int(time.time())}"
    else:
        conversation_id = chat_history[-1]["conversation_id"]
    
    # Thêm tin nhắn mới
    chat_history.append({
        "id": message_id,
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "timestamp_unix": str(int(time.time()))
    })
    
    # Lưu lịch sử chat
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
    
    # Sắp xếp các cuộc trò chuyện theo thời gian
    sorted_conversations = sorted(
        conversations.values(), 
        key=lambda x: x[0].get("timestamp_unix", "0")
    )
    
    return sorted_conversations

def display_chat_message(message, chat_color):
    """Hiển thị tin nhắn chat với định dạng phù hợp"""
    role = message.get("role", "unknown")
    content = message.get("content", "")
    timestamp = message.get("timestamp", "")
    
    # Escape HTML trong nội dung tin nhắn
    from html import escape
    safe_content = escape(content)
    
    try:
        dt = datetime.fromisoformat(timestamp)
        time_str = dt.strftime("%H:%M")
    except:
        time_str = "??:??"
    
    if role == "user":
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
            <div style="
                background-color: {chat_color}; 
                color: black; 
                padding: 12px 16px; 
                border-radius: 18px 18px 0 18px; 
                max-width: 75%;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                {safe_content}
                <div style="
                    font-size: 0.7rem; 
                    text-align: right; 
                    margin-top: 6px; 
                    opacity: 0.8;">
                    {time_str}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
            <div style="
                background-color: #f8f9fa; 
                color: #212529; 
                padding: 12px 16px; 
                border-radius: 18px 18px 18px 0; 
                max-width: 75%;
                border-left: 4px solid {chat_color};
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                {safe_content}
                <div style="
                    font-size: 0.7rem; 
                    text-align: right; 
                    margin-top: 6px; 
                    opacity: 0.8;">
                    {time_str}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_chat_interface(user_email, chat_color_name):
    """Tạo giao diện chat"""
    from config import CHAT_COLORS
    
    chat_color = CHAT_COLORS.get(chat_color_name, "#007bff")
    
    # Khởi tạo session state cho tin nhắn
    if "messages" not in st.session_state:
        st.session_state.messages = get_chat_history(user_email)
    
    # Hiển thị tin nhắn
    for message in st.session_state.messages:
        display_chat_message(message, chat_color)
    
    # Tạo container cho tin nhắn mới
    message_container = st.container()
    
    # Form nhập tin nhắn
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([8, 1])
        
        with col1:
            user_input = st.text_area(
                "Nhập tin nhắn:",
                key="user_input",
                height=70,
                placeholder="Nhập tin nhắn của bạn...",
                label_visibility="collapsed"
            )
        
        with col2:
            submit_button = st.form_submit_button(
                "Gửi",
                type="primary",
                use_container_width=True
            )
        
        if submit_button and user_input:
            # Thêm tin nhắn người dùng
            add_message(user_email, "user", user_input)
            
            # Hiển thị tin nhắn người dùng
            with message_container:
                display_chat_message({"role": "user", "content": user_input, "timestamp": datetime.now().isoformat()}, chat_color)
            
            # Mô phỏng AI đang xử lý
            with st.spinner("AI đang xử lý..."):
                # Mô phỏng độ trễ
                time.sleep(random.uniform(0.5, 1.5))
                
                # Mô phỏng phản hồi từ AI
                ai_response = "Đây là phản hồi mẫu từ AI. Trong ứng dụng thực tế, phản hồi này sẽ được lấy từ API của mô hình AI."
                
                # Thêm tin nhắn AI
                add_message(user_email, "assistant", ai_response)
                
                # Hiển thị tin nhắn AI
                with message_container:
                    display_chat_message({"role": "assistant", "content": ai_response, "timestamp": datetime.now().isoformat()}, chat_color)
            
            # Cập nhật lịch sử chat
            st.session_state.messages = get_chat_history(user_email)

def display_chat_history_sidebar(user_email, chat_color_name):
    """Hiển thị lịch sử chat ở sidebar"""
    from config import CHAT_COLORS
    
    chat_color = CHAT_COLORS.get(chat_color_name, "#007bff")
    
    st.markdown("### 📚 Lịch sử chat gần đây")
    
    # Lấy lịch sử chat
    chat_history = get_chat_history(user_email)
    
    if not chat_history:
        st.info("Chưa có lịch sử chat nào.")
        return
    
    # Nhóm tin nhắn theo cuộc trò chuyện
    conversations = group_messages_by_conversation(chat_history)
    
    # Hiển thị tối đa 5 cuộc trò chuyện gần nhất
    for i, conversation in enumerate(reversed(conversations[:5])):
        # Thông tin cuộc trò chuyện
        conversation_start = conversation[0]["timestamp"]
        message_count = len(conversation)
        
        try:
            dt = datetime.fromisoformat(conversation_start)
            date_str = dt.strftime("%d/%m/%Y")
            time_str = dt.strftime("%H:%M")
        except:
            date_str = "Unknown"
            time_str = "Unknown"
        
        # Lấy nội dung tin nhắn đầu tiên của người dùng
        first_user_message = next((msg for msg in conversation if msg["role"] == "user"), None)
        preview_text = first_user_message["content"] if first_user_message else "Không có nội dung"
        
        # Cắt ngắn preview nếu quá dài
        if len(preview_text) > 50:
            preview_text = preview_text[:50] + "..."
        
        # Hiển thị preview cuộc trò chuyện
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 3px solid {chat_color};">
            <div style="font-size: 0.8rem; opacity: 0.7; color: black;">{date_str} | {time_str}</div>
            <div style="font-size: 0.9rem; margin: 5px 0; color: black;">{preview_text}</div>
            <div style="font-size: 0.8rem; text-align: right; opacity: 0.7; color: black;">{message_count} tin nhắn</div>
        </div>
        """, unsafe_allow_html=True)
    # Nút xem tất cả lịch sử
    if st.button("Xem tất cả lịch sử", key="view_all_history"):
        st.session_state.show_full_history = True
        st.rerun()
    
    # Nút xóa lịch sử
    if st.button("Xóa lịch sử", key="clear_history"):
        clear_chat_history(user_email)
        st.success("Đã xóa lịch sử chat!")
        st.rerun()