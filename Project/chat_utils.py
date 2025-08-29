import streamlit as st
import json
import os
from datetime import datetime
from config import save_chat_history, load_chat_history, CHAT_COLORS
import base64

def add_message_to_history(user_id, message, sender="user", file_info=None):
    """Thêm tin nhắn vào lịch sử chat"""
    chat_history = load_chat_history(user_id)
    
    new_message = {
        "id": len(chat_history) + 1,
        "message": message,
        "sender": sender,
        "timestamp": datetime.now().isoformat(),
        "file_info": file_info
    }
    
    chat_history.append(new_message)
    save_chat_history(user_id, chat_history)
    return chat_history

def get_chat_history(user_id):
    """Lấy lịch sử chat của người dùng"""
    return load_chat_history(user_id)

def clear_chat_history(user_id):
    """Xóa lịch sử chat"""
    save_chat_history(user_id, [])
    return True

def display_chat_message(message_data, chat_color):
    """Hiển thị tin nhắn chat"""
    message = message_data["message"]
    sender = message_data["sender"]
    timestamp = message_data["timestamp"]
    file_info = message_data.get("file_info")
    
    # Chuyển đổi timestamp
    try:
        dt = datetime.fromisoformat(timestamp)
        time_str = dt.strftime("%H:%M")
    except:
        time_str = "Unknown"
    
    if sender == "user":
        st.markdown(f"""
        <div style="text-align: right; margin: 10px 0;">
            <div style="background-color: {CHAT_COLORS[chat_color]}; color: white; padding: 10px 15px; border-radius: 15px; display: inline-block; max-width: 70%;">
                {message}
                <br><small style="opacity: 0.7;">{time_str}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align: left; margin: 10px 0;">
            <div style="background-color: #e9ecef; color: #333; padding: 10px 15px; border-radius: 15px; display: inline-block; max-width: 70%;">
                {message}
                <br><small style="opacity: 0.7;">{time_str}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Hiển thị file nếu có
    if file_info:
        st.markdown(f"""
        <div style="margin: 5px 0; padding: 10px; background-color: #f8f9fa; border-radius: 5px; border-left: 3px solid {CHAT_COLORS[chat_color]};">
            <strong>📎 File đính kèm:</strong> {file_info['filename']}
            <br><small>Kích thước: {file_info['size']} bytes</small>
        </div>
        """, unsafe_allow_html=True)

def handle_file_upload():
    """Xử lý upload file"""
    uploaded_file = st.file_uploader(
        "Chọn file để đính kèm",
        type=['txt', 'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif'],
        help="Hỗ trợ file văn bản, PDF, Word và hình ảnh"
    )
    
    if uploaded_file is not None:
        file_info = {
            "filename": uploaded_file.name,
            "size": uploaded_file.size,
            "type": uploaded_file.type
        }
        
        # Hiển thị thông tin file
        st.info(f"📎 File: {uploaded_file.name} ({uploaded_file.size} bytes)")
        
        return uploaded_file, file_info
    
    return None, None

def simulate_ai_response(user_message, file_info=None):
    """Mô phỏng phản hồi từ AI (tạm thời)"""
    # Đây là phản hồi mẫu, sẽ được thay thế bằng OpenAI API sau
    responses = [
        "Cảm ơn bạn đã gửi tin nhắn! Tôi đang xử lý yêu cầu của bạn.",
        "Tôi hiểu rồi. Bạn có thể cho tôi biết thêm chi tiết không?",
        "Đây là một câu hỏi thú vị. Hãy để tôi suy nghĩ về điều này.",
        "Tôi có thể giúp bạn với vấn đề này. Bạn muốn tôi giải thích chi tiết hơn không?",
        "Cảm ơn bạn đã chia sẻ thông tin này với tôi."
    ]
    
    import random
    response = random.choice(responses)
    
    if file_info:
        response += f"\n\nTôi đã nhận được file {file_info['filename']} của bạn và đang phân tích nội dung."
    
    return response

def create_chat_interface(user_id, chat_color):

    
    # Hiển thị lịch sử chat
    chat_history = get_chat_history(user_id)
    
    # Container cho chat history
    chat_container = st.container()
    
    with chat_container:
        for message_data in chat_history:
            display_chat_message(message_data, chat_color)
    
    # Input area
    st.markdown("---")
    
    # File upload
    uploaded_file, file_info = handle_file_upload()
    
    # Chat input area với layout mới
    st.markdown("""
    <style>
    .chat-input-container {
        position: relative;
        margin: 20px 0;
    }
    .chat-input {
        width: 100%;
        padding: 15px;
        border: 2px solid #e9ecef;
        border-radius: 25px;
        font-size: 16px;
        resize: none;
        outline: none;
    }
    .chat-input:focus {
        border-color: #007bff;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Text input với placeholder
    user_input = st.text_area(
        "Nhập tin nhắn của bạn...",
        height=60,
        placeholder="Gõ tin nhắn và nhấn Enter để gửi...",
        key="chat_input"
    )
    
    # Control buttons
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        # Voice button (đã di chuyển xuống dưới)
        voice_button = st.button("🎤 Ghi âm", help="Nhấn để ghi âm (sẽ được implement sau)", use_container_width=True)
        if voice_button:
            st.info("Tính năng ghi âm sẽ được implement sau!")
    
    with col2:
        clear_button = st.button("🗑️ Xóa", use_container_width=True)
    
    with col3:
        new_chat_button = st.button("🆕 Mới", use_container_width=True)
    
    with col4:
        send_button = st.button("Gửi", type="primary", use_container_width=True)
    
    # Xử lý các button
    if clear_button:
        clear_chat_history(user_id)
        st.success("Đã xóa lịch sử chat!")
        st.rerun()
    
    if new_chat_button:
        # Tạo chat mới (giữ nguyên lịch sử nhưng bắt đầu cuộc trò chuyện mới)
        st.success("Bắt đầu cuộc trò chuyện mới!")
        st.rerun()
    
    # Xử lý gửi tin nhắn
    if send_button and user_input.strip():
        # Thêm tin nhắn người dùng
        add_message_to_history(user_id, user_input.strip(), "user", file_info)
        
        # Mô phỏng phản hồi AI
        ai_response = simulate_ai_response(user_input.strip(), file_info)
        add_message_to_history(user_id, ai_response, "ai")
        
        st.success("Tin nhắn đã được gửi!")
        st.rerun()
    
    # JavaScript để xử lý Enter key
    st.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const textarea = document.querySelector('textarea[data-testid="stTextArea"]');
        if (textarea) {
            textarea.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    // Trigger the send button
                    const sendButton = document.querySelector('button[data-testid="baseButton-primary"]');
                    if (sendButton) {
                        sendButton.click();
                    }
                }
            });
        }
    });
    </script>
    """, unsafe_allow_html=True)

def display_chat_history_sidebar(user_id, chat_color):
    """Hiển thị lịch sử chat trong sidebar"""
    st.markdown("### 📚 Cuộc trò chuyện cuối")
    
    chat_history = get_chat_history(user_id)
    
    if not chat_history:
        st.info("Chưa có lịch sử chat nào.")
        return
    
    # Nhóm tin nhắn theo cuộc trò chuyện (dựa trên thời gian)
    conversations = group_messages_by_conversation(chat_history)
    
    if not conversations:
        st.info("Chưa có cuộc trò chuyện nào.")
        return
    
    # Lấy cuộc trò chuyện cuối cùng
    latest_conversation = conversations[-1]
    
    # Hiển thị thông tin cuộc trò chuyện
    conversation_start = latest_conversation[0]["timestamp"]
    conversation_end = latest_conversation[-1]["timestamp"]
    message_count = len(latest_conversation)
    
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
    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid {CHAT_COLORS[chat_color]};">
        <strong>📅 {date_str}</strong><br>
        <small>🕐 {time_range} | 💬 {message_count} tin nhắn</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Tìm tin nhắn cuối cùng của người dùng trong cuộc trò chuyện
    user_messages = [msg for msg in latest_conversation if msg["sender"] == "user"]
    if user_messages:
        latest_user_message = user_messages[-1]
        message = latest_user_message["message"]
        
        # Rút gọn tin nhắn nếu quá dài
        if len(message) > 80:
            message = message[:80] + "..."
        
        st.markdown(f"""
        <div style="background-color: {CHAT_COLORS[chat_color]}; color: white; padding: 10px 15px; border-radius: 12px; margin: 5px 0; font-size: 0.9em;">
            <strong>Bạn:</strong> {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Chưa có tin nhắn từ bạn.")
    
    # Nút xem tất cả lịch sử
    if st.button("📖 Xem tất cả lịch sử", use_container_width=True):
        st.session_state.show_full_history = True
        st.rerun()

def group_messages_by_conversation(chat_history):
    """Nhóm tin nhắn theo cuộc trò chuyện dựa trên thời gian"""
    if not chat_history:
        return []
    
    conversations = []
    current_conversation = [chat_history[0]]
    
    for i in range(1, len(chat_history)):
        current_msg = chat_history[i]
        prev_msg = chat_history[i-1]
        
        # Tính khoảng thời gian giữa 2 tin nhắn
        try:
            current_time = datetime.fromisoformat(current_msg["timestamp"])
            prev_time = datetime.fromisoformat(prev_msg["timestamp"])
            time_diff = (current_time - prev_time).total_seconds() / 60  # phút
            
            # Nếu khoảng cách > 30 phút, coi như cuộc trò chuyện mới
            if time_diff > 30:
                conversations.append(current_conversation)
                current_conversation = [current_msg]
            else:
                current_conversation.append(current_msg)
        except:
            # Nếu có lỗi parse time, thêm vào cuộc trò chuyện hiện tại
            current_conversation.append(current_msg)
    
    # Thêm cuộc trò chuyện cuối cùng
    if current_conversation:
        conversations.append(current_conversation)
    
    return conversations
