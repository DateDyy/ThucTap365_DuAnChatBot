import streamlit as st
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
                background-color: #007bff;
                color: white;
            }
            .assistant-message {
                background-color: #f8f9fa;
                color: #212529;
                border-left: 4px solid #007bff;
            }
        </style>
        """, unsafe_allow_html=True)
    
    def display_chat_history(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    def create_chat_input(self):
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