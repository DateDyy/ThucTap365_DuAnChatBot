import streamlit as st
<<<<<<< Updated upstream
import time

class ChatBox:
    def __init__(self):
        self.setup_styles()
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        self.display_chat_history()
        self.create_chat_input()
    
    def setup_styles(self):
        st.markdown("""
        <style>
            .stChatMessage {
                border-radius: 12px;
                padding: 12px 16px;
                margin: 8px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
           .user-message {
                background: linear-gradient(135deg, #007bff, #00c4cc);
                color: white;
            }
            .assistant-message {
                background: linear-gradient(135deg, #f8f9fa, #e9ecef);
                color: #212529;
                border-left: 4px solid #007bff;
            }
        </style>
        """, unsafe_allow_html=True)
    
    def display_chat_history(self):
=======
import requests
import json

class ChatBox:
    def __init__(self):
        # Khởi tạo session state nếu chưa có
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Hiển thị các tin nhắn đã có
        self.display_chat_history()
        
        # Tạo form nhập tin nhắn
        self.create_chat_input()
    
    def display_chat_history(self):
        # Hiển thị lịch sử chat
>>>>>>> Stashed changes
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    def create_chat_input(self):
<<<<<<< Updated upstream
        if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Simulate streaming response
                for chunk in self.generate_response(prompt):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.05)
                
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    def generate_response(self, prompt):
        # Replace with actual API call
        response = f"Đây là phản hồi mẫu cho: {prompt}"
        for word in response.split():
            yield word + " "
=======
        # Tạo input cho người dùng
        if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
            # Thêm tin nhắn của người dùng vào lịch sử
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Hiển thị tin nhắn của người dùng
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Hiển thị tin nhắn đang xử lý của bot
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("⏳ Đang xử lý...")
                
                try:
                    # Gọi API để lấy phản hồi
                    # Thay thế URL bằng endpoint thực tế của bạn
                    response = self.get_bot_response(prompt)
                    
                    # Cập nhật tin nhắn của bot
                    message_placeholder.markdown(response)
                    
                    # Lưu tin nhắn của bot vào lịch sử
                    st.session_state.messages.append({"role": "assistant", "content": response})
                
                except Exception as e:
                    message_placeholder.markdown(f"❌ Lỗi: {str(e)}")
    
    def get_bot_response(self, prompt):
        # Hàm này sẽ gọi API để lấy phản hồi từ bot
        # Trong môi trường thực tế, bạn sẽ gọi API của mình ở đây
        
        # Mô phỏng gọi API (thay thế bằng API thực tế)
        try:
            # Thay thế URL này bằng endpoint thực tế của bạn
            api_url = "http://localhost:8000/api/chat"
            
            # Chuẩn bị dữ liệu gửi đi
            payload = {
                "query": prompt,
                "history": st.session_state.messages
            }
            
            # Gọi API (bỏ comment khi có API thực tế)
            # response = requests.post(api_url, json=payload)
            # return response.json()["response"]
            
            # Mô phỏng phản hồi (xóa khi có API thực tế)
            return f"Đây là phản hồi mẫu cho câu hỏi: {prompt}"
        
        except Exception as e:
            return f"Không thể kết nối đến API: {str(e)}"
>>>>>>> Stashed changes
